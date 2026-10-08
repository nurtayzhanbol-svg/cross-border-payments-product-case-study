"""Phase 5 analysis: Wise position, corrected zero-fee and panel analyses, sensitivities.

Usage: PYTHONPATH=src python -m rpw.phase5
Writes outputs/tables/phase5/*.csv, phase5_key_figures.json and outputs/charts/p5_*.png.
The original EDA (rpw.analysis) is left unchanged so both sets of results stay comparable.
All statistics are unweighted survey statistics. Quote counts are not volumes or market share.
"""
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from . import config  # noqa: E402
from .analysis import LATEST_WINDOW, SOURCE_NOTE, load_quotes  # noqa: E402

TABLES = config.ROOT / "outputs" / "tables" / "phase5"
CHARTS = config.ROOT / "outputs" / "charts"
WISE = "Wise"
AMOUNT = {"cc1": 200, "cc2": 500}
LOW_COST_PCT = 3.0


def _save(df, name):
    TABLES.mkdir(parents=True, exist_ok=True)
    df.to_csv(TABLES / f"{name}.csv", index=False)
    return df


def _fig(name, fig):
    CHARTS.mkdir(parents=True, exist_ok=True)
    fig.text(0.01, 0.005, SOURCE_NOTE, fontsize=7, color="#555")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(CHARTS / f"{name}.png", dpi=150)
    plt.close(fig)


def r(x, d=2):
    return None if pd.isna(x) else round(float(x), d)


def latest(q):
    return q[q.complete_cost_eligible & q.period.isin(LATEST_WINDOW)].copy()


def credible(df):
    """Quotes usable as a 'real alternative': non-negative total cost and FX margin."""
    return df[(df.total_cost_pct >= 0) & (df.fx_margin_pct >= 0)]


def like_for_like(df):
    """Alternatives comparable to Wise's surveyed service: digital access and bank-account payout."""
    return df[df.access_has_digital.eq(True) & df.payout_method_group.eq("bank account")]


