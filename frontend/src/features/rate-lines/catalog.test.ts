import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { rateLineCreateBody, rateLineSupersedeBody } from "@/lib/rate-lines-api"

const page = readFileSync(new URL("./catalog-page.tsx", import.meta.url), "utf8")

describe("rateLineCreateBody", () => {
  it("trims fields and uppercases currency", () => {
    expect(
      rateLineCreateBody({
        chargeCode: " thc ",
        amount: " 10.5 ",
        currency: "eur",
        sourceRef: " tariff://msc-2026 ",
      }),
    ).toEqual({
      charge_code: "thc",
      amount: "10.5",
      currency: "EUR",
      source_ref: "tariff://msc-2026",
    })
  })
})

describe("rateLineSupersedeBody", () => {
  it("sends amount as text and required source_ref", () => {
    expect(
      rateLineSupersedeBody({
        amount: "11",
        currency: "eur",
        sourceRef: "tariff://b",
      }),
    ).toEqual({
      amount: "11",
      currency: "EUR",
      source_ref: "tariff://b",
    })
  })
})

describe("rate line grid density for 53.0", () => {
  it("opts the rate line shell into condensed without making it global", () => {
    expect(page).toContain("allowCondensed")
    expect(page).toContain("DataTableShell")
  })
})
