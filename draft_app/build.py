"""Sugeneruoja draft_app/index.html iš nba_reitingas_max.csv.

Paleidimas iš repozitorijos šaknies:  python3 draft_app/build.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POS = ["C", "PG", "PF", "SG", "SF"]


def num(v):
    v = (v or "").strip()
    return float(v) if v else None


def main():
    with open(ROOT / "nba_reitingas_max.csv", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    players = []
    for r in rows:
        players.append({
            "id": int(r["Rank_MAX"]),
            "rank": int(r["Rank_MAX"]),
            "name": r["Player"],
            "team": r["Team"],
            "pos": r["Pos"],
            "p": {c: int(r[c]) for c in POS},
            "inj": r["Injury"].strip(),
            "max": num(r["MAX"]),
            "zp": num(r["Z_proj"]),
            "zl": num(r["Z_last"]),
            "gp": int(r["GP_proj"]) if r["GP_proj"].strip() else None,
        })
    players.sort(key=lambda p: p["rank"])

    tpl = (ROOT / "draft_app" / "template.html").read_text(encoding="utf-8")
    html = tpl.replace("__DATA__", json.dumps(players, ensure_ascii=False, separators=(",", ":")))
    (ROOT / "draft_app" / "index.html").write_text(html, encoding="utf-8")
    print(f"index.html sugeneruotas: {len(players)} žaidėjai")


if __name__ == "__main__":
    main()
