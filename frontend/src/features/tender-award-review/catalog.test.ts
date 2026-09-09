import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { awardReviewWrite } from "@/lib/tender-award-reviews-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("awardReviewWrite", () => {
  it("trims award-review fields without money math", () => {
    expect(
      awardReviewWrite({
        boardStamp: " 11111111-1111-1111-1111-111111111111 ",
        reviewStamp: " challenge ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      tender_id: "11111111-1111-1111-1111-111111111111",
      review_code: "challenge",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_award_review surface for 182.0", () => {
  it("records four-eyes on /tender-award-reviews without auto-award or amount", () => {
    const page = src("features/tender-award-review/catalog-page.tsx")
    const panel = src("features/tender-award-review/review-form.tsx")
    expect(src("routes/tender-award-reviews.tsx")).toContain("/tender-award-reviews")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-award-reviews"')
    expect(src("lib/business-lists.ts")).toContain("tenderAwardReview")
    expect(page).toContain('data-tender-award-review="desk"')
    expect(page).toContain("AwardReviewPanel")
    expect(panel).toContain("persistAwardReviewMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz przegląd")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"182.0": "/tender-award-reviews"')
  })
})
