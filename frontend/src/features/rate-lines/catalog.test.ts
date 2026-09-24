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
        allotmentTeu: "",
      }),
    ).toEqual({
      charge_code: "thc",
      amount: "10.5",
      currency: "EUR",
      source_ref: "tariff://msc-2026",
    })
  })

  it("includes allotment_teu when operator fills TEU", () => {
    expect(
      rateLineCreateBody({
        chargeCode: "THC",
        amount: "10",
        currency: "EUR",
        sourceRef: "tariff://teu",
        allotmentTeu: " 12.5 ",
      }),
    ).toEqual({
      charge_code: "THC",
      amount: "10",
      currency: "EUR",
      source_ref: "tariff://teu",
      allotment_teu: "12.5",
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
        allotmentTeu: "",
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

describe("646.0 allotment_teu HITL", () => {
  it("exposes optional allotment TEU on create and supersede", () => {
    expect(page).toContain('aria-label="Alokacja TEU"')
    expect(page).toContain('aria-label="Nowa alokacja TEU"')
    expect(page).toContain("allotment_teu")
  })
})
