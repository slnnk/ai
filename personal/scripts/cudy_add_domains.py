"""Validate a plain v2fly domain file or apply a reviewed list to Cudy with --apply."""
import argparse
from pathlib import Path
import re
import shlex
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--label', required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9-]+', args.label):
        parser.error('Invalid backup label')
    domains = []
    for line in args.source.read_text().splitlines():
        value = line.split('#', 1)[0].strip()
        if not value:
            continue
        value = value.split()[0]
        if value.startswith(('full:', 'domain:')):
            value = value.split(':', 1)[1]
        if not re.fullmatch(r'[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?', value) or '.' not in value:
            raise SystemExit('Unsupported nonliteral entry; review source before applying')
        if value not in domains:
            domains.append(value)
    if not domains:
        parser.error('Empty source')
    print('Validated domains:', len(domains), flush=True)
    if not args.apply:
        return
    script = r'''
set -e
umask 077
test "$(uci -q get podkop.main.user_domain_list_type)" = dynamic
backup=/root/cudy-before-v2fly-LABEL
mkdir -p "$backup"
test -e "$backup/podkop" || cp -p /etc/config/podkop "$backup/"
previous=$(uci -q get podkop.main.user_domains || true)
current="$previous"
added=0
for domain in DOMAIN_WORDS; do
    case " $current " in
        *" $domain "*) ;;
        *) uci add_list podkop.main.user_domains="$domain"; current="$current $domain"; added=$((added+1));;
    esac
done
if [ "$added" -gt 0 ]; then
    uci commit podkop
    /etc/init.d/podkop reload
fi
sing-box check -c /etc/sing-box/config.json
current=$(uci -q get podkop.main.user_domains)
for domain in $previous; do
    case " $current " in *" $domain "*) ;; *) echo PREVIOUS_DOMAIN_MISSING; exit 1;; esac
done
count=0
for domain in DOMAIN_WORDS; do
    answer=$(dig @127.0.0.1 "$domain" A +short +time=2 +tries=1)
    if ! echo "$answer" | grep -Eq '^198\.(18|19)\.'; then
        echo "FAKEIP_FAILED=$domain";exit 1
    fi
    count=$((count+1))
done
echo ADDED_DOMAINS=$added
echo VERIFIED_FAKEIP_DOMAINS=$count
echo PREVIOUS_DOMAINS_PRESERVED
cat /var/run/cudy-vpn/status.json
curl -4 --noproxy '*' --connect-timeout 4 --max-time 8 -fsS https://ip.podkop.fyi/check
printf '\n'
'''.replace('LABEL', args.label).replace('DOMAIN_WORDS', ' '.join(shlex.quote(d) for d in domains))
    (args.source.parent/'applied-script.sh').write_text(script)
    result = subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=8',
                             '-o', 'StrictHostKeyChecking=yes', 'root@192.168.168.1',
                             'sh -c ' + shlex.quote(script)],
                            capture_output=True, text=True, timeout=100)
    print(result.stdout, flush=True)
    print(result.stderr, flush=True)
    (args.source.parent/'verification.txt').write_text(result.stdout+result.stderr)
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
