import { describe, expect, it } from "vitest"
import { chargeCreateBody } from "@/lib/charges-api"

describe("chargeCreateBody", () => {
  it("sends buy and sell as text with one currency", () => {
    expect(
      chargeCreateBody({
        chargeCode: " thc ",
        buyAmount: " 10.5 ",
        sellAmount: " 14 ",
        currency: "eur",
        rateLineId: "  ",
      }),
    ).toEqual({
      charge_code: "thc",
      buy_amount: "10.5",
      buy_currency: "EUR",
      sell_amount: "14",
      sell_currency: "EUR",
      rate_line_id: null,
    })
  })

  it("keeps rate_line_id when provided", () => {
    expect(
      chargeCreateBody({
        chargeCode: "THC",
        buyAmount: "10",
        sellAmount: "14",
        currency: "EUR",
        rateLineId: " 11111111-1111-1111-1111-111111111111 ",
      }).rate_line_id,
    ).toBe("11111111-1111-1111-1111-111111111111")
  })
})
