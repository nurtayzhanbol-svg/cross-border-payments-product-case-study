"""Checks that figures quoted in the written findings match the generated EDA outputs."""
import json

import pytest

from rpw import config

FIG = config.ROOT / "outputs" / "tables" / "eda" / "eda_key_figures.json"
DOCS = ["eda_findings.md", "case_study.md", "presentation.md", "product_opportunity.md", "prd.md"]


@pytest.fixture(scope="module")
def F():
    if not FIG.exists():
        pytest.skip("Run `python -m rpw.analysis` first")
    return json.loads(FIG.read_text())


@pytest.fixture(scope="module")
def text():
    return "\n".join((config.ROOT / "docs" / d).read_text() for d in DOCS)


def cited(F):
    t, c, a, comp = F["trend"], F["corridors"], F["amounts"], F["composition"]
    return [
        t["median_2016_2Q"], t["median_2025_3Q"], t["panel_median_2016_2Q"], t["panel_median_2025_3Q"], t["mean_2025_3Q"],
        c["share_cheapest_le_3"], c["share_corridor_median_le_3"], c["share_corridor_median_gt_5"], c["median_spread_p10_pp"],
        a["median_total_200"], a["median_total_500"], a["mean_fx_margin_200"], a["mean_fx_margin_500"], a["share_500_cheaper_pct"],
        comp["share_quotes_fx_gt_fee_pct"], comp["zero_fee_mean_fx"], comp["share_zero_fee_quotes"],
        comp["by_provider_type"]["Bank"]["median_total"], comp["by_provider_type"]["Money transfer operator"]["median_total"],
        F["channel_within_corridor"]["share_digital_cheaper_pct"], F["channel_within_corridor"]["median_gap_pp"],
        F["transparency"]["pre_share_undisclosed"], F["transparency"]["post_share_undisclosed"],
    ]


def test_cited_figures_appear_in_docs(F, text):
    missing = [v for v in cited(F) if f"{v:.2f}" not in text and f"{v:.1f}" not in text]
    assert not missing, f"Generated figures not cited as computed: {missing}"


def test_integer_counts(F, text):
    for v in [F["trend"]["panel_pairs"], F["corridors"]["n_corridors"], F["underserved"]["no_quote_le_5"],
              F["underserved"]["no_quote_le_3"], F["underserved"]["no_digital_quote"],
              F["channel_within_corridor"]["corridors_with_both"], F["population"]["complete_cost_eligible_cc1"]]:
        assert f"{v:,}" in text or str(v) in text, v


def test_fx_share_rounding(F, text):
    assert round(F["composition"]["latest_fx_share_pct"]) == 31 and "31%" in text
