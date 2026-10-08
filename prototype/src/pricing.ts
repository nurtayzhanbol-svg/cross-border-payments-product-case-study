import data from "./data/wise_position.json";

export type Arm = "control" | "A" | "B";
export type Frequency = "once" | "weekly" | "fortnightly" | "monthly";
export interface Position { wiseTotal: number; otherMedian: number; shareCheaper: number; gapVsMedian: number; otherProviders: number; quarters: number }
export interface Corridor {
  corridor: string; source: string; destination: string; region: string; sendCurrency: string; lcuPerUsd: number;
  illustrativeFee: { fixed: number; variablePct: number }; usd200: Position; usd500: Position;
}

export const META = data.meta;
export const CORRIDORS = data.corridors as Corridor[];
export const ARMS: Record<Arm, { label: string; fixedDiscount: number }> = {
  control: { label: "Control: standard price", fixedDiscount: 0 },
  A: { label: "Arm A: fixed fee −50%", fixedDiscount: 0.5 },
  B: { label: "Arm B: fixed fee −100%", fixedDiscount: 1 },
};
export const PER_YEAR: Record<Frequency, number> = { once: 1, weekly: 52, fortnightly: 26, monthly: 12 };
export const CAP_USD = 500;
export const MIN_USD = 10;
export const MAX_USD = 5000;

/** Wise above the corridor median at USD 200 but not at USD 500: the small-amount-only gap. */
export const isPilot = (c: Corridor) => c.usd200.shareCheaper > 50 && c.usd500.shareCheaper <= 50;
export const PILOT = CORRIDORS.filter(isPilot);

const toLcu = (c: Corridor, usd: number) => Math.round(usd * c.lcuPerUsd);
export const limits = (c: Corridor) => ({ min: toLcu(c, MIN_USD), max: toLcu(c, MAX_USD), cap: toLcu(c, CAP_USD) });
export const round2 = (v: number) => Math.round((v + Number.EPSILON) * 100) / 100;

export type Parsed = { ok: true; value: number } | { ok: false; error: string };
/** Strict parse: digits with at most two decimals, within the corridor limits. Never rewrites the input. */
export function parseAmount(raw: string, c: Corridor): Parsed {
  const s = raw.trim();
  const { min, max } = limits(c);
  if (s === "") return { ok: false, error: "Enter an amount." };
  if (!/^\d+(\.\d{1,2})?$/.test(s)) {
    if (/^-/.test(s)) return { ok: false, error: "Amount must be positive." };
    if (/^\d+\.\d{3,}$/.test(s)) return { ok: false, error: "Use at most two decimal places." };
    return { ok: false, error: "Use numbers only, for example 200 or 200.50." };
  }
  const value = Number(s);
  if (value < min || value > max) return { ok: false, error: `Enter between ${min} and ${max} ${c.sendCurrency}.` };
  return { ok: true, value };
}

export interface Quote {
  amount: number; standardFee: number; fee: number; saving: number; eligible: boolean; reason: string;
  converted: number; totalPct: number; annualSaving: number; transfersPerYear: number;
}

/** Illustrative quote: fee implied by Wise's two RPW survey points, mid-market rate with no FX margin. */
export function quote(c: Corridor, amount: number, freq: Frequency, arm: Arm): Quote {
  const { fixed, variablePct } = c.illustrativeFee;
  const standardFee = round2(fixed + (variablePct / 100) * amount);
  const { cap } = limits(c);
  let reason = "";
  if (freq === "once") reason = "Regular Send pricing applies to recurring schedules only.";
  else if (amount > cap) reason = `Regular Send pricing applies to transfers up to ${cap} ${c.sendCurrency} (USD ${CAP_USD} equivalent).`;
  else if (arm === "control") reason = "You are in the control group: standard price.";
  const eligible = reason === "";
  const fee = eligible ? round2(standardFee - fixed * ARMS[arm].fixedDiscount) : standardFee;
  const saving = round2(standardFee - fee);
  const n = PER_YEAR[freq];
  return {
    amount, standardFee, fee, saving, eligible, reason, converted: round2(amount - fee),
    totalPct: (fee / amount) * 100, transfersPerYear: n, annualSaving: round2(saving * n),
  };
}

/** Relative rise in retained transfers needed for a fee cut to keep contribution unchanged. */
export function breakEvenUplift(revenue: number, discount: number, cost: number): number {
  const margin = revenue - discount - cost;
  return margin <= 0 ? Infinity : discount / margin;
}
