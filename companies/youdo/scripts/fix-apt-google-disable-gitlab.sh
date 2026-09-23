#!/usr/bin/env bash
set -euo pipefail

# Disable GitLab CE/EE APT repositories and refresh the official Google Linux
# signing key used by the Google Chrome repository.

if [[ ${EUID} -ne 0 ]]; then
  echo "Run as root: sudo $0" >&2
  exit 1
fi

expected_fingerprint="0E225917414670F4442C250DFD533C07C264648F"
work_dir="$(mktemp -d)"
trap 'rm -rf -- "${work_dir}"' EXIT

curl -fsSL https://dl.google.com/linux/linux_signing_key.pub \
  -o "${work_dir}/google-linux-signing-key.pub"

if ! gpg --show-keys --with-colons "${work_dir}/google-linux-signing-key.pub" \
  | awk -F: '$1 == "fpr" { print $10 }' \
  | grep -Fxq "${expected_fingerprint}"; then
  echo "Downloaded Google key does not contain expected fingerprint ${expected_fingerprint}" >&2
  exit 1
fi

gpg --batch --yes --dearmor \
  --output "${work_dir}/google-chrome.gpg" \
  "${work_dir}/google-linux-signing-key.pub"
install -o root -g root -m 0644 \
  "${work_dir}/google-chrome.gpg" \
  /usr/share/keyrings/google-chrome.gpg

printf '%s\n' \
  '### THIS FILE IS AUTOMATICALLY CONFIGURED ###' \
  '# Google Chrome repository; key is scoped with signed-by.' \
  'deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] https://dl.google.com/linux/chrome/deb/ stable main' \
  > "${work_dir}/google-chrome.list"
install -o root -g root -m 0644 \
  "${work_dir}/google-chrome.list" \
  /etc/apt/sources.list.d/google-chrome.list

for repo in gitlab_gitlab-ce gitlab_gitlab-ee; do
  source_file="/etc/apt/sources.list.d/${repo}.list"
  disabled_file="${source_file}.disabled"
  if [[ -f "${source_file}" ]]; then
    if [[ -e "${disabled_file}" ]]; then
      echo "Refusing to overwrite existing ${disabled_file}" >&2
      exit 1
    fi
    mv -- "${source_file}" "${disabled_file}"
  fi
done

apt-get update
