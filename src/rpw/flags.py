"""Explicit data-quality flags. Flags describe records; nothing is deleted or corrected."""
import numpy as np
import pandas as pd

from . import config
from .harmonise import DISCLAIMER_RE, NOT_TRANSPARENT_RE

DUP_EXCLUDE = {"record_id", "record_key", "source_row"}


def add_record_flags(df):
    f = df
    f["flag_fx_undisclosed_by_flag"] = f["transparent_norm"].eq("no")
    f["flag_note_says_not_transparent"] = f["note_text"].str.contains(NOT_TRANSPARENT_RE)
    f["flag_note_zero_margin_disclaimer"] = f["note_text"].str.contains(DISCLAIMER_RE)
    f["fx_margin_disclosed"] = f["transparent_norm"].eq("yes") & ~f["flag_note_says_not_transparent"]
    f["transparency_coding_era"] = np.select(
        [f["period"] < "2021_1Q", f["period"] <= "2022_1Q"],
        ["stable (to 2020_4Q)", "transition (2021_1Q-2022_1Q)"], "post-transition (from 2022_2Q)")

    f["flag_interbank_rate_placeholder"] = f["interbank_fx_rate"].isin([0, 1])
    f["flag_corridor_mismatch"] = f["corridor_raw"] != f["corridor_key"]
    f["flag_lcu_code_differs_cc1_cc2"] = f["cc1_lcu_code"].ne(f["cc2_lcu_code"])
    f["flag_any_numeric_parse_failure"] = f[[c for c in f.columns if c.endswith("__parse_failed")]].any(axis=1)
    f["flag_numeric_stored_as_text"] = (f["year"] == 2024) & f["quarter"].isin([3, 4]) & (f["sheet"] == "POST")

    cd = f["collection_date"]
    f["flag_date_unparsed"] = cd.isna()
    f["flag_date_outside_period"] = cd.notna() & ((cd.dt.year != f["year"]) | (cd.dt.quarter != f["quarter"]))

    pre = f["sheet"].eq("PRE")
    f["flag_access_not_collected"] = pre & f["sending_location_pre"].eq("Not available")
    f["flag_pickup_not_collected"] = pre & f["pickup_method_pre"].fillna("").eq("")
    f["flag_income_label_inferred"] = (f["source_income"].eq("Lower income") | f["destination_income"].eq("Lower income"))

    dup_cols = [c for c in f.columns if c not in DUP_EXCLUDE and not c.startswith("flag_")
                and not c.endswith("__parse_failed")]
    key = pd.util.hash_pandas_object(f[dup_cols].astype(str), index=False)
    f["dup_group_size"] = key.groupby(key).transform("size").astype(int)
    f["flag_duplicate_except_id"] = f["dup_group_size"] > 1
    f["flag_duplicate_surplus"] = key.groupby(key).cumcount() > 0
    return f


def to_long(df):
    """One row per record × amount scenario (USD 200 = cc1, USD 500 = cc2)."""
    keep = [c for c in df.columns if not c.startswith(("cc1_", "cc2_")) and not c.endswith("__parse_failed")]
    parts = []
    for cc, usd in config.AMOUNTS.items():
        part = df[keep].copy()
        part.insert(part.columns.get_loc("record_key") + 1, "amount_scenario", cc)
        part.insert(part.columns.get_loc("amount_scenario") + 1, "amount_usd_nominal", usd)
        for src, dst in [("denomination_usd", "denomination_usd"), ("lcu_amount", "lcu_amount"),
                         ("lcu_code", "lcu_code"), ("lcu_fee", "fee_lcu"), ("applied_fx_rate", "applied_fx_rate"),
                         ("fx_margin_pct", "fx_margin_pct"), ("total_cost_pct", "total_cost_pct")]:
            part[dst] = df[f"{cc}_{src}"].values
        parts.append(part)
    q = pd.concat(parts, ignore_index=True)

    amt = q["lcu_amount"].where(q["lcu_amount"] > 0)
    q["fee_pct"] = q["fee_lcu"] / amt * 100
    q["cost_identity_residual_pp"] = q["total_cost_pct"] - (q["fee_pct"] + q["fx_margin_pct"])
    q["flag_cost_identity_fail"] = q["cost_identity_residual_pp"].abs() > config.COST_TOLERANCE_PP
    q["flag_cost_identity_untestable"] = q["cost_identity_residual_pp"].isna()
    q["flag_fee_omitted_from_total"] = ((q["fee_pct"] > config.COST_TOLERANCE_PP)
                                        & ((q["total_cost_pct"] - q["fx_margin_pct"]).abs() <= config.COST_TOLERANCE_PP))
    q["flag_denomination_nonstandard"] = q["denomination_usd"].ne(q["amount_usd_nominal"])
    q["flag_total_cost_missing"] = q["total_cost_pct"].isna()
    q["flag_negative_fx_margin"] = q["fx_margin_pct"] < 0
    q["flag_negative_total_cost"] = q["total_cost_pct"] < 0
    q["flag_extreme_total_cost"] = q["total_cost_pct"] > config.EXTREME_TOTAL_COST_PCT
    q["flag_applied_rate_placeholder"] = q["applied_fx_rate"].isin([0, 1])
    q["flag_zero_margin_undisclosed"] = (~q["fx_margin_disclosed"]) & q["fx_margin_pct"].eq(0)

    q["cost_analysis_eligible"] = ~(q["flag_total_cost_missing"] | q["flag_denomination_nonstandard"]
                                    | q["flag_duplicate_surplus"] | q["flag_cost_identity_fail"]
                                    | q["flag_cost_identity_untestable"])
    q["complete_cost_eligible"] = q["cost_analysis_eligible"] & q["fx_margin_disclosed"]
    q["cost_completeness"] = np.where(q["fx_margin_disclosed"], "fee + disclosed FX margin",
                                      "fee only or FX margin uncertain")
    return q
