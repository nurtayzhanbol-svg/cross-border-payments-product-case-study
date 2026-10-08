"""Exploratory analysis: reproducible tables and charts from data/processed.

Usage: PYTHONPATH=src python -m rpw.analysis
All statistics are descriptive. Quote counts are survey records, not transaction volumes.
"""
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from . import config  # noqa: E402

TABLES = config.ROOT / "outputs" / "tables" / "eda"
CHARTS = config.ROOT / "outputs" / "charts"
LATEST_WINDOW = ["2024_3Q", "2024_4Q", "2025_1Q", "2025_3Q"]
PALETTE = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00", "#F0E442", "#999999"]
SOURCE_NOTE = "Source: World Bank, Remittance Prices Worldwide (2011 Q1–2025 Q3). Survey quotes, unweighted."


def load_quotes():
    return pd.read_parquet(config.PROCESSED_DIR / "rpw_quotes_long.parquet")


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


def complete(q, scenario="cc1"):
    return q[q.complete_cost_eligible & (q.amount_scenario == scenario)]


def trend(q, F):
    c = complete(q)
    by = c.groupby("period").agg(quotes=("total_cost_pct", "size"), corridors=("corridor_key", "nunique"),
                                 mean_total=("total_cost_pct", "mean"), median_total=("total_cost_pct", "median"),
                                 mean_fee=("fee_pct", "mean"), mean_fx=("fx_margin_pct", "mean")).reset_index()
    # Fixed-composition panel: corridor × firm pairs observed in both 2016_2Q and 2025_3Q (POST only).
    post = c[c.sheet == "POST"]
    pairs = post.groupby(["corridor_key", "firm"]).period.agg(set)
    keep = pairs[pairs.map(lambda s: {"2016_2Q", "2025_3Q"} <= s)].index
    panel = post.set_index(["corridor_key", "firm"]).loc[lambda d: d.index.isin(keep)].reset_index()
    pan = panel.groupby("period").agg(panel_pairs=("firm", "size"), panel_median=("total_cost_pct", "median"),
                                      panel_mean=("total_cost_pct", "mean")).reset_index()
    by = by.merge(pan, on="period", how="left")
    _save(by.round(3), "cost_trend_by_period_cc1")
    first, last = by.iloc[0], by.iloc[-1]
    p16, p25 = by.set_index("period").loc["2016_2Q"], by.set_index("period").loc["2025_3Q"]
    F["trend"] = {"first_period": first.period, "first_mean": round(first.mean_total, 2),
                  "mean_2016_2Q": round(p16.mean_total, 2), "mean_2025_3Q": round(p25.mean_total, 2),
                  "median_2016_2Q": round(p16.median_total, 2), "median_2025_3Q": round(p25.median_total, 2),
                  "panel_pairs": int(len(keep)), "panel_median_2016_2Q": round(p16.panel_median, 2),
                  "panel_median_2025_3Q": round(p25.panel_median, 2)}

    fig, ax = plt.subplots(figsize=(10, 4.8))
    x = np.arange(len(by))
    ax.plot(x, by.mean_total, color=PALETTE[0], lw=2, label="Mean, all surveyed quotes")
    ax.plot(x, by.median_total, color=PALETTE[1], lw=2, label="Median, all surveyed quotes")
    ax.plot(x, by.panel_median, color=PALETTE[2], lw=2, ls="--",
            label=f"Median, fixed panel ({len(keep)} corridor×provider pairs, POST)")
    ax.axhline(config.SDG_TARGET_PCT, color="#333", lw=1, ls=":", label="SDG 10.c target (3%)")
    ax.axvline(by.index[by.period == "2016_2Q"][0] - 0.5, color="#999", lw=1)
    ax.text(by.index[by.period == "2016_2Q"][0], ax.get_ylim()[1] * 0.95, " schema change (2016 Q2)", fontsize=8)
    ax.set_xticks(x[::4]); ax.set_xticklabels(by.period[::4], rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Total cost, % of USD 200"); ax.legend(fontsize=8)
    ax.set_title("Surveyed cost of sending USD 200 has fallen, but the median quote is still above 3%")
    _fig("01_cost_trend_cc1", fig)


def corridors(q, F):
    c = complete(q)
    w = c[c.period.isin(LATEST_WINDOW)]
    cor = w.groupby("corridor_key").agg(source_name=("source_name", "last"), destination_name=("destination_name", "last"),
        quotes=("total_cost_pct", "size"), providers=("firm", "nunique"),
        median_total=("total_cost_pct", "median"), min_total=("total_cost_pct", lambda s: s[s >= 0].min()),
        p10=("total_cost_pct", lambda s: s.quantile(.10)),
        max_total=("total_cost_pct", "max"), p25=("total_cost_pct", lambda s: s.quantile(.25)),
        p75=("total_cost_pct", lambda s: s.quantile(.75)),
        share_digital=("access_has_digital", "mean")).reset_index()
    cor["spread_median_minus_p10"] = cor.median_total - cor.p10
    cor = _save(cor.sort_values("median_total", ascending=False).round(3), "corridor_costs_latest_window_cc1")
    F["corridors"] = {"n_corridors": int(len(cor)), "median_of_corridor_medians": round(cor.median_total.median(), 2),
                      "share_corridor_median_gt_5": round((cor.median_total > 5).mean() * 100, 1),
                      "share_corridor_median_le_3": round((cor.median_total <= 3).mean() * 100, 1),
                      "share_cheapest_le_3": round((cor.min_total <= 3).mean() * 100, 1),
                      "median_spread_p10_pp": round(cor.spread_median_minus_p10.median(), 2)}

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.hist(cor.median_total.clip(upper=20), bins=40, color=PALETTE[0], alpha=.85, label="Median quote")
    ax.hist(cor.min_total.clip(upper=20), bins=40, color=PALETTE[1], alpha=.6, label="Cheapest quote")
    for v, lbl in [(3, "3% SDG"), (5, "5% G20")]:
        ax.axvline(v, color="#333", ls=":", lw=1); ax.text(v, ax.get_ylim()[1] * .9, f" {lbl}", fontsize=8)
    ax.set_xlabel("Total cost, % of USD 200 (clipped at 20%)"); ax.set_ylabel("Corridors")
    ax.set_title(f"Corridors, latest 4 surveyed quarters: median vs cheapest surveyed quote (n={len(cor)})")
    ax.legend(fontsize=8)
    _fig("02_corridor_cost_distribution", fig)


def amounts(q, F):
    c = q[q.complete_cost_eligible & q.period.isin(LATEST_WINDOW)]
    p = c.pivot_table(index="record_key", columns="amount_scenario", values=["total_cost_pct", "fee_pct", "fx_margin_pct"])
    p = p.dropna()
    t = pd.DataFrame({"scenario": ["USD 200 (cc1)", "USD 500 (cc2)"],
                      "median_total": [p.total_cost_pct.cc1.median(), p.total_cost_pct.cc2.median()],
                      "mean_total": [p.total_cost_pct.cc1.mean(), p.total_cost_pct.cc2.mean()],
                      "mean_fee_pct": [p.fee_pct.cc1.mean(), p.fee_pct.cc2.mean()],
                      "mean_fx_margin": [p.fx_margin_pct.cc1.mean(), p.fx_margin_pct.cc2.mean()]})
    t["paired_records"] = len(p)
    _save(t.round(3), "amount_comparison_latest_window")
    F["amounts"] = {"paired": int(len(p)), **{f"{k}_{s}": round(v, 2) for s, r in zip(["200", "500"], t.to_dict("records"))
                                              for k, v in r.items() if k.startswith(("median", "mean"))},
                    "share_500_cheaper_pct": round((p.total_cost_pct.cc2 < p.total_cost_pct.cc1).mean() * 100, 1)}


def composition(q, F):
    c = complete(q)
    c = c.assign(window=np.where(c.period.isin(LATEST_WINDOW), "latest", "other"))
    g = c.groupby(["provider_type"]).agg(quotes=("fee_pct", "size")).reset_index()
    lat = c[c.window == "latest"].groupby("provider_type").agg(
        quotes=("fee_pct", "size"), mean_fee_pct=("fee_pct", "mean"), mean_fx_margin=("fx_margin_pct", "mean"),
        median_total=("total_cost_pct", "median"), median_fee_pct=("fee_pct", "median"),
        median_fx_margin=("fx_margin_pct", "median"), share_zero_fee=("fee_lcu", lambda s: (s == 0).mean())).reset_index()
    lat["fx_share_of_cost"] = lat.mean_fx_margin / (lat.mean_fee_pct + lat.mean_fx_margin)
    lat = _save(lat.sort_values("quotes", ascending=False).round(3), "provider_type_costs_latest_window_cc1")
    del g
    by = c.groupby("year").agg(mean_fee=("fee_pct", "mean"), mean_fx=("fx_margin_pct", "mean")).reset_index()
    by["fx_share"] = by.mean_fx / (by.mean_fee + by.mean_fx)
    _save(by.round(3), "fee_fx_composition_by_year_cc1")
    lw = c[c.window == "latest"]
    F["composition"] = {"latest_mean_fee_pct": round(lw.fee_pct.mean(), 2), "latest_mean_fx": round(lw.fx_margin_pct.mean(), 2),
                        "latest_fx_share_pct": round(lw.fx_margin_pct.mean() / lw.total_cost_pct.mean() * 100, 1),
                        "latest_median_fee_pct": round(lw.fee_pct.median(), 2), "latest_median_fx": round(lw.fx_margin_pct.median(), 2),
                        "share_quotes_fx_gt_fee_pct": round((lw.fx_margin_pct > lw.fee_pct).mean() * 100, 1),
                        "share_zero_fee_quotes": round((lw.fee_lcu == 0).mean() * 100, 1),
                        "zero_fee_mean_fx": round(lw[lw.fee_lcu == 0].fx_margin_pct.mean(), 2),
                        "fee_bearing_mean_fx": round(lw[lw.fee_lcu > 0].fx_margin_pct.mean(), 2),
                        "zero_fee_median_total": round(lw[lw.fee_lcu == 0].total_cost_pct.median(), 2),
                        "fee_bearing_median_total": round(lw[lw.fee_lcu > 0].total_cost_pct.median(), 2),
                        "by_provider_type": lat.set_index("provider_type")[["quotes", "median_total", "median_fee_pct", "median_fx_margin", "mean_fee_pct", "mean_fx_margin"]].round(2).to_dict("index")}

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    ax[0].bar(by.year, by.mean_fee, color=PALETTE[0], label="Fee (% of amount)")
    ax[0].bar(by.year, by.mean_fx, bottom=by.mean_fee, color=PALETTE[1], label="FX margin (%)")
    ax[0].set_title("Mean cost composition by year, USD 200"); ax[0].legend(fontsize=8); ax[0].set_ylabel("%")
    lat2 = lat[lat.quotes >= 200]
    ax[1].barh(lat2.provider_type, lat2.median_fee_pct, color=PALETTE[0], label="Fee")
    ax[1].barh(lat2.provider_type, lat2.median_fx_margin, left=lat2.median_fee_pct, color=PALETTE[1], label="FX margin")
    ax[1].set_title("Latest 4 quarters, medians by provider type (≥200 quotes)"); ax[1].set_xlabel("% of USD 200")
    fig.suptitle("FX margin is a large part of total cost — and it is the part senders see least clearly", fontsize=11)
    _fig("03_fee_vs_fx_composition", fig)


def access_channel(q, F):
    c = complete(q)
    lw = c[c.period.isin(LATEST_WINDOW) & c.access_has_digital.notna()]
    lw = lw.assign(channel=np.where(lw.access_digital_only, "Digital only",
                                    np.where(lw.access_has_digital, "Digital + physical", "Physical only")))
    t = lw.groupby("channel").agg(quotes=("total_cost_pct", "size"), median_total=("total_cost_pct", "median"),
                                  mean_fee=("fee_pct", "mean"), mean_fx=("fx_margin_pct", "mean")).reset_index()
    _save(t.round(3), "access_channel_costs_latest_window_cc1")
    # Within-corridor comparison: corridors where both digital-only and physical-only quotes exist.
    m = lw[lw.channel != "Digital + physical"].groupby(["corridor_key", "channel"]).total_cost_pct.median().unstack()
    m = m.dropna()
    m["gap_pp"] = m["Physical only"] - m["Digital only"]
    _save(m.reset_index().round(3), "within_corridor_digital_vs_physical_latest_window_cc1")
    F["channel"] = t.set_index("channel").round(2).to_dict("index")
    F["channel_within_corridor"] = {"corridors_with_both": int(len(m)), "median_gap_pp": round(m.gap_pp.median(), 2),
                                    "share_digital_cheaper_pct": round((m.gap_pp > 0).mean() * 100, 1)}


def transparency(q, F):
    r = q[q.amount_scenario == "cc1"]
    t = r.groupby(["period", "transparency_coding_era"]).agg(
        quotes=("record_key", "size"), flag_no=("flag_fx_undisclosed_by_flag", "mean"),
        note_not_transparent=("flag_note_says_not_transparent", "mean"),
        margin_not_disclosed=("fx_margin_disclosed", lambda s: 1 - s.mean()),
        complete_cost_eligible=("complete_cost_eligible", "mean")).reset_index()
    _save(t.round(4), "transparency_by_period")
    F["transparency"] = {"pre_share_undisclosed": round((~r[r.sheet == "PRE"].fx_margin_disclosed).mean() * 100, 1),
                         "post_share_undisclosed": round((~r[r.sheet == "POST"].fx_margin_disclosed).mean() * 100, 1),
                         "complete_eligible_pct": round(r.complete_cost_eligible.mean() * 100, 1)}
    fig, ax = plt.subplots(figsize=(10, 4))
    x = np.arange(len(t))
    ax.plot(x, t.flag_no * 100, color=PALETTE[5], lw=2, label="transparent = no")
    ax.plot(x, t.note_not_transparent * 100, color=PALETTE[3], lw=2, ls="--", label="note says 'not transparent'")
    ax.set_xticks(x[::4]); ax.set_xticklabels(t.period[::4], rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("% of surveyed records"); ax.legend(fontsize=8)
    ax.set_title("The 'transparent' flag disappears after 2021 while notes still describe non-transparent services")
    _fig("04_transparency_coding", fig)


def markets(q, F):
    c = complete(q)
    w = c[c.period.isin(LATEST_WINDOW)]
    s = w.groupby("source_name").agg(quotes=("total_cost_pct", "size"), corridors=("corridor_key", "nunique"),
                                     median_total=("total_cost_pct", "median")).reset_index()
    d = w.groupby("destination_region").agg(quotes=("total_cost_pct", "size"), corridors=("corridor_key", "nunique"),
                                            median_total=("total_cost_pct", "median"),
                                            mean_fx=("fx_margin_pct", "mean")).reset_index()
    _save(s.sort_values("median_total").round(3), "sending_market_costs_latest_window_cc1")
    d = _save(d.sort_values("median_total").round(3), "receiving_region_costs_latest_window_cc1")
    F["markets"] = {"n_sending": int(len(s)), "cheapest_sending": s.nsmallest(3, "median_total").source_name.tolist(),
                    "dearest_sending": s.nlargest(3, "median_total").source_name.tolist(),
                    "region": d.set_index("destination_region").median_total.round(2).to_dict()}
    fig, ax = plt.subplots(figsize=(9, 4.5))
    d2 = d[d.destination_region != ".."]
    ax.barh(d2.destination_region, d2.median_total, color=PALETTE[0])
    ax.axvline(3, color="#333", ls=":"); ax.set_xlabel("Median total cost, % of USD 200")
    ax.set_title("Receiving region: median surveyed quote, latest 4 quarters")
    _fig("05_receiving_region_costs", fig)


def underserved(q, F):
    c = complete(q)
    w = c[c.period.isin(LATEST_WINDOW)]
    cor = w.groupby("corridor_key").agg(source_name=("source_name", "last"), destination_name=("destination_name", "last"), destination_region=("destination_region", "last"),
        providers=("firm", "nunique"), quotes=("total_cost_pct", "size"),
        min_total=("total_cost_pct", lambda s: s[s >= 0].min()), p10=("total_cost_pct", lambda s: s.quantile(.10)),
        median_total=("total_cost_pct", "median"), digital_quotes=("access_has_digital", "sum")).reset_index()
    best_digital = w[w.access_has_digital == True].groupby("corridor_key").total_cost_pct.min()  # noqa: E712
    cor["min_digital_total"] = cor.corridor_key.map(best_digital)
    cor["no_quote_le_3pct"] = cor.min_total > 3
    cor["no_quote_le_5pct"] = cor.min_total > 5
    cor["savings_median_to_p10_pp"] = cor.median_total - cor.p10
    cor = cor.reset_index().drop(columns="index", errors="ignore").sort_values(["no_quote_le_5pct", "min_total"], ascending=False)
    _save(cor.round(3), "underserved_corridor_screen_latest_window_cc1")
    F["underserved"] = {"corridors": int(len(cor)), "no_quote_le_3": int(cor.no_quote_le_3pct.sum()),
                        "no_quote_le_5": int(cor.no_quote_le_5pct.sum()),
                        "no_digital_quote": int((cor.digital_quotes == 0).sum()),
                        "top_no_quote_le_5": cor[cor.no_quote_le_5pct].head(10)[["corridor_key", "min_total"]].round(2).values.tolist(),
                        "share_corridors_gap_ge_2pp": round((cor.savings_median_to_p10_pp >= 2).mean() * 100, 1),
                        "median_gap_median_to_p10_pp": round(cor.savings_median_to_p10_pp.median(), 2),
                        "negative_total_quotes_excluded_from_cheapest": int((w.total_cost_pct < 0).sum())}
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.scatter(cor.p10.clip(-1, 25), cor.savings_median_to_p10_pp.clip(upper=25), s=10 + cor.providers * 4,
               alpha=.5, color=PALETTE[0], edgecolor="none")
    ax.axvline(3, color="#333", ls=":"); ax.axvline(5, color="#333", ls=":")
    ax.set_xlabel("10th-percentile quote in corridor, % (clipped to [-1, 25])")
    ax.set_ylabel("Median − 10th percentile, pp (clipped 25)")
    ax.set_title("Price dispersion: in most corridors the typical quote costs well above the low end")
    _fig("06_corridor_dispersion", fig)


def run():
    q = load_quotes()
    F = {"population": {"quotes_total": int(len(q)), "complete_cost_eligible_cc1": int(complete(q).shape[0]),
                        "latest_window": LATEST_WINDOW}}
    for fn in (trend, corridors, amounts, composition, access_channel, transparency, markets, underserved):
        fn(q, F)
    (TABLES / "eda_key_figures.json").write_text(json.dumps(F, indent=2, default=str) + "\n")
    return F


if __name__ == "__main__":
    print(json.dumps(run(), indent=1, default=str))
