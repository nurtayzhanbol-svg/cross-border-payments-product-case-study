import data from "./data/benchmarks.json";

export type Benchmark = { quotes: number; p10: number; median: number; p90: number; medianFee: number; medianFx: number };
export type Corridor = {
  corridor: string; source: string; destination: string; sendCurrency: string;
  periods: string[]; providers: number; usd200: Benchmark; usd500: Benchmark;
};

export const BENCHMARK_META = data.meta;
export const CORRIDORS = data.corridors as Corridor[];

/** ILLUSTRATIVE values used to generate a demo quote. Not real prices or live rates. */
export const ILLUSTRATIVE: Record<string, { receive: string; midRate: number; fixedFee: number; pctFee: number; fxMarginPct: number }> = {
  GBRNGA: { receive: "NGN", midRate: 2000, fixedFee: 0.99, pctFee: 0.004, fxMarginPct: 0.6 },
  GBRIND: { receive: "INR", midRate: 112, fixedFee: 0.99, pctFee: 0.004, fxMarginPct: 0.5 },
  GBRKEN: { receive: "KES", midRate: 172, fixedFee: 0.99, pctFee: 0.005, fxMarginPct: 0.8 },
  USAMEX: { receive: "MXN", midRate: 18.5, fixedFee: 2.99, pctFee: 0.0, fxMarginPct: 1.2 },
  USAPHL: { receive: "PHP", midRate: 57, fixedFee: 1.99, pctFee: 0.003, fxMarginPct: 1.0 },
  DEUTUR: { receive: "TRY", midRate: 47, fixedFee: 1.49, pctFee: 0.004, fxMarginPct: 0.9 },
};

export type Quote = {
  amount: number; fee: number; fxCost: number; totalCost: number; totalPct: number;
  midRate: number; appliedRate: number; recipientGets: number; receive: string;
};

export const MIN_AMOUNT = 20;
export const MAX_AMOUNT = 5000;

export function quote(corridor: string, amount: number): Quote {
  const p = ILLUSTRATIVE[corridor];
  if (!p) throw new Error(`No illustrative pricing for ${corridor}`);
  const fee = p.fixedFee + amount * p.pctFee;
  const converted = amount - fee;
  const appliedRate = p.midRate * (1 - p.fxMarginPct / 100);
  const recipientGets = converted * appliedRate;
  const fxCost = converted * (p.fxMarginPct / 100);
  const totalCost = fee + fxCost;
  return { amount, fee, fxCost, totalCost, totalPct: (totalCost / amount) * 100, midRate: p.midRate,
           appliedRate, recipientGets, receive: p.receive };
}

/** Position of a cost % within the survey benchmark for the nearest surveyed amount (USD 200 or 500). */
export function benchmarkFor(c: Corridor, amount: number): { b: Benchmark; label: string } | null {
  const b = amount >= 350 ? c.usd500 : c.usd200;
  if (b.quotes < 10) return null;
  return { b, label: amount >= 350 ? "~USD 500" : "~USD 200" };
}

export function position(totalPct: number, b: Benchmark): "below-p10" | "below-median" | "above-median" | "above-p90" {
  if (totalPct <= b.p10) return "below-p10";
  if (totalPct <= b.median) return "below-median";
  if (totalPct <= b.p90) return "above-median";
  return "above-p90";
}
