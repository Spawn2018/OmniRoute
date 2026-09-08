import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { documentChecklistRuleBody } from "@/lib/document-checklist-rules-api"
import { documentDispatchRuleBody } from "@/lib/document-dispatch-rules-api"
import { fieldCarryForwardBody } from "@/lib/field-carry-forwards-api"
import { incotermResponsibilityBody } from "@/lib/incoterm-responsibilities-api"
import {
  quotationBatchBody,
  quotationCreateBody,
  quotationCurrencies,
  quotationAcceptancePending,
  quotationCarrierInquiries,
  quotationInquiryTrails,
  quotationInvoiceSettlements,
  quotationLanes,
  quotationOperationalExceptions,
  quotationResponseComparisons,
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
    customer_rfq_id: null,
    commodity_code_id: null,
    dangerous_good_id: null,
    document_number: null,
    negotiated_channel_quote_id: null,
    noted_credit_review_id: null,
    incoterm: null,
    incoterms_version: null,
    trade_side: null,
    named_place: null,
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
    expect(body).not.toHaveProperty("customer_rfq_id")
    expect(body).not.toHaveProperty("commodity_code_id")
    expect(body).not.toHaveProperty("dangerous_good_id")
  })

  it("sends customer_rfq_id only when selected", () => {
    const rfqId = "44444444-4444-4444-8444-444444444444"
    const body = quotationCreateBody({
      chargeCode: "THC",
      originPortId: ORIGIN,
      destinationPortId: DESTINATION,
      partyId: PARTY,
      customerRfqId: rfqId,
    })
    expect(body.customer_rfq_id).toBe(rfqId)
    expect(body).not.toHaveProperty("amount")
  })

  it("sends commodity_code_id only when selected", () => {
    const hsId = "55555555-5555-4555-8555-555555555555"
    const body = quotationCreateBody({
      chargeCode: "THC",
      originPortId: ORIGIN,
      destinationPortId: DESTINATION,
      partyId: PARTY,
      commodityCodeId: hsId,
    })
    expect(body.commodity_code_id).toBe(hsId)
    expect(body).not.toHaveProperty("amount")
  })

  it("sends dangerous_good_id only when selected", () => {
    const unId = "66666666-6666-4666-8666-666666666666"
    const body = quotationCreateBody({
      chargeCode: "THC",
      originPortId: ORIGIN,
      destinationPortId: DESTINATION,
      partyId: PARTY,
      dangerousGoodId: unId,
    })
    expect(body.dangerous_good_id).toBe(unId)
    expect(body).not.toHaveProperty("amount")
  })

  it("sends incoterm fields only when selected, never an amount", () => {
    const body = quotationCreateBody({
      chargeCode: "THC",
      originPortId: ORIGIN,
      destinationPortId: DESTINATION,
      partyId: PARTY,
      incoterm: "DAP",
      incotermsVersion: "2020",
      tradeSide: "import",
      namedPlace: " Gdynia ",
    })
    expect(body.incoterm).toBe("DAP")
    expect(body.named_place).toBe("Gdynia")
    expect(body).not.toHaveProperty("amount")
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

describe("field carry-forward and checklist bodies", () => {
  it("sends allowlisted snapshot fields and never an amount", () => {
    const body = fieldCarryForwardBody({
      quotationId: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
      shipmentId: "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
      incoterm: " FOB ",
      tradeSide: "export",
      namedPlace: null,
    })
    expect(body.fields).toEqual({ incoterm: "FOB", trade_side: "export" })
    expect(body).not.toHaveProperty("amount")
  })

  it("sends checklist triple with blocks_dispatch flag, never an amount", () => {
    const body = documentChecklistRuleBody({
      incoterm: "FOB",
      tradeSide: "export",
      mode: "ocean",
      documentKind: "bill_of_lading",
      blocksDispatch: true,
    })
    expect(body.blocks_dispatch).toBe(true)
    expect(body).not.toHaveProperty("amount")
  })

  it("sends dispatch recipient role without an amount", () => {
    const body = documentDispatchRuleBody({
      incoterm: " DAP ",
      tradeSide: "import",
      documentKind: "commercial_invoice",
      recipientRole: "omni_customs",
    })
    expect(body.recipient_role).toBe("omni_customs")
    expect(body.source_ref).toBe("tenant:manual")
    expect(body).not.toHaveProperty("amount")
  })

  it("sends incoterm responsibility pair without an amount", () => {
    const body = incotermResponsibilityBody({
      incoterm: " DDP ",
      tradeSide: "import",
      exportClearanceRole: "seller",
      importClearanceRole: "seller",
      mainCarriageBooker: "seller",
      bookingScope: ["ocean", "oncarriage"],
    })
    expect(body.import_clearance_role).toBe("seller")
    expect(body.source_ref).toBe("tenant:manual")
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

  it("lists operational exceptions when party is set but POL or POD is missing", () => {
    const withParty = { ...quotationWithCurrency("EUR"), party_id: PARTY }
    expect(quotationOperationalExceptions([{ ...withParty, party_id: null }])).toEqual([])
    expect(
      quotationOperationalExceptions([
        {
          ...withParty,
          origin_port_id: ORIGIN,
          destination_port_id: DESTINATION,
        },
      ]),
    ).toEqual([])
    expect(quotationOperationalExceptions([withParty])).toEqual([withParty])
    expect(
      quotationOperationalExceptions([{ ...withParty, origin_port_id: ORIGIN }]),
    ).toEqual([{ ...withParty, origin_port_id: ORIGIN }])
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

  it("hides quotations that already have an accepted decision", () => {
    const withParty = { ...quotationWithCurrency("EUR"), party_id: PARTY }
    expect(
      quotationAcceptancePending(
        [withParty],
        [{ subject_kind: "quotation", subject_id: withParty.id, status: "accepted" }],
      ),
    ).toEqual([])
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

  it("pairs quotation lanes with channel quotes on POL/POD even when party_id differs", () => {
    const lane = {
      id: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
      chargeCode: "THC",
      partyId: PARTY,
      originPortId: ORIGIN,
      destinationPortId: DESTINATION,
      amount: "10.0000",
      currency: "EUR",
    }
    const sameParty = {
      id: "ffffffff-ffff-4fff-8fff-ffffffffffff",
      party_id: PARTY,
      origin_port_id: ORIGIN,
      destination_port_id: DESTINATION,
    }
    const otherCarrier = "55555555-5555-4555-8555-555555555555"
    const otherParty = {
      id: "66666666-6666-4666-8666-666666666666",
      party_id: otherCarrier,
      origin_port_id: ORIGIN,
      destination_port_id: DESTINATION,
    }
    const otherLane = {
      id: "77777777-7777-4777-8777-777777777777",
      party_id: PARTY,
      origin_port_id: ORIGIN,
      destination_port_id: PARTY,
    }
    expect(quotationResponseComparisons([lane], [sameParty, otherParty, otherLane, sameParty])).toEqual([
      {
        originPortId: ORIGIN,
        destinationPortId: DESTINATION,
        quotations: [lane],
        quotes: [sameParty, otherParty],
      },
    ])
  })

  it("pairs quotations with charge sell on shared rate_line_id and skips nulls", () => {
    const quoted = quotationWithCurrency("EUR")
    const hit = {
      id: "ffffffff-ffff-4fff-8fff-ffffffffffff",
      rate_line_id: quoted.rate_line_id,
      sell_amount: "12.0000",
      sell_currency: "EUR",
    }
    const orphan = {
      id: "99999999-9999-4999-8999-999999999999",
      rate_line_id: null,
      sell_amount: "1.0000",
      sell_currency: "EUR",
    }
    const otherCharge = {
      id: "88888888-8888-4888-8888-888888888888",
      rate_line_id: "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
      sell_amount: "3.0000",
      sell_currency: "USD",
    }
    expect(quotationInvoiceSettlements([quoted], [hit, orphan, hit, otherCharge])).toEqual([
      {
        rateLineId: quoted.rate_line_id,
        quotations: [quoted],
        charges: [hit],
      },
    ])
  })
})

describe("quotation catalog screen", () => {
  it("filters and form use party_id origin_port_id destination_port_id", () => {
    const page = readFileSync(new URL("./catalog-page.tsx", import.meta.url), "utf8")
    expect(page).toContain("party_id")
    expect(page).toContain("customer_rfq_id")
    expect(page).toContain("commodity_code_id")
    expect(page).toContain("dangerous_good_id")
    expect(page).toContain("fetchCustomerRfqs")
    expect(page).toContain("fetchCommodityCodes")
    expect(page).toContain("fetchDangerousGoods")
    expect(page).toContain('data-quote-un="picker"')
    expect(page).toContain('data-quote-incoterm="picker"')
    expect(page).toContain("origin_port_id")
    expect(page).toContain("destination_port_id")
    expect(page).toContain("fetchParties")
    expect(page).toContain("fetchPorts")
    expect(page).toContain("resolveNbpRate")
    expect(page).toContain("quotationSkipsNbpCatalog")
    expect(page).toContain("resolveCreditReview")
    expect(page).toContain("fetchPartyScorecard")
    expect(page).toContain("noteQuotationRisk")
    expect(page).toContain("Zapisz fakt")
    expect(page).toContain('data-offer-risk="fact"')
    expect(page).toContain("resolveChannelQuote")
    expect(page).toContain("negotiateQuotation")
    expect(page).toContain("Zapisz wynik")
    expect(page).toContain('data-offer-negotiation="result"')
    expect(page).toContain("createQuotationBatch")
    expect(page).toContain("quotationBatchBody")
    expect(page).toContain("Kody wsadowe")
    expect(page).not.toContain(".csv")
    expect(page).toContain('data-offer-document="preview"')
    expect(page).toContain("data-print-template")
    expect(page).toContain("Nadaj numer")
    expect(page).toContain("Drukuj")
    expect(page).toContain("issueQuotationDocumentNumber")
    expect(page).toContain("fetchQuotationDocumentLayout")
    expect(page).toContain("window.print")
    expect(page).toContain('data-customer-inquiry="trail"')
    expect(page).toContain("quotationInquiryTrails")
    expect(page).toContain('data-offer-acceptance="pending"')
    expect(page).toContain("quotationAcceptancePending")
    expect(page).toContain("createOperatorDecision")
    expect(page).toContain("decideOperatorDecision")
    expect(page).toContain("Przyjmij")
    expect(page).toContain("DecideStatusButtons")
    expect(page).toContain("fetchChannelQuotes")
    expect(page).toContain("createChannelQuote")
    expect(page).toContain('data-channel-quote="from-quote"')
    expect(page).toContain("Zapisz ofertę kanału")
    expect(page).toContain("quotationCarrierInquiries")
    expect(page).toContain('data-carrier-inquiry="trail"')
    expect(page).toContain("quotationResponseComparisons")
    expect(page).toContain('data-response-comparison="lanes"')
    expect(page).toContain("najtańsza")
    expect(page).toContain("najszybszy TT")
    expect(page).toContain("comparisonChargeBody")
    expect(page).toContain("createCharge")
    expect(page).toContain("CarryForwardPanel")
    expect(page).toContain("ChecklistRulePanel")
    expect(page).toContain("IncotermResponsibilityPanel")
    expect(page).toContain("DispatchRulePanel")
    const carry = readFileSync(new URL("./carry-forward-panel.tsx", import.meta.url), "utf8")
    const checklist = readFileSync(new URL("./checklist-rule-panel.tsx", import.meta.url), "utf8")
    const matrix = readFileSync(new URL("./incoterm-responsibility-panel.tsx", import.meta.url), "utf8")
    const dispatch = readFileSync(new URL("./dispatch-rule-panel.tsx", import.meta.url), "utf8")
    expect(carry).toContain('data-carry-forward="job"')
    expect(carry).toContain("Przenieś pola")
    expect(carry).toContain("fieldCarryForwardBody")
    expect(carry).not.toContain("parseFloat")
    expect(checklist).toContain('data-checklist-rule="job"')
    expect(checklist).toContain("Zapisz regułę")
    expect(checklist).toContain("blocks_dispatch")
    expect(checklist).toContain("documentChecklistRuleBody")
    expect(matrix).toContain('data-incoterm-responsibility="job"')
    expect(matrix).toContain("Seed Omni 11×2")
    expect(matrix).toContain("incotermResponsibilityBody")
    expect(matrix).not.toContain("ICC")
    expect(matrix).not.toContain("parseFloat")
    expect(dispatch).toContain('data-dispatch-rule="catalog"')
    expect(dispatch).toContain("Zapisz adresata")
    expect(dispatch).toContain("documentDispatchRuleBody")
    expect(dispatch).not.toContain("sold_to")
    expect(dispatch).not.toContain("parseFloat")
    expect(page).not.toContain("acceptExtractionDraft")
    expect(page).not.toContain("imap")
    expect(page).not.toMatch(/reduce\s*\(/)
    expect(page).not.toMatch(/amount\s*\*\s*mid|mid\s*\*\s*amount/)
    expect(page).not.toMatch(/selected\.amount\s*-|channel\.amount\s*-/)
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("risk_score")
    expect(page).not.toContain("won")
    expect(page).not.toContain("jspdf")
    expect(page).not.toContain("html2canvas")
  })
})
