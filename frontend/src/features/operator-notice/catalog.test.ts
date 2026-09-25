import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { operatorNotices, operatorNoticesFiltered, readNoticeKindFilter } from "@/lib/operator-notices"
import type { Quotation } from "@/lib/quotations-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

const PARTY = "11111111-1111-4111-8111-111111111111"

function quotation(partyId: string | null): Quotation {
  return {
    id: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    organization_id: "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
    charge_code: "THC",
    rate_line_id: "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
    amount: "10.0000",
    currency: "EUR",
    source_ref: "fixture",
    origin_port_id: null,
    destination_port_id: null,
    party_id: partyId,
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
    valid_until: null,
    revision_no: null,
    mqc_teu: null,
    mqc_window: null,
  }
}

describe("operator notices", () => {
  it("lists pending HITL drafts and quotations with party_id, skipping reviewed drafts", () => {
    expect(
      operatorNotices(
        [
          { id: "draft-pending", status: "pending", source_ref: "tariff://a" },
          { id: "draft-done", status: "accepted", source_ref: "tariff://b" },
        ],
        [quotation(PARTY), quotation(null)],
      ),
    ).toEqual([
      {
        kind: "extraction_draft",
        id: "draft-pending",
        href: "/extractions",
        label: "tariff://a",
        amount: null,
        currency: null,
      },
      {
        kind: "offer_acceptance",
        id: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
        href: "/quotations",
        label: "THC",
        amount: "10.0000",
        currency: "EUR",
      },
    ])
  })

  it("filters the 27.0 board by kind without dropping the compose-read", () => {
    const mixed = operatorNotices(
      [{ id: "draft-pending", status: "pending", source_ref: "tariff://a" }],
      [quotation(PARTY)],
    )
    expect(operatorNoticesFiltered(mixed, "all")).toHaveLength(2)
    expect(operatorNoticesFiltered(mixed, "extraction_draft")).toEqual([mixed[0]])
    expect(operatorNoticesFiltered(mixed, "offer_acceptance")).toEqual([mixed[1]])
    expect(readNoticeKindFilter("offer_acceptance")).toBe("offer_acceptance")
    expect(readNoticeKindFilter("loose")).toBe("all")
  })
})

describe("operator-notice surface for 27.0", () => {
  it("ships /notifications as read-only pending work without sending mail", () => {
    const page = readFileSync(path.join(srcRoot, "features/operator-notice/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/notifications.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    const helper = readFileSync(path.join(srcRoot, "lib/operator-notices.ts"), "utf8")
    expect(route).toContain("/notifications")
    expect(nav).toContain("/notifications")
    expect(lists).toContain("operatorNotice")
    expect(ops).toContain("/notifications")
    expect(page).toContain('data-operator-notice="board"')
    expect(page).toContain('data-operator-notice="kind-filter"')
    expect(page).toContain("operatorNoticesFiltered")
    expect(page).toContain("Filtr pending")
    expect(page).toContain("fetchExtractionDrafts")
    expect(page).toContain("operatorNotices")
    expect(helper).toContain("quotationAcceptancePending")
    expect(page).toContain("fetchQuotations")
    expect(page).toContain("Art. 50")
    expect(page).not.toContain("acceptExtractionDraft")
    expect(page).not.toContain("imap")
    expect(page).not.toContain("smtp")
    expect(page).not.toContain("CatalogCreateForm")
  })

  it("ships stored operator_notice inbox on the same /notifications screen", () => {
    const page = readFileSync(path.join(srcRoot, "features/operator-notice/catalog-page.tsx"), "utf8")
    const api = readFileSync(path.join(srcRoot, "lib/operator-notices-api.ts"), "utf8")
    expect(api).toContain("/api/v1/operator-notices")
    expect(page).toContain("createOperatorNotice")
    expect(page).toContain("readOperatorNotice")
    expect(page).toContain("Zapisz unread")
    expect(page).not.toContain("amount +")
    expect(page).not.toContain("imap")
  })
})

