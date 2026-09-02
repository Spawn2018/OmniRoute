import { readFileSync } from "node:fs"
import { createElement } from "react"
import { renderToStaticMarkup } from "react-dom/server"
import { describe, expect, it } from "vitest"
import { Money } from "@/components/money"
import { formatMoney, moneyAxis, parseMoney } from "@/lib/money"

const moneySrc = readFileSync(new URL("../components/money.tsx", import.meta.url), "utf8")

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

describe("moneyAxis", () => {
  it("splits a parsed pair on the decimal point without Number", () => {
    expect(moneyAxis("125,5", "EUR")).toEqual({
      integer: "125",
      fraction: "5000",
      currency: "EUR",
    })
  })

  it("returns null for HITL text that is not a decimal", () => {
    expect(moneyAxis("ok. 10", "EUR")).toBeNull()
  })
})

describe("Money decimal axis for 52.0", () => {
  it("ships integer fraction currency grid without parseFloat", () => {
    expect(moneySrc).toContain("moneyAxis")
    expect(moneySrc).toContain('data-money="axis"')
    expect(moneySrc).not.toContain("parseFloat")
    expect(moneySrc).not.toContain("Number(")
    const html = renderToStaticMarkup(createElement(Money, { amount: "10", currency: "PLN" }))
    expect(html).toContain('data-money="axis"')
    expect(html).toContain("10")
    expect(html).toContain(".0000")
    expect(html).toContain("PLN")
  })

  it("keeps raw HITL text off the axis", () => {
    const html = renderToStaticMarkup(createElement(Money, { amount: "ok. 10", currency: "EUR" }))
    expect(html).not.toContain('data-money="axis"')
    expect(html).toContain("ok. 10 EUR")
  })
})
