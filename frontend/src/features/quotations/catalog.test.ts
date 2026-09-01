import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { quotationCreateBody } from "@/lib/quotations-api"

const PARTY = "11111111-1111-4111-8111-111111111111"
const ORIGIN = "22222222-2222-4222-8222-222222222222"
const DESTINATION = "33333333-3333-4333-8333-333333333333"

describe("quotationCreateBody", () => {
  it("sends charge_code with POL POD and party, never an amount", () => {
    const body = quotationCreateBody({
      chargeCode: " thc ",
      originPortId: ORIGIN,
      destinationPortId: DESTINATION,
      partyId: PARTY,
    })
    expect(body).toEqual({
      charge_code: "thc",
      origin_port_id: ORIGIN,
      destination_port_id: DESTINATION,
      party_id: PARTY,
    })
    expect(body).not.toHaveProperty("amount")
    expect(body).not.toHaveProperty("currency")
  })
})

describe("quotation catalog screen", () => {
  it("filters and form use party_id origin_port_id destination_port_id", () => {
    const page = readFileSync(new URL("./catalog-page.tsx", import.meta.url), "utf8")
    expect(page).toContain("party_id")
    expect(page).toContain("origin_port_id")
    expect(page).toContain("destination_port_id")
    expect(page).toContain("fetchParties")
    expect(page).toContain("fetchPorts")
  })
})
