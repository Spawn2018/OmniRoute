import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import {
  quotationBatchBody,
  quotationCreateBody,
  quotationCurrencies,
  quotationAcceptancePending,
  quotationCarrierInquiries,
  quotationInquiryTrails,
  quotationLanes,
  quotationPartyIds,
  quotationSkipsNbpCatalog,
  type Quotation,
} from "@/lib/quotations-api"

const PARTY = "11111111-1111-4111-8111-111111111111"
const ORIGIN = "22222222-2222-4222-8222-222222222222"
const DESTINATION = "33333333-3333-4333-8333-333333333333"

function quotationWithCurrency(currency: string): Quotation {
  return {
    id: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    organization_id: "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
    charge_code: "THC",
    rate_line_id: "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
    amount: "10.0000",
    currency,
    source_ref: "fixture",
    origin_port_id: null,
    destination_port_id: null,
    party_id: null,
  }
}

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

describe("quotationBatchBody", () => {
  it("sends charge_codes from lines, never an amount", () => {
    const body = quotationBatchBody({
      chargeCodesText: " thc \nBAF\n",
      originPortId: ORIGIN,
      destinationPortId: DESTINATION,
      partyId: PARTY,
    })
    expect(body).toEqual({
      charge_codes: ["thc", "BAF"],
      origin_port_id: ORIGIN,
      destination_port_id: DESTINATION,
      party_id: PARTY,
    })
    expect(body).not.toHaveProperty("amount")
  })
})

describe("quotation NBP lookup", () => {
  it("skips the nbp_rate catalog for PLN and lists distinct offer currencies", () => {
    expect(quotationSkipsNbpCatalog("pln")).toBe(true)
    expect(quotationSkipsNbpCatalog("EUR")).toBe(false)
    expect(
      quotationCurrencies([
        quotationWithCurrency("USD"),
        quotationWithCurrency("EUR"),
        quotationWithCurrency("USD"),
      ]),
    ).toEqual(["EUR", "USD"])
  })

  it("lists distinct party_id values and drops nulls", () => {
    const withParty = quotationWithCurrency("EUR")
    expect(
      quotationPartyIds([
        { ...withParty, party_id: PARTY },
        { ...withParty, party_id: PARTY },
        { ...withParty, party_id: null },
      ]),
    ).toEqual([PARTY])
  })

  it("builds lanes only when party POL and POD are set", () => {
    expect(quotationLanes([quotationWithCurrency("EUR")])).toEqual([])
    expect(
      quotationLanes([
        {
          ...quotationWithCurrency("EUR"),
          party_id: PARTY,
          origin_port_id: ORIGIN,
          destination_port_id: DESTINATION,
        },
      ]),
    ).toEqual([
      {
        id: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
        chargeCode: "THC",
        partyId: PARTY,
        originPortId: ORIGIN,
        destinationPortId: DESTINATION,
        amount: "10.0000",
        currency: "EUR",
      },
    ])
  })

  it("groups quotations by party_id and never sums amounts", () => {
    const first = { ...quotationWithCurrency("EUR"), party_id: PARTY, charge_code: "THC" }
    const second = {
      ...quotationWithCurrency("EUR"),
      id: "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
      party_id: PARTY,
      charge_code: "BAF",
      amount: "3.0000",
    }
    const otherParty = "44444444-4444-4444-8444-444444444444"
    const third = {
      ...quotationWithCurrency("USD"),
      id: "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
      party_id: otherParty,
      charge_code: "OTHC",
    }
    expect(
      quotationInquiryTrails([first, second, { ...first, party_id: null }, third]),
    ).toEqual([
      { partyId: PARTY, quotations: [first, second] },
      { partyId: otherParty, quotations: [third] },
    ])
  })

  it("lists quotations with party_id as pending acceptance, skipping nulls", () => {
    const withParty = { ...quotationWithCurrency("EUR"), party_id: PARTY }
    expect(
      quotationAcceptancePending([withParty, quotationWithCurrency("USD")]),
    ).toEqual([withParty])
  })

  it("matches channel quotes to quotation lanes without subtracting amounts", () => {
    const lane = {
      id: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
      chargeCode: "THC",
      partyId: PARTY,
      originPortId: ORIGIN,
      destinationPortId: DESTINATION,
      amount: "10.0000",
      currency: "EUR",
    }
    const hit = {
      id: "ffffffff-ffff-4fff-8fff-ffffffffffff",
      party_id: PARTY,
      origin_port_id: ORIGIN,
      destination_port_id: DESTINATION,
    }
    const miss = {
      id: "99999999-9999-4999-8999-999999999999",
      party_id: PARTY,
      origin_port_id: ORIGIN,
      destination_port_id: PARTY,
    }
    expect(quotationCarrierInquiries([lane], [hit, miss, hit])).toEqual([hit])
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
    expect(page).toContain("resolveNbpRate")
    expect(page).toContain("quotationSkipsNbpCatalog")
    expect(page).toContain("resolveCreditReview")
    expect(page).toContain("fetchPartyScorecard")
    expect(page).toContain("resolveChannelQuote")
    expect(page).toContain("createQuotationBatch")
    expect(page).toContain("quotationBatchBody")
    expect(page).toContain("Kody wsadowe")
    expect(page).not.toContain(".csv")
    expect(page).toContain('data-offer-document="preview"')
    expect(page).toContain('data-customer-inquiry="trail"')
    expect(page).toContain("quotationInquiryTrails")
    expect(page).toContain('data-offer-acceptance="pending"')
    expect(page).toContain("quotationAcceptancePending")
    expect(page).toContain("fetchChannelQuotes")
    expect(page).toContain("quotationCarrierInquiries")
    expect(page).toContain('data-carrier-inquiry="trail"')
    expect(page).not.toContain("acceptExtractionDraft")
    expect(page).not.toContain("imap")
    expect(page).not.toMatch(/reduce\s*\(/)
    expect(page).not.toMatch(/amount\s*\*\s*mid|mid\s*\*\s*amount/)
    expect(page).not.toMatch(/selected\.amount\s*-|channel\.amount\s*-/)
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("risk_score")
    expect(page).not.toContain("won")
    expect(page).not.toContain("window.print")
    expect(page).not.toContain("jspdf")
    expect(page).not.toContain("html2canvas")
  })
})