# ---------------------------------------------------------------- A1 Wise
def wise_position(q, F):
    w = latest(q)
    rows = []
    for (cor, per, sc), g in w.groupby(["corridor_key", "period", "amount_scenario"]):
        wq = g[g.firm == WISE]
        if wq.empty:
            continue
        others = credible(g[g.firm != WISE])
        lfl = like_for_like(others)
        wt = wq.total_cost_pct.median()
        rows.append({
            "corridor_key": cor, "period": per, "amount_scenario": sc,
            "source_code": g.source_code.iloc[0], "destination_code": g.destination_code.iloc[0],
            "destination_region": g.destination_region.iloc[0],
            "wise_quotes": len(wq), "wise_total": wt,
            "wise_fee_pct": wq.fee_pct.median(), "wise_fx": wq.fx_margin_pct.median(),
            "other_quotes": len(others), "other_providers": others.firm.nunique(),
            "other_median": others.total_cost_pct.median(),
            "other_min": others.total_cost_pct.min(),
            "other_p10": others.total_cost_pct.quantile(.10) if len(others) else np.nan,
            "share_cheaper_all": (others.total_cost_pct < wt).mean() * 100 if len(others) else np.nan,
            "lfl_quotes": len(lfl),
            "lfl_median": lfl.total_cost_pct.median(),
            "share_cheaper_lfl": (lfl.total_cost_pct < wt).mean() * 100 if len(lfl) else np.nan,
            "cheapest_alt_firm": others.loc[others.total_cost_pct.idxmin(), "firm"] if len(others) else None,
            "cheapest_alt_type": others.loc[others.total_cost_pct.idxmin(), "provider_type"] if len(others) else None,
            "cheapest_alt_payout": others.loc[others.total_cost_pct.idxmin(), "payout_method_group"] if len(others) else None,
            "cheaper_alt_fee_zero_share": (others[others.total_cost_pct < wt].fee_lcu.eq(0).mean() * 100)
            if (others.total_cost_pct < wt).any() else np.nan,
        })
    cp = pd.DataFrame(rows)
    cp["gap_vs_median_pp"] = cp.wise_total - cp.other_median
    cp["gap_vs_min_pp"] = cp.wise_total - cp.other_min
    cp["gap_vs_p10_pp"] = cp.wise_total - cp.other_p10
    _save(cp, "wise_corridor_period_position")

    cor = cp.groupby(["corridor_key", "amount_scenario"]).agg(
        source_code=("source_code", "first"), destination_code=("destination_code", "first"),
        destination_region=("destination_region", "first"), periods=("period", "nunique"),
        wise_total=("wise_total", "median"), wise_fee_pct=("wise_fee_pct", "median"), wise_fx=("wise_fx", "median"),
        other_median=("other_median", "median"), other_providers=("other_providers", "median"),
        share_cheaper_all=("share_cheaper_all", "median"), share_cheaper_lfl=("share_cheaper_lfl", "median"),
        gap_vs_median_pp=("gap_vs_median_pp", "median"), gap_vs_min_pp=("gap_vs_min_pp", "median"),
        gap_vs_p10_pp=("gap_vs_p10_pp", "median"),
    ).reset_index()
    cor["position"] = np.select(
        [cor.share_cheaper_all <= 10, cor.share_cheaper_all <= 50, cor.share_cheaper_all.notna()],
        ["top decile", "cheaper than median", "more expensive than median"], "no comparison")
    _save(cor, "wise_corridor_position_latest_window")

    # Implied fee schedule from the two surveyed amounts (fee = fixed + variable × amount).
    ww = w[w.firm == WISE].pivot_table(index="record_key", columns="amount_scenario",
                                       values=["fee_lcu", "lcu_amount", "fx_margin_pct", "total_cost_pct"]).dropna()
    slope = (ww.fee_lcu.cc2 - ww.fee_lcu.cc1) / (ww.lcu_amount.cc2 - ww.lcu_amount.cc1)
    fixed_lcu = ww.fee_lcu.cc1 - slope * ww.lcu_amount.cc1
    fees = pd.DataFrame({"variable_pct": slope * 100, "fixed_usd_equiv": fixed_lcu / ww.lcu_amount.cc1 * 200,
                         "total_200": ww.total_cost_pct.cc1, "total_500": ww.total_cost_pct.cc2})
    _save(fees.reset_index(), "wise_implied_fee_schedule")

    by_amt = {}
    for sc in ["cc1", "cc2"]:
        c = cor[cor.amount_scenario == sc]
        by_amt[f"usd{AMOUNT[sc]}"] = {
            "corridors": int(len(c)),
            "median_wise_total": r(c.wise_total.median()),
            "median_wise_fee_pct": r(c.wise_fee_pct.median()),
            "median_wise_fx": r(c.wise_fx.median()),
            "median_share_cheaper_all": r(c.share_cheaper_all.median(), 1),
            "median_share_cheaper_lfl": r(c.share_cheaper_lfl.median(), 1),
            "median_gap_vs_median_pp": r(c.gap_vs_median_pp.median()),
            "median_gap_vs_p10_pp": r(c.gap_vs_p10_pp.median()),
            "median_gap_vs_min_pp": r(c.gap_vs_min_pp.median()),
            "share_corridors_top_decile": r((c.position == "top decile").mean() * 100, 1),
            "share_corridors_below_median": r((c.share_cheaper_all <= 50).mean() * 100, 1),
            "share_corridors_above_median": r((c.share_cheaper_all > 50).mean() * 100, 1),
            "share_corridors_wise_above_3pct": r((c.wise_total > LOW_COST_PCT).mean() * 100, 1),
        }
    cheaper = cp[cp.amount_scenario == "cc1"]
    alt = w[(w.firm != WISE)].merge(cheaper[["corridor_key", "period", "wise_total"]], on=["corridor_key", "period"])
    alt = credible(alt[alt.amount_scenario == "cc1"])
    alt = alt[alt.total_cost_pct < alt.wise_total]
    alt_types = alt.provider_type.value_counts(normalize=True).mul(100).round(1)
    alt_payout = alt.payout_method_group.value_counts(normalize=True).mul(100).round(1)
    _save(alt.groupby("firm").size().sort_values(ascending=False).head(25).rename("quotes_cheaper_than_wise_usd200")
          .reset_index(), "providers_cheaper_than_wise_usd200")
    srcs = cor[cor.amount_scenario == "cc1"].groupby("source_code").agg(
        corridors=("corridor_key", "size"), median_wise_total=("wise_total", "median"),
        median_share_cheaper=("share_cheaper_all", "median"), median_gap_vs_median=("gap_vs_median_pp", "median"),
    ).reset_index().sort_values("corridors", ascending=False)
    _save(srcs, "wise_by_sending_market_usd200")

    all_cor = w.corridor_key.nunique()
    F["wise"] = {
        "provider_names_mapped": ["Wise", "TransferWise"],
        "latest_window_quotes": int((w.firm == WISE).sum()),
        "latest_window_records": int(w[w.firm == WISE].record_key.nunique()),
        "corridors_with_wise": int(w[w.firm == WISE].corridor_key.nunique()),
        "corridors_total": int(all_cor),
        "sending_markets_with_wise": int(w[w.firm == WISE].source_code.nunique()),
        "payout_groups": w[(w.firm == WISE) & (w.amount_scenario == "cc1")].payout_method_group.value_counts().to_dict(),
        "by_amount": by_amt,
        "implied_variable_fee_pct_median": r(fees.variable_pct.median()),
        "implied_fixed_fee_usd_median": r(fees.fixed_usd_equiv.median()),
        "fx_margin_le_0_5_share": r((w[w.firm == WISE].fx_margin_pct <= 0.5).mean() * 100, 1),
        "cheaper_alternatives_usd200": {
            "quotes": int(len(alt)),
            "provider_type_share": alt_types.to_dict(),
            "payout_share": alt_payout.to_dict(),
            "zero_fee_share": r(alt.fee_lcu.eq(0).mean() * 100, 1),
            "median_fx_margin": r(alt.fx_margin_pct.median()),
            "median_fee_pct": r(alt.fee_pct.median()),
        },
    }

    c1 = cor[cor.amount_scenario == "cc1"].sort_values("share_cheaper_all")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.hist(c1.share_cheaper_all.dropna(), bins=20, color="#0072B2")
    ax.axvline(50, color="#D55E00", ls="--", lw=1)
    ax.set_xlabel("Share of other surveyed quotes in the same corridor and quarter cheaper than Wise (%)")
    ax.set_ylabel("Corridors")
    ax.set_title("Wise's position within corridors, USD 200, latest four surveyed quarters")
    _fig("p5_01_wise_position_usd200", fig)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    for sc, col in [("cc1", "#0072B2"), ("cc2", "#E69F00")]:
        c = cor[cor.amount_scenario == sc]
        ax.scatter(c.other_median, c.wise_total, s=12, alpha=.7, color=col, label=f"USD {AMOUNT[sc]}")
    lim = [0, 12]
    ax.plot(lim, lim, color="#999", lw=1)
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_xlabel("Median of other providers in the corridor (% total cost)")
    ax.set_ylabel("Wise (% total cost)")
    ax.set_title("Wise vs corridor median by amount (points below the line: Wise cheaper)")
    ax.legend()
    _fig("p5_02_wise_vs_corridor_median", fig)
    return cor


