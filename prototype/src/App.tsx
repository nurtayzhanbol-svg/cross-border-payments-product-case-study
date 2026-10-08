import { useMemo, useState } from "react";
import {
  ARMS, CORRIDORS, CAP_USD, META, PILOT, PER_YEAR, breakEvenUplift, isPilot, limits, parseAmount, quote,
  type Arm, type Corridor, type Frequency,
} from "./pricing";

const money = (v: number, cur: string) =>
  new Intl.NumberFormat("en-GB", { style: "currency", currency: cur, minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(v);
const pct = (v: number) => `${v.toFixed(2)}%`;
const label = (c: Corridor) => `${c.source} → ${c.destination} (${c.sendCurrency})`;
const FREQ: Record<Frequency, string> = { once: "One-off", weekly: "Every week", fortnightly: "Every 2 weeks", monthly: "Every month" };

type Tab = "flow" | "evidence" | "economics";
type Step = "quote" | "review" | "done";

function Banner() {
  return (
    <p className="banner" role="note">
      <strong>Independent portfolio prototype.</strong> Not affiliated with or endorsed by Wise or the World Bank. Prices are
      <strong> illustrative</strong> (derived from 2024–25 survey quotes), not live or official Wise prices. No money moves.
    </p>
  );
}

export default function App() {
  const [tab, setTab] = useState<Tab>("flow");
  const tabs: [Tab, string][] = [["flow", "Regular Send flow"], ["evidence", "Evidence: Wise vs corridor"], ["economics", "Break-even"]];
  return (
    <main className="shell">
      <Banner />
      <header>
        <h1>Regular Send pricing — prototype</h1>
        <p className="muted">Hypothesis: a lower fixed fee for recurring small transfers keeps regular remittance senders. To be validated.</p>
      </header>
      <div role="tablist" aria-label="Prototype views" className="tabs">
        {tabs.map(([id, name]) => (
          <button key={id} role="tab" id={`tab-${id}`} aria-selected={tab === id} aria-controls={`panel-${id}`}
            className={tab === id ? "tab active" : "tab"} onClick={() => setTab(id)}>{name}</button>
        ))}
      </div>
      <section role="tabpanel" id={`panel-${tab}`} aria-labelledby={`tab-${tab}`}>
        {tab === "flow" && <Flow />}
        {tab === "evidence" && <Evidence />}
        {tab === "economics" && <Economics />}
      </section>
      <footer className="muted small">
        Data: {META.source}; survey window {META.window.join(", ")}. {META.note}
      </footer>
    </main>
  );
}

function Flow() {
  const [showAll, setShowAll] = useState(false);
  const list = showAll ? CORRIDORS : PILOT;
  const [key, setKey] = useState(PILOT[0].corridor);
  const c = CORRIDORS.find((x) => x.corridor === key) ?? PILOT[0];
  const [raw, setRaw] = useState(String(Math.round(200 * c.lcuPerUsd)));
  const [freq, setFreq] = useState<Frequency>("monthly");
  const [arm, setArm] = useState<Arm>("A");
  const [step, setStep] = useState<Step>("quote");
  const parsed = parseAmount(raw, c);
  const q = parsed.ok ? quote(c, parsed.value, freq, arm) : null;
  const cur = c.sendCurrency;
  const { cap } = limits(c);

  const changeCorridor = (k: string) => {
    const n = CORRIDORS.find((x) => x.corridor === k)!;
    setKey(k); setRaw(String(Math.round(200 * n.lcuPerUsd))); setStep("quote");
  };

  if (step === "done" && q) {
    return (
      <div className="card" aria-live="polite">
        <h2>Schedule created (demo)</h2>
        <p>{FREQ[freq]}: {money(q.amount, cur)} to your recipient in {c.destination}. Fee per transfer {money(q.fee, cur)}.</p>
        {q.saving > 0 && <p className="big">{money(q.annualSaving, cur)} saved a year</p>}
        <button className="primary" onClick={() => setStep("quote")}>Start again</button>
      </div>
    );
  }

  return (
    <>
      <div className="card">
        <div className="row">
          <label>Corridor
            <select value={c.corridor} onChange={(e) => changeCorridor(e.target.value)}>
              {list.map((x) => <option key={x.corridor} value={x.corridor}>{label(x)}</option>)}
            </select>
          </label>
          <label>You send ({cur})
            <input inputMode="decimal" value={raw} aria-invalid={!parsed.ok} aria-describedby="amount-msg"
              onChange={(e) => { setRaw(e.target.value); setStep("quote"); }} />
          </label>
        </div>
        <label className="check"><input type="checkbox" checked={showAll}
          onChange={(e) => { setShowAll(e.target.checked); if (!e.target.checked && !isPilot(c)) changeCorridor(PILOT[0].corridor); }} />
          Show all 127 surveyed Wise corridors (default: 11 pilot corridors)</label>
        <p id="amount-msg" className={parsed.ok ? "muted small" : "error"} role={parsed.ok ? undefined : "alert"}>
          {parsed.ok ? `Regular Send pricing applies up to ${cap} ${cur} (USD ${CAP_USD} equivalent).` : parsed.error}
        </p>
        <div className="row">
          <label>How often
            <select value={freq} onChange={(e) => { setFreq(e.target.value as Frequency); setStep("quote"); }}>
              {(Object.keys(FREQ) as Frequency[]).map((f) => <option key={f} value={f}>{FREQ[f]}</option>)}
            </select>
          </label>
          <label>Experiment arm (demo control)
            <select value={arm} onChange={(e) => { setArm(e.target.value as Arm); setStep("quote"); }}>
              {(Object.keys(ARMS) as Arm[]).map((a) => <option key={a} value={a}>{ARMS[a].label}</option>)}
            </select>
          </label>
        </div>
      </div>

      {q && (
        <div className="card" aria-live="polite">
          <h2>{step === "review" ? "Review your schedule" : "Your quote"} <span className="tag">Illustrative</span></h2>
          <dl className="breakdown">
            <div><dt>Standard fee</dt><dd>{money(q.standardFee, cur)}</dd></div>
            <div><dt>Regular Send fee</dt><dd>{q.eligible ? money(q.fee, cur) : "Not applied"}</dd></div>
            {!q.eligible && <div className="sub"><dt>Why</dt><dd>{q.reason}</dd></div>}
            <div><dt>Fee as % of amount</dt><dd>{pct(q.totalPct)}</dd></div>
            <div><dt>Exchange rate</dt><dd>Mid-market, no markup (rate not simulated)</dd></div>
            <div className="gets"><dt>Converted for your recipient</dt><dd>{money(q.converted, cur)}</dd></div>
            {q.saving > 0 && <div><dt>Saving</dt><dd>{money(q.saving, cur)} per transfer · {money(q.annualSaving, cur)} a year ({PER_YEAR[freq]} transfers)</dd></div>}
            {step === "review" && <div><dt>Schedule</dt><dd>{FREQ[freq]}</dd></div>}
          </dl>
          <p className="muted small">
            Survey context (2024–25, unweighted): {c.usd200.shareCheaper}% of other surveyed quotes in this corridor were cheaper
            than Wise at USD 200, {c.usd500.shareCheaper}% at USD 500.
          </p>
          {step === "quote"
            ? <button className="primary" onClick={() => setStep("review")}>Continue</button>
            : <div className="row">
                <button className="secondary" onClick={() => setStep("quote")}>Back</button>
                <button className="primary" onClick={() => setStep("done")}>{freq === "once" ? "Confirm transfer (demo)" : "Confirm schedule (demo)"}</button>
              </div>}
        </div>
      )}
    </>
  );
}

type Filter = "all" | "pilot" | "above200" | "competitive";
const FILTERS: Record<Filter, [string, (c: Corridor) => boolean]> = {
  all: ["All surveyed Wise corridors", () => true],
  pilot: ["Uncompetitive at USD 200 only (pilot)", isPilot],
  above200: ["Majority of quotes cheaper at USD 200", (c) => c.usd200.shareCheaper > 50],
  competitive: ["Wise cheaper than most at both amounts", (c) => c.usd200.shareCheaper <= 50 && c.usd500.shareCheaper <= 50],
};

function Evidence() {
  const [f, setF] = useState<Filter>("above200");
  const rows = useMemo(() => CORRIDORS.filter(FILTERS[f][1]).sort((a, b) => b.usd200.shareCheaper - a.usd200.shareCheaper), [f]);
  return (
    <div className="card">
      <h2>Wise's position in the RPW survey</h2>
      <p className="muted small">Same corridor and quarter; other credible quotes only; median across up to four quarters. Shares are of survey quotes, not customers or volume.</p>
      <label>Show
        <select value={f} onChange={(e) => setF(e.target.value as Filter)}>
          {(Object.keys(FILTERS) as Filter[]).map((k) => <option key={k} value={k}>{FILTERS[k][0]}</option>)}
        </select>
      </label>
      <p aria-live="polite"><strong>{rows.length}</strong> of {CORRIDORS.length} corridors</p>
      <div className="tablewrap" tabIndex={0} aria-label="Corridor table, scrollable">
        <table>
          <thead><tr><th scope="col">Corridor</th><th scope="col">Wise @200</th><th scope="col">Median @200</th>
            <th scope="col">% cheaper @200</th><th scope="col">Wise @500</th><th scope="col">% cheaper @500</th></tr></thead>
          <tbody>{rows.map((c) => (
            <tr key={c.corridor}><th scope="row">{c.source} → {c.destination}</th>
              <td>{pct(c.usd200.wiseTotal)}</td><td>{pct(c.usd200.otherMedian)}</td><td>{c.usd200.shareCheaper}%</td>
              <td>{pct(c.usd500.wiseTotal)}</td><td>{c.usd500.shareCheaper}%</td></tr>))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Num({ id, labelText, value, set }: { id: string; labelText: string; value: string; set: (v: string) => void }) {
  const bad = !/^\d+(\.\d{1,2})?$/.test(value.trim());
  return (
    <label htmlFor={id}>{labelText}
      <input id={id} inputMode="decimal" value={value} aria-invalid={bad} onChange={(e) => set(e.target.value)} />
    </label>
  );
}

function Economics() {
  const [r, setR] = useState("4.81");
  const [d, setD] = useState("1.12");
  const [cost, setCost] = useState("2.00");
  const vals = [r, d, cost].map((v) => (/^\d+(\.\d{1,2})?$/.test(v.trim()) ? Number(v) : NaN));
  const ok = vals.every(Number.isFinite);
  const u = ok ? breakEvenUplift(vals[0], vals[1], vals[2]) : NaN;
  return (
    <div className="card">
      <h2>How much must retention rise to pay for the discount?</h2>
      <p className="muted small">All inputs are assumptions in USD per transfer. Defaults: RPW-implied Wise fee at USD 200 (USD 2.23 fixed + 1.29%), arm A discount, a guessed variable cost.</p>
      <div className="row">
        <Num id="rev" labelText="Fee revenue per transfer" value={r} set={setR} />
        <Num id="disc" labelText="Discount per transfer" value={d} set={setD} />
        <Num id="cost" labelText="Variable cost per transfer (unknown)" value={cost} set={setCost} />
      </div>
      <p aria-live="polite" className={ok ? "big" : "error"}>
        {!ok ? "Enter non-negative numbers with up to two decimals."
          : u === Infinity ? "Never: the discount leaves no margin."
          : `+${(u * 100).toFixed(0)}% more retained transfers needed`}
      </p>
      <p className="muted small">Formula: discount ÷ (revenue − discount − cost). The pilot ships only if the measured lift beats this (see measurement plan).</p>
    </div>
  );
}
