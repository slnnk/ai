#!/usr/bin/env python3
"""Render the Nomad resource optimization CSV as a standalone interactive HTML table."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Input CSV")
    parser.add_argument("--output", required=True, help="Output HTML")
    parser.add_argument("--title", default="Yandex-test · Nomad resource optimization")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()
    with input_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        rows = list(reader)

    services = len({row["Nomad job"] for row in rows})
    mem_recommendations = sum(bool(row["Recommended mem limit"]) for row in rows)
    cpu_recommendations = sum(bool(row["Recommended cpu limit"]) for row in rows)
    payload = json.dumps(rows, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    columns_json = json.dumps(columns, ensure_ascii=False).replace("</", "<\\/")
    generated = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")

    html = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{args.title}</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #0b1020;
      --panel: #11182b;
      --panel-2: #182137;
      --line: #2a3550;
      --text: #e8edf7;
      --muted: #9aa8bf;
      --accent: #71a7ff;
      --down: #3ddc97;
      --down-bg: rgba(61,220,151,.12);
      --up: #ffb454;
      --up-bg: rgba(255,180,84,.13);
      --same: #b7c4d8;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: radial-gradient(circle at 15% 0%, #17213b, var(--bg) 38rem); color: var(--text); font: 14px/1.45 Inter, ui-sans-serif, system-ui, -apple-system, sans-serif; }}
    main {{ max-width: 1900px; margin: 0 auto; padding: 28px; }}
    h1 {{ margin: 0; font-size: clamp(24px, 3vw, 38px); letter-spacing: -.035em; }}
    .subtitle {{ margin: 8px 0 22px; color: var(--muted); }}
    .cards {{ display: grid; grid-template-columns: repeat(4, minmax(150px, 1fr)); gap: 12px; margin-bottom: 18px; }}
    .card {{ padding: 16px; border: 1px solid var(--line); border-radius: 14px; background: rgba(17,24,43,.88); box-shadow: 0 12px 28px rgba(0,0,0,.18); }}
    .card strong {{ display: block; font-size: 24px; }}
    .card span {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .06em; }}
    .toolbar {{ display: flex; flex-wrap: wrap; align-items: center; gap: 12px; padding: 14px; border: 1px solid var(--line); border-bottom: 0; border-radius: 14px 14px 0 0; background: var(--panel); }}
    input[type=search] {{ flex: 1 1 340px; min-width: 220px; padding: 10px 12px; border: 1px solid var(--line); border-radius: 9px; background: #0c1324; color: var(--text); outline: none; }}
    input[type=search]:focus {{ border-color: var(--accent); box-shadow: 0 0 0 3px rgba(113,167,255,.12); }}
    label {{ color: var(--muted); white-space: nowrap; }}
    .count {{ margin-left: auto; color: var(--muted); }}
    .table-wrap {{ max-height: calc(100vh - 260px); overflow: auto; border: 1px solid var(--line); border-radius: 0 0 14px 14px; background: var(--panel); box-shadow: 0 18px 42px rgba(0,0,0,.22); }}
    table {{ width: 100%; min-width: 1650px; border-collapse: separate; border-spacing: 0; }}
    th {{ position: sticky; top: 0; z-index: 2; padding: 11px 10px; border-bottom: 1px solid var(--line); background: #202b44; color: #dce6f7; font-size: 12px; text-align: left; cursor: pointer; user-select: none; white-space: nowrap; }}
    th:hover {{ background: #283653; }}
    td {{ padding: 9px 10px; border-bottom: 1px solid rgba(42,53,80,.65); white-space: nowrap; font-variant-numeric: tabular-nums; }}
    tbody tr:nth-child(even) {{ background: rgba(255,255,255,.018); }}
    tbody tr:hover {{ background: rgba(113,167,255,.08); }}
    td:nth-child(n+3) {{ text-align: right; }}
    td:nth-child(1), td:nth-child(2) {{ color: #dce7fa; font-weight: 550; }}
    td.decrease {{ color: var(--down); background: var(--down-bg); }}
    td.increase {{ color: var(--up); background: var(--up-bg); }}
    td.same {{ color: var(--same); }}
    td.empty {{ color: #5f6e87; }}
    .legend {{ display: flex; gap: 16px; margin-top: 12px; color: var(--muted); font-size: 12px; }}
    .dot {{ display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 5px; }}
    .dot.down {{ background: var(--down); }} .dot.up {{ background: var(--up); }}
    a {{ color: var(--accent); }}
    @media (max-width: 800px) {{ main {{ padding: 16px; }} .cards {{ grid-template-columns: repeat(2, 1fr); }} .count {{ margin-left: 0; }} }}
  </style>
</head>
<body>
<main>
  <h1>{args.title}</h1>
  <p class="subtitle">Объединённые test-стенды · память в MiB · CPU в MHz · срез {generated}</p>
  <section class="cards">
    <div class="card"><strong>{services}</strong><span>сервисов</span></div>
    <div class="card"><strong>{len(rows)}</strong><span>job/task строк</span></div>
    <div class="card"><strong>{mem_recommendations}</strong><span>memory рекомендаций</span></div>
    <div class="card"><strong>{cpu_recommendations}</strong><span>CPU рекомендаций</span></div>
  </section>
  <section class="toolbar">
    <input id="search" type="search" placeholder="Поиск по Nomad job или task…" autofocus>
    <label><input id="changes" type="checkbox"> только с рекомендациями</label>
    <span class="count" id="count"></span>
    <a href="{input_path.name}">Скачать CSV</a>
  </section>
  <div class="table-wrap">
    <table>
      <thead><tr id="head"></tr></thead>
      <tbody id="body"></tbody>
    </table>
  </div>
  <div class="legend">
    <span><i class="dot down"></i>рекомендуется уменьшить</span>
    <span><i class="dot up"></i>рекомендуется увеличить</span>
    <span>Пусто — недостаточно истории или lifecycle task</span>
  </div>
</main>
<script>
const columns = {columns_json};
const allRows = {payload};
const numericColumns = new Set(columns.slice(2));
const recommendationBase = {{
  "Recommended mem limit": "Nomad mem limit",
  "Recommended max mem limit": "Nomad max mem limit",
  "Recommended cpu limit": "Nomad cpu limit"
}};
let sortColumn = "Nomad job";
let sortDirection = 1;

const head = document.getElementById("head");
const body = document.getElementById("body");
const search = document.getElementById("search");
const changes = document.getElementById("changes");
const count = document.getElementById("count");

for (const column of columns) {{
  const th = document.createElement("th");
  th.textContent = column;
  th.addEventListener("click", () => {{
    if (sortColumn === column) sortDirection *= -1;
    else {{ sortColumn = column; sortDirection = 1; }}
    render();
  }});
  head.appendChild(th);
}}

function comparisonClass(row, column) {{
  const baseColumn = recommendationBase[column];
  if (!baseColumn || row[column] === "") return row[column] === "" ? "empty" : "";
  const recommended = Number(row[column]);
  const base = Number(row[baseColumn]);
  if (!Number.isFinite(base) || base === 0) return "same";
  if (recommended < base) return "decrease";
  if (recommended > base) return "increase";
  return "same";
}}

function render() {{
  const needle = search.value.trim().toLowerCase();
  let rows = allRows.filter(row => {{
    const matchesSearch = !needle || row["Nomad job"].toLowerCase().includes(needle) || row["Nomad task"].toLowerCase().includes(needle);
    const hasRecommendation = row["Recommended mem limit"] !== "" || row["Recommended cpu limit"] !== "";
    return matchesSearch && (!changes.checked || hasRecommendation);
  }});
  rows.sort((a, b) => {{
    if (numericColumns.has(sortColumn)) {{
      const av = a[sortColumn] === "" ? Number.NEGATIVE_INFINITY : Number(a[sortColumn]);
      const bv = b[sortColumn] === "" ? Number.NEGATIVE_INFINITY : Number(b[sortColumn]);
      return (av - bv) * sortDirection;
    }}
    return a[sortColumn].localeCompare(b[sortColumn], "ru", {{numeric: true}}) * sortDirection;
  }});
  body.replaceChildren();
  for (const row of rows) {{
    const tr = document.createElement("tr");
    for (const column of columns) {{
      const td = document.createElement("td");
      td.textContent = row[column] === "" ? "—" : row[column];
      const cssClass = comparisonClass(row, column);
      if (cssClass) td.classList.add(cssClass);
      tr.appendChild(td);
    }}
    body.appendChild(tr);
  }}
  count.textContent = `Показано ${{rows.length}} из ${{allRows.length}}`;
}}

search.addEventListener("input", render);
changes.addEventListener("change", render);
render();
</script>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(json.dumps({"output": str(output_path), "rows": len(rows), "services": services}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

