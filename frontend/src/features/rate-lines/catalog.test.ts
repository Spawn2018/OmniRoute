import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { rateLineCreateBody, rateLineSupersedeBody } from "@/lib/rate-lines-api"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

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
        spotOrContract: "",
        indexId: "",
        fuelIndexId: "",
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
        spotOrContract: "",
        indexId: "",
        fuelIndexId: "",
      }),
    ).toEqual({
      charge_code: "THC",
      amount: "10",
      currency: "EUR",
      source_ref: "tariff://teu",
      allotment_teu: "12.5",
    })
  })

  it("includes spot_or_contract when operator fills stance", () => {
    expect(
      rateLineCreateBody({
        chargeCode: "THC",
        amount: "10",
        currency: "EUR",
        sourceRef: "tariff://spot",
        allotmentTeu: "",
        spotOrContract: " spot ",
        indexId: "",
        fuelIndexId: "",
      }),
    ).toEqual({
      charge_code: "THC",
      amount: "10",
      currency: "EUR",
      source_ref: "tariff://spot",
      spot_or_contract: "spot",
    })
  })

  it("includes index_id when operator fills pin", () => {
    expect(
      rateLineCreateBody({
        chargeCode: "THC",
        amount: "10",
        currency: "EUR",
        sourceRef: "tariff://fsc",
        allotmentTeu: "",
        spotOrContract: "",
        indexId: " FSC-Q3-2026 ",
        fuelIndexId: "",
      }),
    ).toEqual({
      charge_code: "THC",
      amount: "10",
      currency: "EUR",
      source_ref: "tariff://fsc",
      index_id: "FSC-Q3-2026",
    })
  })

  it("includes fuel_index_id when operator fills UUID", () => {
    expect(
      rateLineCreateBody({
        chargeCode: "THC",
        amount: "10",
        currency: "EUR",
        sourceRef: "tariff://fsc-fk",
        allotmentTeu: "",
        spotOrContract: "",
        indexId: "",
        fuelIndexId: " 11111111-1111-1111-1111-111111111111 ",
      }),
    ).toEqual({
      charge_code: "THC",
      amount: "10",
      currency: "EUR",
      source_ref: "tariff://fsc-fk",
      fuel_index_id: "11111111-1111-1111-1111-111111111111",
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
        spotOrContract: "",
        indexId: "",
        fuelIndexId: "",
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

describe("647.0 spot_or_contract HITL", () => {
  it("exposes optional spot_or_contract on create and supersede", () => {
    expect(page).toContain('aria-label="Spot lub kontrakt"')
    expect(page).toContain('aria-label="Nowy spot lub kontrakt"')
    expect(page).toContain("spot_or_contract")
  })
})

describe("648.0 index_id HITL", () => {
  it("exposes optional index_id on create and supersede", () => {
    expect(page).toContain('aria-label="Pin indeksu FSC"')
    expect(page).toContain('aria-label="Nowy pin indeksu FSC"')
    expect(page).toContain("index_id")
  })

  it("ships on rate-lines route", () => {
    expect(SHIPPED_CHARGE_ROUTES["648.0"]).toBe("/rate-lines")
  })
})

describe("651.0 fuel_index_id FK HITL", () => {
  it("exposes optional fuel_index_id on create and supersede", () => {
    expect(page).toContain('aria-label="Identyfikator indeksu paliwowego"')
    expect(page).toContain('aria-label="Nowy identyfikator indeksu paliwowego"')
    expect(page).toContain("fuel_index_id")
  })

  it("ships on rate-lines route", () => {
    expect(SHIPPED_CHARGE_ROUTES["651.0"]).toBe("/rate-lines")
  })
})
