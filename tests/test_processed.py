import json

import numpy as np

from rpw import config
from rpw.load import sha256


def test_raw_workbook_unchanged():
    assert sha256() == config.RAW_SHA256


def test_no_rows_dropped(wide, long):
    assert (wide.sheet == "PRE").sum() == config.EXPECTED_ROWS["PRE"]
    assert (wide.sheet == "POST").sum() == config.EXPECTED_ROWS["POST"]
    assert len(long) == 2 * len(wide)
    assert wide.record_key.is_unique
    assert not long.duplicated(["record_key", "amount_scenario"]).any()


def test_manifest_matches(wide):
    m = json.loads((config.PROCESSED_DIR / "manifest.json").read_text())
    assert m["raw_sha256"] == config.RAW_SHA256 and m["rows"]["records_wide"] == len(wide)


def test_periods_and_types(wide):
    assert wide.period.min() == "2011_1Q" and wide.period.max() == "2025_3Q"
    assert "2025_2Q" not in set(wide.period)
    for c in config.NUMERIC_FIELDS:
        assert wide[c].dtype == np.float64, c
    assert wide.collection_date.notna().all()


def test_transparency_flags(wide):
    assert set(wide.transparent_norm) == {"yes", "no"}
    assert wide.flag_fx_undisclosed_by_flag.sum() == 4057 + 3361
    assert not (wide.flag_fx_undisclosed_by_flag & wide.fx_margin_disclosed).any()
    assert wide.loc[wide.period >= "2022_1Q", "flag_fx_undisclosed_by_flag"].sum() == 0
    post_yes_note = (wide.sheet == "POST") & (wide.transparent_norm == "yes") & wide.flag_note_says_not_transparent
    assert post_yes_note.sum() == 282


def test_undisclosed_fx_never_treated_as_complete(long):
    assert not (long.complete_cost_eligible & ~long.fx_margin_disclosed).any()
    assert (long.loc[~long.fx_margin_disclosed, "cost_completeness"] == "fee only or FX margin uncertain").all()


def test_duplicates_flagged_not_removed(wide):
    g = wide.groupby("sheet")
    assert g.flag_duplicate_surplus.sum().to_dict() == {"PRE": 133, "POST": 189}
    assert g.flag_duplicate_except_id.sum().to_dict() == {"PRE": 266, "POST": 372}


def test_cost_identity_on_eligible_quotes(long):
    e = long[long.cost_analysis_eligible]
    assert (e.cost_identity_residual_pp.abs() <= config.COST_TOLERANCE_PP).all()
    assert set(e.denomination_usd.unique()) <= {200.0, 500.0}
    share = long.cost_analysis_eligible.mean()
    assert share > 0.99


def test_raw_values_preserved(wide):
    assert (wide.firm_raw.str.casefold() == "transferwise").sum() > 0
    assert set(wide.loc[wide.firm_raw.str.casefold() == "transferwise", "firm"]) == {"Wise"}
    assert wide.flag_corridor_mismatch.sum() == 95
    assert wide.loc[wide.flag_corridor_mismatch, "destination_code"].eq("KSV").all()
    assert (wide.sending_location_pre == "Not available").sum() == 16559
