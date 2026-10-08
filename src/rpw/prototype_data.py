"""Export RPW evidence for the Regular Send prototype (prototype/src/data/wise_position.json).

For every corridor where Wise was surveyed in the latest window it exports Wise's position versus other
credible quotes (from rpw.phase5 outputs) and an illustrative fee schedule implied by Wise's two surveyed
amounts (fee = fixed + variable x amount, in the sending currency). These are survey statistics,
not live or official Wise prices. Run `python -m rpw.phase5` first.
"""
import json

import pandas as pd

from . import config
from .analysis import LATEST_WINDOW
from .phase5 import TABLES, WISE

OUT = config.ROOT / "prototype" / "src" / "data" / "wise_position.json"


def _fee_schedule(q):
    w = q[q.complete_cost_eligible & q.period.isin(LATEST_WINDOW) & (q.firm == WISE)]
    p = w.pivot_table(index=["record_key", "corridor_key"], columns="amount_scenario",
                      values=["fee_lcu", "lcu_amount"], aggfunc="first").dropna()
    slope = (p.fee_lcu.cc2 - p.fee_lcu.cc1) / (p.lcu_amount.cc2 - p.lcu_amount.cc1)
    f = pd.DataFrame({"variable": slope, "fixed": p.fee_lcu.cc1 - slope * p.lcu_amount.cc1,
                      "lcuPerUsd": p.lcu_amount.cc1 / config.AMOUNTS["cc1"]}).reset_index()
    cur = w.groupby("corridor_key").lcu_code.agg(lambda s: s.mode().iloc[0])
    names = w.groupby("corridor_key")[["source_name", "destination_name"]].last()
    g = f.groupby("corridor_key")[["variable", "fixed", "lcuPerUsd"]].median()
    g["fixed"] = g.fixed.clip(lower=0)
    g["variable"] = g.variable.clip(lower=0)
    return g.join(cur.rename("sendCurrency")).join(names)


def export():
    q = pd.read_parquet(config.PROCESSED_DIR / "rpw_quotes_long.parquet")
    pos = pd.read_csv(TABLES / "wise_corridor_position_latest_window.csv")
    fees = _fee_schedule(q)
    out = []
    for key, g in pos.groupby("corridor_key"):
        if key not in fees.index:
            continue
        fs = fees.loc[key]
        row = {"corridor": key, "source": fs.source_name, "destination": fs.destination_name,
               "region": g.destination_region.iloc[0], "sendCurrency": fs.sendCurrency,
               "lcuPerUsd": round(float(fs.lcuPerUsd), 4),
               "illustrativeFee": {"fixed": round(float(fs.fixed), 2), "variablePct": round(float(fs.variable) * 100, 3)}}
        for sc, usd in config.AMOUNTS.items():
            s = g[g.amount_scenario == sc]
            if s.empty:
                continue
            s = s.iloc[0]
            row[f"usd{usd}"] = {"wiseTotal": round(s.wise_total, 2), "otherMedian": round(s.other_median, 2),
                                "shareCheaper": round(s.share_cheaper_all, 1), "gapVsMedian": round(s.gap_vs_median_pp, 2),
                                "otherProviders": int(s.other_providers), "quarters": int(s.periods)}
        if "usd200" in row and "usd500" in row:
            out.append(row)
    meta = {"source": "World Bank, Remittance Prices Worldwide (rpw_dataset_2011_2025_q3.xlsx)",
            "window": LATEST_WINDOW,
            "note": "Survey statistics, unweighted; not live or official Wise prices. Quote counts are not volumes.",
            "method": "docs/phase5_analysis.md (A1)"}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"meta": meta, "corridors": out}, indent=1, ensure_ascii=False) + "\n")
    return out


if __name__ == "__main__":
    rows = export()
    print(len(rows), "corridors")
    for r in rows[:3]:
        print(r)