# ---------------------------------------------------------------- A2 zero fee
def zero_fee(q, F):
    w = latest(q)
    out = {}
    rows = []
    for sc in ["cc1", "cc2"]:
        s = w[w.amount_scenario == sc]
        z, f = s[s.fee_lcu == 0], s[s.fee_lcu > 0]
        out[f"usd{AMOUNT[sc]}"] = {
            "zero_fee_share": r(len(z) / len(s) * 100, 1),
            "zero_fee_median_total": r(z.total_cost_pct.median()), "fee_bearing_median_total": r(f.total_cost_pct.median()),
            "zero_fee_mean_total": r(z.total_cost_pct.mean()), "fee_bearing_mean_total": r(f.total_cost_pct.mean()),
            "zero_fee_median_fx": r(z.fx_margin_pct.median()), "fee_bearing_median_fx": r(f.fx_margin_pct.median()),
            "zero_fee_mean_fx": r(z.fx_margin_pct.mean()), "fee_bearing_mean_fx": r(f.fx_margin_pct.mean()),
        }
        g = s.assign(zf=s.fee_lcu.eq(0)).groupby(["corridor_key", "zf"]).total_cost_pct.median().unstack().dropna()
        g.columns = ["fee_bearing", "zero_fee"]
        out[f"usd{AMOUNT[sc]}"]["within_corridor"] = {
            "corridors_with_both": int(len(g)),
            "share_zero_fee_cheaper": r((g.zero_fee < g.fee_bearing).mean() * 100, 1),
            "median_gap_pp": r((g.zero_fee - g.fee_bearing).median()),
        }
        rows.append(g.reset_index().assign(amount_scenario=sc))
    _save(pd.concat(rows), "zero_fee_vs_fee_bearing_within_corridor")
    F["zero_fee"] = out


