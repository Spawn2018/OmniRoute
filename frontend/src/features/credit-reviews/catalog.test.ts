import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { creditReviewAttachBureauBody, creditReviewCreateBody } from "@/lib/credit-reviews-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("creditReviewCreateBody", () => {
  it("lowers decision and drops empty note without source_ref", () => {
    expect(
      creditReviewCreateBody({
        partyId: "  party-1  ",
        reviewDate: "2026-09-01",
        decision: " HOLD ",
        note: "  ",
      }),
    ).toEqual({
      party_id: "party-1",
      review_date: "2026-09-01",
      decision: "hold",
      note: null,
    })
  })
})

describe("credit-reviews catalog surface for 14.0", () => {
  it("ships /credit-reviews on DataTableShell with decision and without scoring", () => {
    const page = readFileSync(
      path.join(srcRoot, "features/credit-reviews/catalog-page.tsx"),
      "utf8",
    )
    const route = readFileSync(path.join(srcRoot, "routes/credit-reviews.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    const parties = readFileSync(path.join(srcRoot, "features/parties/catalog-page.tsx"), "utf8")
    expect(route).toContain("/credit-reviews")
    expect(nav).toContain("/credit-reviews")
    expect(lists).toContain("creditReviews")
    expect(ops).toContain("/credit-reviews")
    expect(parties).toContain("createCreditReview")
    expect(parties).toContain("Recenzja kredytowa")
    expect(page).toContain("CatalogLoadedTable")
    expect(page).toContain("createCreditReview")
    expect(page).toContain("resolveCreditReview")
    expect(page).toContain("decision")
    expect(page).toContain("source_ref")
    expect(page).not.toContain("score")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("credit_limit")
    expect(page).not.toContain("charge.margin")
    expect(page).not.toContain("BIK")
    expect(page).not.toContain("<Money")
  })

  it("ships attach-bureau job without scoring or auto-limit", () => {
    const page = readFileSync(
      path.join(srcRoot, "features/credit-reviews/catalog-page.tsx"),
      "utf8",
    )
    const api = readFileSync(path.join(srcRoot, "lib/credit-reviews-api.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(page).toContain("Dołącz raport")
    expect(page).toContain("attachCreditReviewBureau")
    expect(page).toContain("bureau_attachment_ref")
    expect(page).not.toContain("risk_score")
    expect(page).not.toContain("credit_limit")
    expect(api).toContain("/attach-bureau")
    expect(api).not.toContain("http://")
    expect(ops).toContain('"88.0": "/credit-reviews"')
  })
})

describe("creditReviewAttachBureauBody", () => {
  it("trims the bureau pointer and does not send source_ref", () => {
    expect(
      creditReviewAttachBureauBody({
        bureauAttachmentRef: "  file://wywiad/raport-1  ",
      }),
    ).toEqual({
      bureau_attachment_ref: "file://wywiad/raport-1",
    })
  })
})
