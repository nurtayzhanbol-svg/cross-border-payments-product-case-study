import { describe, expect, it } from "vitest";
import { CORRIDORS, PILOT, breakEvenUplift, isPilot, limits, parseAmount, quote } from "./pricing";

const c = PILOT[0];

describe("data", () => {
  it("exports all surveyed Wise corridors with both amounts", () => {
    expect(CORRIDORS.length).toBe(127);
    for (const x of CORRIDORS) {
      expect(x.illustrativeFee.fixed).toBeGreaterThanOrEqual(0);
      expect(x.usd200.shareCheaper).toBeGreaterThanOrEqual(0);
    }
  });
  it("pilot corridors are uncompetitive at USD 200 only", () => {
    expect(PILOT.length).toBe(11);
    expect(PILOT.every(isPilot)).toBe(true);
  });
});

describe("parseAmount", () => {
  it("rejects invalid input without rewriting it", () => {
    expect(parseAmount("-200", c)).toEqual({ ok: false, error: "Amount must be positive." });
    expect(parseAmount("200.555", c).ok).toBe(false);
    expect(parseAmount("2e3", c).ok).toBe(false);
    expect(parseAmount("", c).ok).toBe(false);
    expect(parseAmount(String(limits(c).max + 1), c).ok).toBe(false);
  });
  it("accepts two-decimal amounts", () => {
    expect(parseAmount("200.50", c)).toEqual({ ok: true, value: 200.5 });
  });
});

describe("quote", () => {
  it("control and one-off transfers pay the standard fee", () => {
    expect(quote(c, 200, "monthly", "control").saving).toBe(0);
    expect(quote(c, 200, "once", "B").saving).toBe(0);
  });
  it("arm B removes the fixed fee only up to the cap", () => {
    const q = quote(c, 200, "monthly", "B");
    expect(q.eligible).toBe(true);
    expect(q.saving).toBeCloseTo(c.illustrativeFee.fixed, 2);
    expect(q.annualSaving).toBeCloseTo(q.saving * 12, 2);
    expect(quote(c, limits(c).cap + 1, "monthly", "B").eligible).toBe(false);
  });
  it("percentage fee falls with amount when a fixed fee exists", () => {
    const x = CORRIDORS.find((k) => k.illustrativeFee.fixed > 0)!;
    expect(quote(x, 500, "once", "control").totalPct).toBeLessThan(quote(x, 200, "once", "control").totalPct);
  });
});

describe("breakEvenUplift", () => {
  it("matches the PRD worked example", () => {
    expect(breakEvenUplift(4.81, 1.12, 2)).toBeCloseTo(0.663, 3);
    expect(breakEvenUplift(1, 1, 0.5)).toBe(Infinity);
  });
});