# ---------------------------------------------------------------- A3 panel
def panel(q, F):
    c = q[q.complete_cost_eligible & (q.amount_scenario == "cc1") & (q.sheet == "POST")]
    pp = c.groupby(["corridor_key", "firm", "period"]).total_cost_pct.median().rename("med").reset_index()
    start, end = "2016_2Q", "2025_3Q"
    s = pp[pp.period == start].set_index(["corridor_key", "firm"]).med
    e = pp[pp.period == end].set_index(["corridor_key", "firm"]).med
    both = s.index.intersection(e.index)
    exiters, entrants = s.index.difference(e.index), e.index.difference(s.index)
    pair = pd.DataFrame({"start": s.loc[both], "end": e.loc[both]})
    pair["change_pp"] = pair.end - pair.start
    _save(pair.reset_index(), "panel_pair_level_2016Q2_2025Q3")
    cs_start, cs_end = c[c.period == start].total_cost_pct.median(), c[c.period == end].total_cost_pct.median()
    F["panel"] = {
        "unit": "median USD 200 total cost per corridor × canonical provider × period",
        "cross_section_median_start": r(cs_start), "cross_section_median_end": r(cs_end),
        "pairs_start": int(len(s)), "pairs_end": int(len(e)), "pairs_both": int(len(both)),
        "survival_share_pct": r(len(both) / len(s) * 100, 1),
        "survivors_start_median": r(s.loc[both].median()), "exiters_start_median": r(s.loc[exiters].median()),
        "entrants_end_median": r(e.loc[entrants].median()), "survivors_end_median": r(e.loc[both].median()),
        "pair_change_median_pp": r(pair.change_pp.median()), "pair_change_mean_pp": r(pair.change_pp.mean()),
        "share_pairs_fell_pct": r((pair.change_pp < 0).mean() * 100, 1),
        "share_pairs_rose_pct": r((pair.change_pp > 0).mean() * 100, 1),
        "pair_level_median_start": r(pair.start.median()), "pair_level_median_end": r(pair.end.median()),
    }
    yearly = pp[pp.period.str.endswith("3Q") | (pp.period == start)]
    trend = []
    for per, g in yearly.groupby("period"):
        k = g.set_index(["corridor_key", "firm"]).med
        trend.append({"period": per, "pairs": len(k), "median_all_pairs": k.median(),
                      "median_panel_pairs": k[k.index.isin(both)].median(),
                      "panel_pairs_present": int(k.index.isin(both).sum())})
    t = _save(pd.DataFrame(trend), "panel_vs_cross_section_by_year")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(t.period, t.median_all_pairs, marker="o", label="All corridor × provider pairs present that quarter")
    ax.plot(t.period, t.median_panel_pairs, marker="o", label=f"Pairs present in both {start} and {end} ({len(both)})")
    ax.set_ylabel("Median of pair medians, USD 200 (%)")
    ax.set_title("Cost trend: full cross-section vs survivor pairs (one value per pair per quarter)")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(fontsize=8)
    _fig("p5_03_panel_vs_cross_section", fig)


# ---------------------------------------------------------------- A4-A6 sensitivity
def _corridor_stats(w):
    g = w.groupby("corridor_key").total_cost_pct
    med, p10 = g.median(), g.quantile(.10)
    nn = w[w.total_cost_pct >= 0].groupby("corridor_key").total_cost_pct.min()
    return med, p10, nn


