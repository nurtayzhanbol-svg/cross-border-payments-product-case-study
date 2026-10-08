"""Phase 5 analysis: invariants and recomputation of headline Wise / zero-fee / panel figures."""
import json
import statistics

import pytest

from rpw import config, phase5

FIG = config.ROOT / "outputs" / "tables" / "phase5" / "phase5_key_figures.json"


@pytest.fixture(scope="module")
def F():
    if not FIG.exists():
        pytest.skip("Run `python -m rpw.phase5` first")
    return json.loads(FIG.read_text())


def test_wise_aliases_merged(long):
    raw = long.loc[long.firm == phase5.WISE, "firm_raw"].str.strip().str.lower().unique()
    assert {"wise", "transferwise"} <= set(raw)
    assert not any("via wise" in r or "wisely" in r for r in raw)


def test_wise_coverage(F, long):
    w = phase5.latest(long)
    assert F["wise"]["latest_window_records"] == w[w.firm == phase5.WISE].record_key.nunique()
    assert F["wise"]["corridors_with_wise"] <= F["wise"]["corridors_total"]


def test_wise_position_recomputed(F, long):
    """Recompute USD 200 median share of cheaper credible quotes without the module's helpers."""
    w = long[long.complete_cost_eligible & long.period.isin(phase5.LATEST_WINDOW) & (long.amount_scenario == "cc1")]
    shares = {}
    for (cor, per), g in w.groupby(["corridor_key", "period"]):
        wq = g[g.firm == "Wise"]
        o = g[(g.firm != "Wise") & (g.total_cost_pct >= 0) & (g.fx_margin_pct >= 0)]
        if len(wq) and len(o):
            shares.setdefault(cor, []).append((o.total_cost_pct < wq.total_cost_pct.median()).mean() * 100)
    per_corridor = [statistics.median(v) for v in shares.values()]
    assert len(per_corridor) == F["wise"]["by_amount"]["usd200"]["corridors"]
    assert round(statistics.median(per_corridor), 1) == F["wise"]["by_amount"]["usd200"]["median_share_cheaper_all"]


def test_position_shares_sum(F):
    for amt in ["usd200", "usd500"]:
        b = F["wise"]["by_amount"][amt]
        assert abs(b["share_corridors_below_median"] + b["share_corridors_above_median"] - 100) < 0.2


def test_zero_fee_cheaper_overall(F):
    for amt in ["usd200", "usd500"]:
        z = F["zero_fee"][amt]
        assert z["zero_fee_median_total"] < z["fee_bearing_median_total"]


def test_panel_accounting(F):
    p = F["panel"]
    assert p["pairs_both"] <= min(p["pairs_start"], p["pairs_end"])
    assert p["survival_share_pct"] == round(p["pairs_both"] / p["pairs_start"] * 100, 1)
    assert p["share_pairs_fell_pct"] + p["share_pairs_rose_pct"] <= 100


def test_sensitivity_specs_present(F):
    specs = F["sensitivity"]["specifications"]
    assert set(specs) == {"baseline_keep_negatives", "drop_negative_total", "drop_negative_total_or_fx",
                          "drop_zero_margin_non_wise_post_2021Q3"}
    assert specs["baseline_keep_negatives"]["median_of_corridor_medians"] == 4.5


def test_docs_cite_current_figures(F):
    text = "\n".join((config.ROOT / "docs" / d).read_text() for d in ["phase5_analysis.md", "case_study_v2.md", "presentation_v2.md"])
    w2, w5 = F["wise"]["by_amount"]["usd200"], F["wise"]["by_amount"]["usd500"]
    cited = [w2["median_wise_total"], w5["median_wise_total"], w2["median_share_cheaper_all"], w2["share_corridors_wise_above_3pct"],
             w5["share_corridors_wise_above_3pct"], F["zero_fee"]["usd200"]["within_corridor"]["share_zero_fee_cheaper"],
             F["panel"]["survival_share_pct"], F["panel"]["pair_change_median_pp"], F["wise"]["implied_fixed_fee_usd_median"]]
    for v in cited:
        assert f"{abs(v):.2f}".rstrip("0").rstrip(".") in text or f"{abs(v):.1f}" in text, v
