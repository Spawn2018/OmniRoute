import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { chargeCreateBody, comparisonChargeBody } from "@/lib/charges-api"

describe("charge catalog shipment field", () => {
  it("shows an optional shipment id on the charge form", () => {
    expect(page).toContain('aria-label="Zlecenie"')
  })
})

const page = readFileSync(
  new URL("../../features/charges/catalog-page.tsx", import.meta.url),
  "utf8",
)

describe("chargeCreateBody", () => {
  it("sends buy and sell as text with one currency", () => {
    expect(
      chargeCreateBody({
        chargeCode: " thc ",
        buyAmount: " 10.5 ",
        sellAmount: " 14 ",
        currency: "eur",
        rateLineId: "  ",
        sourceRef: " tenant:manual ",
      }),
    ).toEqual({
      charge_code: "thc",
      buy_amount: "10.5",
      buy_currency: "EUR",
      sell_amount: "14",
      sell_currency: "EUR",
      rate_line_id: null,
      source_ref: "tenant:manual",
      shipment_id: null,
    })
  })

  it("sends optional shipment_id when the operator typed one", () => {
    expect(
      chargeCreateBody({
        chargeCode: "THC",
        buyAmount: "10",
        sellAmount: "14",
        currency: "EUR",
        rateLineId: "",
        sourceRef: "tenant:manual",
        shipmentId: " 33333333-3333-3333-3333-333333333333 ",
      }).shipment_id,
    ).toBe("33333333-3333-3333-3333-333333333333")
  })

  it("keeps rate_line_id when provided", () => {
    expect(
      chargeCreateBody({
        chargeCode: "THC",
        buyAmount: "10",
        sellAmount: "14",
        currency: "EUR",
        rateLineId: " 11111111-1111-1111-1111-111111111111 ",
        sourceRef: "tariff://a",
      }).rate_line_id,
    ).toBe("11111111-1111-1111-1111-111111111111")
  })

  it("sends optional UN pair and floor_decision_id for margin_floor", () => {
    expect(
      chargeCreateBody({
        chargeCode: "THC",
        buyAmount: "10",
        sellAmount: "11",
        currency: "EUR",
        rateLineId: "",
        sourceRef: "tenant:manual",
        originUnlocode: " plgdy ",
        destinationUnlocode: " deham ",
        floorDecisionId: " 22222222-2222-2222-2222-222222222222 ",
      }),
    ).toMatchObject({
      origin_unlocode: "PLGDY",
      destination_unlocode: "DEHAM",
      floor_decision_id: "22222222-2222-2222-2222-222222222222",
    })
  })
})

describe("comparisonChargeBody", () => {
  it("copies buy from channel and sell from quotation without subtracting", () => {
    expect(
      comparisonChargeBody(
        { chargeCode: " ofr ", amount: " 1200 ", currency: "usd" },
        { amount: " 900 ", currency: "usd" },
      ),
    ).toEqual({
      charge_code: "ofr",
      buy_amount: "900",
      buy_currency: "USD",
      sell_amount: "1200",
      sell_currency: "USD",
      rate_line_id: null,
      source_ref: "tenant:manual:comparison",
    })
  })
})

describe("charge catalog 547.0", () => {
  it("exposes UN and floor_decision fields without matching in the browser", () => {
    expect(page).toContain("UN/LOCODE origin")
    expect(page).toContain("UN/LOCODE destination")
    expect(page).toContain("floor_decision_id")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("Haversine")
  })
})
