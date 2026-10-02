#!/usr/bin/env python3
"""WebDriver session start time per test in a Jenkins web-autotest build.

For each uitests/logs_html/*.html artifact the gap is the time between the last log line
before the first "remote IP" line and that line (new WebDriver session on the grid).

Usage: jenkins_session_start_gap.py <job> <build> [<job> <build> ...]
  e.g. jenkins_session_start_gap.py youdo_web_testing_three 1614 youdo_web_testing_one 3343
Env: JENKINS_USER, JENKINS_TOKEN (source ~/ai/current/.env), JENKINS_URL (default build.youdo.sg).
"""
import base64, concurrent.futures as cf, datetime as dt, json, os, re, statistics, sys
import urllib.parse, urllib.request

BASE = os.environ.get("JENKINS_URL", "https://build.youdo.sg")
AUTH = "Basic " + base64.b64encode(f'{os.environ["JENKINS_USER"]}:{os.environ["JENKINS_TOKEN"]}'.encode()).decode()
TS = re.compile(r"^(\d{2}:\d{2}:\d{2}),(\d{3})")


def get(url, tries=3):
    req = urllib.request.Request(url, headers={"Authorization": AUTH})
    for i in range(tries):
        try:
            return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
        except OSError:
            if i == tries - 1:
                raise


def gap(build_url, path):
    try:
        text = get(f"{build_url}/artifact/{urllib.parse.quote(path)}")
    except OSError:
        return None
    prev = None
    for line in re.sub(r"<[^>]+>", "\n", text).replace("&nbsp;", " ").splitlines():
        m = TS.match(line.strip())
        if not m:
            continue
        t = dt.datetime.strptime(m.group(1), "%H:%M:%S") + dt.timedelta(milliseconds=int(m.group(2)))
        if "remote IP" in line:
            return None if prev is None else (t - prev).total_seconds() % 86400
        prev = t
    return None


def pct(v, p):
    return v[min(len(v) - 1, int(round(p / 100 * (len(v) - 1))))]


def main(args):
    if len(args) < 2 or len(args) % 2 or "-h" in args or "--help" in args:
        print(__doc__); return 1
    for job, num in zip(args[::2], args[1::2]):
        url = f"{BASE}/job/{job}/{num}"
        meta = json.loads(get(f"{url}/api/json?tree=result,duration,timestamp,artifacts%5BrelativePath%5D"))
        paths = [a["relativePath"] for a in meta["artifacts"]
                 if "/logs_html/" in a["relativePath"] and not a["relativePath"].endswith(("beforeClass.html", "afterClass.html"))]
        with cf.ThreadPoolExecutor(8) as ex:
            gaps = sorted(g for g in ex.map(lambda p: gap(url, p), paths) if g is not None)
        start = dt.datetime.fromtimestamp(meta["timestamp"] / 1000).strftime("%m-%d %H:%M")
        head = f"{job}/{num} {start} {meta['result']} {meta['duration'] / 60000:.1f} min, tests {len(paths)}, with session {len(gaps)}"
        if not gaps:
            print(head + ": no 'remote IP' lines"); continue
        print(f"{head}: median {statistics.median(gaps):.1f}s p90 {pct(gaps, 90):.1f}s "
              f"max {gaps[-1]:.1f}s sum {sum(gaps) / 60:.1f} min")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