def sensitivity(q, F):
    w = latest(q)
    c1 = w[w.amount_scenario == "cc1"]
    post21 = c1.period >= "2021_3Q"
    specs = {
        "baseline_keep_negatives": c1,
        "drop_negative_total": c1[c1.total_cost_pct >= 0],
        "drop_negative_total_or_fx": c1[(c1.total_cost_pct >= 0) & (c1.fx_margin_pct >= 0)],
        "drop_zero_margin_non_wise_post_2021Q3": c1[~(post21 & c1.fx_margin_pct.eq(0) & c1.firm.ne(WISE))],
    }
    rows = []
    for name, s in specs.items():
        med, p10, mn = _corridor_stats(s)
        cq = s[s.total_cost_pct >= 0].groupby(["corridor_key", "period"]).total_cost_pct.min()
        rows.append({
            "specification": name, "quotes": len(s), "corridors": int(s.corridor_key.nunique()),
            "median_of_corridor_medians": r(med.median()),
            "median_gap_median_minus_p10_pp": r((med - p10).median()),
            "share_corridors_min_le_3_pooled": r((mn <= LOW_COST_PCT).mean() * 100, 1),
            "share_corridor_quarters_min_le_3": r((cq <= LOW_COST_PCT).mean() * 100, 1),
            "share_corridors_p10_le_3": r((p10 <= LOW_COST_PCT).mean() * 100, 1),
            "fx_share_of_mean_cost_pct": r(s.fx_margin_pct.mean() / (s.fx_margin_pct.mean() + s.fee_pct.mean()) * 100, 1),
            "share_fx_gt_fee_pct": r((s.fx_margin_pct > s.fee_pct).mean() * 100, 1),
            "zero_fee_median_total": r(s[s.fee_lcu == 0].total_cost_pct.median()),
            "fee_bearing_median_total": r(s[s.fee_lcu > 0].total_cost_pct.median()),
        })
    t = _save(pd.DataFrame(rows), "sensitivity_specifications_usd200")
    big = c1.groupby("corridor_key").filter(lambda g: len(g) >= 20)
    _, p10b, mnb = _corridor_stats(big)
    zero_yes = q[(q.amount_scenario == "cc1") & (q.sheet == "POST") & q.transparent_norm.eq("yes")]
    zy = zero_yes.groupby("year").fx_margin_pct.apply(lambda s: (s == 0).mean() * 100).round(1)
    zy_nw = zero_yes[zero_yes.firm != WISE].groupby("year").fx_margin_pct.apply(lambda s: (s == 0).mean() * 100).round(1)
    _save(pd.DataFrame({"year": zy.index, "zero_margin_share_all": zy.values,
                        "zero_margin_share_excl_wise": zy_nw.reindex(zy.index).values}), "zero_margin_share_transparent_yes_by_year")
    F["sensitivity"] = {
        "specifications": t.set_index("specification").to_dict("index"),
        "corridors_ge_20_quotes": int(big.corridor_key.nunique()),
        "share_min_le_3_ge20": r((mnb <= LOW_COST_PCT).mean() * 100, 1),
        "share_p10_le_3_ge20": r((p10b <= LOW_COST_PCT).mean() * 100, 1),
        "zero_margin_share_yes_by_year": {int(k): v for k, v in zy.items()},
        "zero_margin_share_yes_by_year_excl_wise": {int(k): v for k, v in zy_nw.items()},
    }


# ---------------------------------------------------------------- Opportunity screens
def opportunity_screens(q, F):
    """Descriptive screens used to compare candidate opportunities (not product evidence on their own)."""
    w = latest(q)
    c1 = w[w.amount_scenario == "cc1"]
    wise_cor = set(c1[c1.firm == WISE].corridor_key)
    src_with_wise = set(c1[c1.firm == WISE].source_code)
    cor = c1.groupby("corridor_key").agg(
        source_code=("source_code", "first"), destination_code=("destination_code", "first"),
        destination_region=("destination_region", "first"), quotes=("total_cost_pct", "size"),
        median_total=("total_cost_pct", "median"),
        share_cash=("payout_method_group", lambda s: (s == "cash").mean() * 100),
        share_wallet=("payout_method_group", lambda s: (s == "mobile wallet").mean() * 100),
        share_bank=("payout_method_group", lambda s: (s == "bank account").mean() * 100),
    ).reset_index()
    cor["wise_surveyed"] = cor.corridor_key.isin(wise_cor)
    cor["source_has_wise"] = cor.source_code.isin(src_with_wise)
    _save(cor, "corridor_opportunity_screen_usd200")
    pay = c1.groupby("payout_method_group").total_cost_pct.agg(["size", "median"]).reset_index()
    _save(pay, "cost_by_payout_method_usd200")
    nw = cor[cor.source_has_wise & ~cor.wise_surveyed]
    F["opportunity_screens"] = {
        "corridors": int(len(cor)), "wise_surveyed": int(cor.wise_surveyed.sum()),
        "corridors_from_wise_sending_markets_without_wise_quote": int(len(nw)),
        "median_total_without_wise_from_wise_markets": r(nw.median_total.median()),
        "median_cash_share_without_wise": r(nw.share_cash.median(), 1),
        "median_cash_share_with_wise": r(cor[cor.wise_surveyed].share_cash.median(), 1),
        "median_wallet_share_without_wise": r(nw.share_wallet.median(), 1),
        "payout_method_medians": {k: {"quotes": int(a), "median": r(b)} for k, a, b in pay.itertuples(index=False)},
    }


def run():
    q = load_quotes()
    F = {"window": LATEST_WINDOW, "notes": "Unweighted survey statistics; quote counts are not volumes."}
    wise_position(q, F)
    zero_fee(q, F)
    panel(q, F)
    sensitivity(q, F)
    opportunity_screens(q, F)
    (TABLES / "phase5_key_figures.json").write_text(json.dumps(F, indent=2, default=str))
    return F


if __name__ == "__main__":
    print(json.dumps(run(), indent=1, default=str))
