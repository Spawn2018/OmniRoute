import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { stanceWrite } from "@/lib/tender-bid-stances-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("stanceWrite", () => {
  it("trims bid-stance fields without money math", () => {
    expect(
      stanceWrite({
        boardStamp: " 11111111-1111-1111-1111-111111111111 ",
        stanceStamp: " no_bid ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      tender_id: "11111111-1111-1111-1111-111111111111",
      stance_code: "no_bid",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_bid_stance surface for 181.0", () => {
  it("records a stance on /tender-bid-stances without auto-award or amount", () => {
    const page = src("features/tender-bid-stance/catalog-page.tsx")
    const panel = src("features/tender-bid-stance/stance-form.tsx")
    expect(src("routes/tender-bid-stances.tsx")).toContain("/tender-bid-stances")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-bid-stances"')
    expect(src("lib/business-lists.ts")).toContain("tenderBidStance")
    expect(page).toContain('data-tender-bid-stance="desk"')
    expect(page).toContain("StancePanel")
    expect(panel).toContain("persistStanceMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz udział")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"181.0": "/tender-bid-stances"')
  })
})
