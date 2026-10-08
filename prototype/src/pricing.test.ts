import { describe, expect, it } from "vitest";
import { CORRIDORS, benchmarkFor, position, quote } from "./pricing";

describe("quote", () => {
  it("total cost equals fee plus FX cost and reconciles with recipient amount", () => {
    const q = quote("GBRNGA", 200);
    expect(q.totalCost).toBeCloseTo(q.fee + q.fxCost, 10);
    const atMid = (200 - q.totalCost) * q.midRate;
    expect(q.recipientGets).toBeCloseTo(atMid, 6);
  });
  it("percentage cost falls with amount when a fixed fee exists", () => {
    expect(quote("USAMEX", 500).totalPct).toBeLessThan(quote("USAMEX", 200).totalPct);
  });
});

describe("benchmarks", () => {
  it("every exported corridor has illustrative pricing and ordered percentiles", () => {
    for (const c of CORRIDORS) {
      expect(() => quote(c.corridor, 100)).not.toThrow();
      for (const b of [c.usd200, c.usd500]) expect(b.p10 <= b.median && b.median <= b.p90).toBe(true);
    }
  });
  it("positions a quote within the survey range", () => {
    const c = CORRIDORS[0];
    const bm = benchmarkFor(c, 200)!;
    expect(position(bm.b.p10 - 0.01, bm.b)).toBe("below-p10");
    expect(position(bm.b.p90 + 1, bm.b)).toBe("above-p90");
  });
});
