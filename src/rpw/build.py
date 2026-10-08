"""Build the processed analytical datasets.

Usage: python -m rpw.build   (with src/ on PYTHONPATH; see README)
"""
import json
import platform
import sys

import pandas as pd

from . import config
from .flags import add_record_flags, to_long
from .harmonise import harmonise
from .load import load_raw, verify_raw


def flag_summary(wide, long):
    rows = []
    for name, frame, grain in [("records", wide, "record"), ("quotes", long, "quote")]:
        for c in [c for c in frame.columns if c.startswith("flag_")] + (
                ["cost_analysis_eligible", "complete_cost_eligible"] if grain == "quote" else ["fx_margin_disclosed"]):
            for sheet, g in frame.groupby("sheet"):
                rows.append({"dataset": name, "flag": c, "sheet": sheet, "rows": len(g),
                             "flagged": int(g[c].fillna(False).astype(bool).sum())})
    out = pd.DataFrame(rows)
    out["share_pct"] = (out["flagged"] / out["rows"] * 100).round(3)
    return out


def build(use_cache=True):
    digest = verify_raw()
    raw = load_raw(use_cache=use_cache)
    wide, pmap = harmonise(raw)
    wide = add_record_flags(wide)
    long = to_long(wide)
    if len(wide) != sum(config.EXPECTED_ROWS.values()) or len(long) != 2 * len(wide):
        raise AssertionError("Row count changed during the pipeline")

    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    wide_out = wide.drop(columns=[c for c in wide.columns if c.endswith("__parse_failed")])
    wide_out.to_parquet(config.PROCESSED_DIR / "rpw_records_wide.parquet", index=False)
    long.to_parquet(config.PROCESSED_DIR / "rpw_quotes_long.parquet", index=False)
    pmap.to_csv(config.PROCESSED_DIR / "provider_name_map.csv", index=False)
    summary = flag_summary(wide, long)
    summary.to_csv(config.PROCESSED_DIR / "data_quality_flag_summary.csv", index=False)
    manifest = {
        "raw_file": config.RAW_WORKBOOK.name, "raw_sha256": digest,
        "rows": {"records_wide": len(wide_out), "quotes_long": len(long),
                 "PRE": int((wide["sheet"] == "PRE").sum()), "POST": int((wide["sheet"] == "POST").sum())},
        "columns": {"records_wide": len(wide_out.columns), "quotes_long": len(long.columns)},
        "python": sys.version.split()[0], "pandas": pd.__version__, "platform": platform.platform(),
    }
    (config.PROCESSED_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    if verify_raw() != digest:
        raise AssertionError("Raw workbook changed during build")
    return wide_out, long, pmap, summary


if __name__ == "__main__":
    w, l, p, s = build(use_cache="--no-cache" not in sys.argv)
    print(f"records_wide: {w.shape}, quotes_long: {l.shape}, providers: {p['firm'].nunique()}")
