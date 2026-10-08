"""Export real RPW corridor benchmarks for the prototype (prototype/src/data/benchmarks.json).

Benchmarks are survey statistics (USD 200 and USD 500 quotes, latest window, complete-cost quotes only).
Quotes shown inside the prototype itself are illustrative and are generated in the frontend.
"""
import json

import pandas as pd

from . import config
from .analysis import LATEST_WINDOW

CORRIDORS = ["GBRNGA", "GBRIND", "USAMEX", "USAPHL", "DEUTUR", "GBRKEN"]
OUT = config.ROOT / "prototype" / "src" / "data" / "benchmarks.json"


def export():
    q = pd.read_parquet(config.PROCESSED_DIR / "rpw_quotes_long.parquet")
    w = q[q.complete_cost_eligible & q.period.isin(LATEST_WINDOW) & q.corridor_key.isin(CORRIDORS)]
    out = []
    for key, g in w.groupby("corridor_key"):
        row = {"corridor": key, "source": g.source_name.iloc[-1], "destination": g.destination_name.iloc[-1],
               "sendCurrency": g.lcu_code.mode().iloc[0], "periods": sorted(g.period.unique().tolist()),
               "providers": int(g.firm.nunique())}
        for cc, usd in config.AMOUNTS.items():
            s = g[g.amount_scenario == cc]
            row[f"usd{usd}"] = {"quotes": int(len(s)), "p10": round(s.total_cost_pct.quantile(.1), 2),
                                "median": round(s.total_cost_pct.median(), 2),
                                "p90": round(s.total_cost_pct.quantile(.9), 2),
                                "medianFee": round(s.fee_pct.median(), 2), "medianFx": round(s.fx_margin_pct.median(), 2)}
        out.append(row)
    meta = {"source": "World Bank, Remittance Prices Worldwide (rpw_dataset_2011_2025_q3.xlsx)",
            "window": LATEST_WINDOW, "population": "complete_cost_eligible survey quotes (see docs/pipeline.md)",
            "note": "Survey benchmarks, not live prices. Unweighted across surveyed quotes."}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"meta": meta, "corridors": out}, indent=2, ensure_ascii=False) + "\n")
    return out


if __name__ == "__main__":
    for r in export():
        print(r["corridor"], r["sendCurrency"], r["providers"], r["usd200"], r["usd500"]["median"])
