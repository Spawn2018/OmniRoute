import { describe, expect, it } from "vitest"
import {
  resolveTableDensity,
  rowEstimatePx,
  rowPadClass,
} from "@/components/data-table/types"

describe("resolveTableDensity", () => {
  it("keeps condensed only when the rate-line grid allows it", () => {
    expect(resolveTableDensity("condensed", true)).toBe("condensed")
    expect(resolveTableDensity("condensed", false)).toBe("compact")
    expect(resolveTableDensity("comfortable", false)).toBe("comfortable")
  })
})

describe("condensed row metrics", () => {
  it("uses a shorter pad and estimate than compact", () => {
    expect(rowPadClass("condensed")).toBe("py-0.5")
    expect(rowEstimatePx("condensed")).toBe(24)
    expect(rowEstimatePx("compact")).toBe(32)
    expect(rowEstimatePx("comfortable")).toBe(40)
  })
})
