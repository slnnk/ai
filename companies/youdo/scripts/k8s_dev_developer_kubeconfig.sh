#!/usr/bin/env bash
# Build and check the shared developer kubeconfig for the Yandex dev cluster (DevOps-883).
# ServiceAccount k8s-access/k8s-dev-developer, token Secret managed in infra-tf/dev/developer-access.tf,
# RoleBinding developer-access (ClusterRole edit) comes from helm-charts/ephemeral-namespace.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  k8s_dev_developer_kubeconfig.sh build -o FILE    write kubeconfig (mode 0600), never prints the token
  k8s_dev_developer_kubeconfig.sh check -f FILE [-n NAMESPACE]
                                                   run read-only permission checks with FILE
Env:
  ADMIN_KUBECONFIG  admin kubeconfig to read the token and CA (default ~/.kube/config-yandex-dev)
  SERVER            API endpoint written to the kubeconfig (default: from ADMIN_KUBECONFIG)
Check uses `auth can-i` and server-side dry-run only; nothing is created.
EOF
}

ADMIN_KUBECONFIG=${ADMIN_KUBECONFIG:-$HOME/.kube/config-yandex-dev}
SA_NS=k8s-access
SA_NAME=k8s-dev-developer
SECRET=k8s-dev-developer-token

cmd=${1:-}; shift || true
out= file= ns=
while getopts "o:f:n:h" opt; do
  case $opt in
    o) out=$OPTARG ;;
    f) file=$OPTARG ;;
    n) ns=$OPTARG ;;
    *) usage; exit 0 ;;
  esac
done

build() {
  [[ -n $out ]] || { usage; exit 2; }
  local k="kubectl --kubeconfig $ADMIN_KUBECONFIG"
  local server ca token
  server=${SERVER:-$($k config view --minify -o jsonpath='{.clusters[0].cluster.server}')}
  ca=$($k -n $SA_NS get secret $SECRET -o jsonpath='{.data.ca\.crt}')
  token=$($k -n $SA_NS get secret $SECRET -o jsonpath='{.data.token}' | base64 -d)
  [[ -n $ca && -n $token ]] || { echo "token or CA is empty in $SA_NS/$SECRET" >&2; exit 1; }
  umask 077
  cat > "$out" <<EOF
apiVersion: v1
kind: Config
clusters:
- name: yandex-dev
  cluster:
    server: $server
    certificate-authority-data: $ca
users:
- name: $SA_NAME
  user:
    token: $token
contexts:
- name: yandex-dev
  context:
    cluster: yandex-dev
    user: $SA_NAME
current-context: yandex-dev
EOF
  chmod 600 "$out"
  echo "written $out (server $server, user $SA_NS/$SA_NAME)"
}

check() {
  [[ -n $file ]] || { usage; exit 2; }
  local k="kubectl --kubeconfig $file"
  if [[ -z $ns ]]; then
    ns=$($k get ns -l environment=dev,createdBy=jenkins -o jsonpath='{.items[0].metadata.name}')
  fi
  [[ -n $ns ]] || { echo "no dev namespace found" >&2; exit 1; }
  echo "whoami: $($k auth whoami -o jsonpath='{.status.userInfo.username}')"
  echo "dev namespace: $ns"
  local fail=0
  expect() { # expect yes|no verb resource namespace-or-empty
    local want=$1 verb=$2 res=$3 n=${4:-}
    local got
    got=$($k auth can-i "$verb" "$res" ${n:+-n "$n"} 2>/dev/null || true)
    printf '%-4s %-4s can-i %s %s %s\n' "$([[ $got == "$want" ]] && echo ok || echo FAIL)" "$got" "$verb" "$res" "${n:+-n $n}"
    [[ $got == "$want" ]] || fail=1
  }
  expect yes list namespaces
  expect no  create namespaces
  expect no  delete namespaces
  expect yes create deployments.apps "$ns"
  expect yes create pods/exec "$ns"
  expect yes create pods/portforward "$ns"
  expect yes get secrets "$ns"
  expect no  create rolebindings.rbac.authorization.k8s.io "$ns"
  expect no  get pods kube-system
  expect no  get secrets vault
  expect no  get pods monitoring
  local psa
  psa=$($k run psa-check --image=busybox --restart=Never -n "$ns" --dry-run=server \
        --overrides='{"spec":{"containers":[{"name":"psa-check","image":"busybox","securityContext":{"privileged":true}}]}}' 2>&1 || true)
  if grep -q 'violates PodSecurity' <<<"$psa"; then
    echo "ok   privileged pod rejected by Pod Security"
  else
    echo "FAIL privileged pod not rejected: ${psa%%$'\n'*}"; fail=1
  fi
  return $fail
}

case $cmd in
  build) build ;;
  check) check ;;
  *) usage ;;
esac
