import { describe, expect, it } from "vitest"
import { quotationCreateBody } from "@/lib/quotations-api"

describe("quotationCreateBody", () => {
  it("sends only charge_code, never an amount", () => {
    const body = quotationCreateBody(" thc ")
    expect(body).toEqual({ charge_code: "thc" })
    expect(body).not.toHaveProperty("amount")
    expect(body).not.toHaveProperty("currency")
  })
})
