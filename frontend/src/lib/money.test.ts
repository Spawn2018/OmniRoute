import { describe, expect, it } from "vitest"
import { formatMoney, parseMoney } from "@/lib/money"

describe("parseMoney", () => {
  it("binds a decimal string to an ISO 4217 currency", () => {
    expect(parseMoney("125.5", "EUR")).toEqual({ amount: "125.5000", currency: "EUR" })
  })

  it("accepts a comma decimal from HITL amount_text without using number", () => {
    expect(parseMoney("125,50", "USD")).toEqual({ amount: "125.5000", currency: "USD" })
  })

  it("rejects number/float at runtime", () => {
    expect(() => parseMoney(1.25 as unknown as string, "EUR")).toThrow(/float/)
  })

  it("returns null for currency that is not ISO 4217", () => {
    expect(parseMoney("10", "eu")).toBeNull()
  })

  it("returns null when the fractional scale exceeds Numeric(14,4)", () => {
    expect(parseMoney("1.12345", "EUR")).toBeNull()
  })
})

describe("formatMoney", () => {
  it("renders the bound pair without converting to number", () => {
    expect(formatMoney("10", "PLN")).toBe("10.0000 PLN")
  })

  it("keeps raw HITL text when the draft amount is not a decimal", () => {
    expect(formatMoney("ok. 10", "EUR")).toBe("ok. 10 EUR")
  })
})
