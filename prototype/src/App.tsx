import { useEffect, useMemo, useState } from "react";
import { BENCHMARK_META, CORRIDORS, MAX_AMOUNT, MIN_AMOUNT, benchmarkFor, position, quote } from "./pricing";

const fmt = (v: number, cur: string, d = 2) =>
  new Intl.NumberFormat("en-GB", { style: "currency", currency: cur, maximumFractionDigits: d }).format(v);
const pct = (v: number) => `${v.toFixed(2)}%`;

const POSITION_TEXT = {
  "below-p10": "Lower than 90% of surveyed quotes for this corridor",
  "below-median": "Below the median surveyed quote for this corridor",
  "above-median": "Above the median surveyed quote for this corridor",
  "above-p90": "Higher than 90% of surveyed quotes for this corridor",
} as const;

type Step = "quote" | "review" | "done";

export default function App() {
  const [corridor, setCorridor] = useState(CORRIDORS.find((c) => c.corridor === "GBRNGA")?.corridor ?? CORRIDORS[0].corridor);
  const [raw, setRaw] = useState("200");
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState<Step>("quote");
  const [showFxHelp, setShowFxHelp] = useState(false);
  const [expired, setExpired] = useState(false);

  const c = CORRIDORS.find((x) => x.corridor === corridor)!;
  const amount = Number(raw);
  const invalid = !Number.isFinite(amount) || amount < MIN_AMOUNT || amount > MAX_AMOUNT;

  useEffect(() => {
    setLoading(true); setExpired(false);
    const t = setTimeout(() => setLoading(false), 350);
    return () => clearTimeout(t);
  }, [corridor, raw]);

  const q = useMemo(() => (invalid ? null : quote(corridor, amount)), [corridor, amount, invalid]);
  const big = useMemo(() => (invalid ? null : quote(corridor, Math.max(amount * 2.5, 500))), [corridor, amount, invalid]);
  const bm = invalid ? null : benchmarkFor(c, amount);
  const cur = c.sendCurrency;

  if (step === "done" && q) {
    return (
      <main className="shell">
        <Banner />
        <section className="card" aria-live="polite">
          <h1>Transfer scheduled (demo)</h1>
          <p className="big">{fmt(q.recipientGets, q.receive, 0)}</p>
          <p>will arrive for your recipient in {c.destination}. You paid {fmt(q.amount, cur)}, of which {fmt(q.totalCost, cur)} ({pct(q.totalPct)}) was the total cost.</p>
          <button className="primary" onClick={() => setStep("quote")}>Start a new transfer</button>
        </section>
      </main>
    );
  }

  return (
    <main className="shell">
      <Banner />
      <header>
        <h1>Send money — True Cost</h1>
        <p className="muted">See everything a transfer costs — fee <em>and</em> exchange-rate margin — before you pay.</p>
      </header>

      <section className="card" aria-labelledby="send-h">
        <h2 id="send-h">1. Amount and destination</h2>
        <div className="row">
          <label>Corridor
            <select value={corridor} onChange={(e) => { setCorridor(e.target.value); setStep("quote"); }}>
              {CORRIDORS.map((x) => <option key={x.corridor} value={x.corridor}>{x.source} → {x.destination} ({x.sendCurrency})</option>)}
            </select>
          </label>
          <label>You send ({cur})
            <input inputMode="decimal" value={raw} aria-invalid={invalid} aria-describedby="amt-help"
                   onChange={(e) => { setRaw(e.target.value.replace(/[^0-9.]/g, "")); setStep("quote"); }} />
          </label>
        </div>
        <p id="amt-help" className={invalid ? "error" : "muted"} role={invalid ? "alert" : undefined}>
          {invalid ? `Enter an amount between ${fmt(MIN_AMOUNT, cur, 0)} and ${fmt(MAX_AMOUNT, cur, 0)}.` : "Illustrative quote — prices refresh as you type."}
        </p>
      </section>

      {loading && !invalid && <section className="card skeleton" aria-busy="true" aria-label="Loading quote"><div /><div /><div /></section>}

      {!loading && q && (
        <section className="card" aria-labelledby="cost-h" aria-live="polite">
          <h2 id="cost-h">2. What this transfer really costs</h2>
          <div className="total">
            <span>Total cost</span>
            <strong>{fmt(q.totalCost, cur)}</strong>
            <span className="pill">{pct(q.totalPct)} of amount</span>
          </div>
          <dl className="breakdown">
            <div><dt>Transfer fee</dt><dd>{fmt(q.fee, cur)}</dd></div>
            <div>
              <dt>Exchange-rate margin{" "}
                <button className="link" aria-expanded={showFxHelp} aria-controls="fx-help" onClick={() => setShowFxHelp((s) => !s)}>What is this?</button>
              </dt>
              <dd>{fmt(q.fxCost, cur)}</dd>
            </div>
            <div className="sub"><dt>Our rate vs mid-market</dt><dd>1 {cur} = {q.appliedRate.toFixed(2)} {q.receive} (mid-market {q.midRate.toFixed(2)})</dd></div>
            <div className="gets"><dt>Recipient gets</dt><dd>{fmt(q.recipientGets, q.receive, 0)}</dd></div>
          </dl>
          {showFxHelp && (
            <p id="fx-help" className="help">
              The <strong>mid-market rate</strong> is the midpoint between buy and sell prices on currency markets. Providers often apply a less favourable rate and keep the difference — the <strong>exchange-rate margin</strong>. A "no fee" transfer can still cost you through this margin, so we show it as an amount.
            </p>
          )}

          <h3>How this compares</h3>
          {bm ? (
            <div className="bench">
              <Range p10={bm.b.p10} median={bm.b.median} p90={bm.b.p90} value={q.totalPct} />
              <p><strong>{POSITION_TEXT[position(q.totalPct, bm.b)]}</strong> (World Bank survey, {bm.label} transfers, {bm.b.quotes} quotes from {c.providers} providers, {c.periods[0]}–{c.periods[c.periods.length - 1]}).</p>
              <p className="muted small">Survey benchmark, not live prices. Median surveyed fee {pct(bm.b.medianFee)}, FX margin {pct(bm.b.medianFx)}.</p>
            </div>
          ) : <p className="muted">No survey benchmark is available for this corridor and amount.</p>}

          {big && (
            <>
              <h3>Sending more at once</h3>
              <p>Sending {fmt(big.amount, cur, 0)} would cost <strong>{pct(big.totalPct)}</strong> instead of {pct(q.totalPct)}, because part of the fee is fixed.</p>
            </>
          )}

          {step === "quote" && <button className="primary" onClick={() => setStep("review")}>Continue to review</button>}
        </section>
      )}

      {!loading && q && step === "review" && (
        <section className="card" aria-labelledby="rev-h">
          <h2 id="rev-h">3. Review</h2>
          {expired ? (
            <p className="error" role="alert">This quote expired. <button className="link" onClick={() => setExpired(false)}>Get a fresh quote</button></p>
          ) : (
            <>
              <p>You pay <strong>{fmt(q.amount, cur)}</strong> · total cost <strong>{fmt(q.totalCost, cur)}</strong> · recipient gets <strong>{fmt(q.recipientGets, q.receive, 0)}</strong></p>
              <div className="row">
                <button className="primary" onClick={() => setStep("done")}>Confirm transfer (demo)</button>
                <button className="secondary" onClick={() => setExpired(true)}>Simulate expired quote</button>
              </div>
            </>
          )}
        </section>
      )}

      <footer className="muted small">
        Benchmarks: {BENCHMARK_META.source}. {BENCHMARK_META.note} Fees, rates and the provider in this demo are illustrative.
      </footer>
    </main>
  );
}

function Banner() {
  return <p className="banner" role="note">Portfolio prototype with illustrative pricing. Not a real product; not affiliated with Wise or the World Bank. No real money moves.</p>;
}

function Range({ p10, median, p90, value }: { p10: number; median: number; p90: number; value: number }) {
  const max = Math.max(p90 * 1.25, value * 1.1, 1);
  const x = (v: number) => `${Math.min(Math.max(v / max, 0), 1) * 100}%`;
  return (
    <div className="range" role="img" aria-label={`Your cost ${value.toFixed(2)}%. Survey 10th percentile ${p10}%, median ${median}%, 90th percentile ${p90}%.`}>
      <div className="band" style={{ left: x(p10), width: `calc(${x(p90)} - ${x(p10)})` }} />
      <div className="tick" style={{ left: x(median) }}><span>median {median}%</span></div>
      <div className="you" style={{ left: x(value) }}><span>you {value.toFixed(2)}%</span></div>
    </div>
  );
}
