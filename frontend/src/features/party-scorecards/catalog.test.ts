import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { quotationOfferOutcomes } from "@/features/party-scorecards/offer-outcomes"
import { scorecardUpsertBody } from "@/lib/party-scorecards-api"
import type { OperatorDecision } from "@/lib/operator-decisions-api"
import type { Quotation } from "@/lib/quotations-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("scorecardUpsertBody", () => {
  it("turns blank KPI fields into null and keeps counts", () => {
    expect(
      scorecardUpsertBody({
        partyId: " ignored ",
        responseRate: " 0.8 ",
        medianHours: "  ",
        pricePosition: "0.4",
        quoteInvoiceMatch: "",
        rolloverCount: "2",
        sampleSize: "3",
        windowDays: "60",
      }),
    ).toEqual({
      response_rate: "0.8",
      median_response_hours: null,
      price_position: "0.4",
      quote_invoice_match_rate: null,
      rollover_count: 2,
      sample_size: 3,
      window_days: 60,
    })
  })
})

describe("party-scorecards catalog surface for 10.0", () => {
  it("ships ranking table with snapshot save and no money engine", () => {
    const page = readFileSync(
      path.join(srcRoot, "features/party-scorecards/catalog-page.tsx"),
      "utf8",
    )
    const route = readFileSync(path.join(srcRoot, "routes/party-scorecards.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/party-scorecards")
    expect(nav).toContain("/party-scorecards")
    expect(lists).toContain("partyScorecards")
    expect(ops).toContain("/party-scorecards")
    expect(page).toContain("CatalogLoadedTable")
    expect(page).toContain("upsertPartyScorecard")
    expect(page).toContain("source_ref")
    expect(page).not.toContain("amount")
    expect(page).not.toContain("natural_person")
    expect(page).not.toContain("charge.margin")
  })

  it("lists quotation S11 verdicts without writing KPI or scoring a person", () => {
    const page = readFileSync(
      path.join(srcRoot, "features/party-scorecards/catalog-page.tsx"),
      "utf8",
    )
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(ops).toContain('"120.0": "/party-scorecards"')
    expect(page).toContain('data-scorecard="offer-outcomes"')
    expect(page).toContain("quotationOfferOutcomes")
    expect(page).toContain("fetchQuotations")
    expect(page).toContain("fetchOperatorDecisions")
    expect(page).toContain("/decisions")
    expect(page).toContain("/quotations")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("openai")
    expect(page).not.toContain("won")
    expect(page).not.toContain("lost")
    expect(page).not.toContain("natural_person")
  })
})

function quoteRow(id: string, partyId: string | null): Quotation {
  return {
    id,
    organization_id: "org",
    charge_code: "FRT",
    rate_line_id: "rl",
    amount: "1.00",
    currency: "EUR",
    source_ref: "fixture://quotation/1",
    origin_port_id: null,
    destination_port_id: null,
    party_id: partyId,
    customer_rfq_id: null,
    commodity_code_id: null,
    document_number: null,
    negotiated_channel_quote_id: null,
    noted_credit_review_id: null,
  }
}

function decisionRow(
  subjectId: string,
  status: OperatorDecision["status"],
  kind = "quotation",
): OperatorDecision {
  return {
    id: `d-${subjectId}-${status}`,
    organization_id: "org",
    subject_kind: kind,
    subject_id: subjectId,
    status,
    decided_at: null,
    lock_version: 1,
    source_ref: "fixture://decision/1",
  }
}

describe("quotationOfferOutcomes", () => {
  it("keeps accepted and rejected quotation verdicts with a party", () => {
    expect(
      quotationOfferOutcomes(
        [quoteRow("q1", "p1"), quoteRow("q2", null)],
        [
          decisionRow("q1", "accepted"),
          decisionRow("q1-pending", "pending"),
          decisionRow("q2", "rejected"),
          decisionRow("q1", "accepted", "inbound_message"),
        ],
      ),
    ).toEqual([
      {
        quotationId: "q1",
        partyId: "p1",
        status: "accepted",
        sourceRef: "fixture://decision/1",
      },
    ])
  })
})
