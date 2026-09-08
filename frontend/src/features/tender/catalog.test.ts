import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { sideWrite } from "@/lib/tenders-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("sideWrite", () => {
  it("trims board fields without parsing money", () => {
    expect(
      sideWrite({
        sideStamp: " sell ",
        kindStamp: "open",
        statusStamp: "draft",
        buyerStamp: " 11111111-1111-1111-1111-111111111111 ",
        untilStamp: "2026-12-31",
        termStamp: "FOB",
        tradeStamp: "export",
        placeStamp: " Gdynia ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      side: "sell",
      kind: "open",
      status: "draft",
      buyer_party_id: "11111111-1111-1111-1111-111111111111",
      deadline_at: "2026-12-31",
      incoterm: "FOB",
      trade_side: "export",
      named_place: "Gdynia",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender surface for 169.0", () => {
  it("records tender header on /tenders without auto-award", () => {
    const page = src("features/tender/catalog-page.tsx")
    const panel = src("features/tender/side-form.tsx")
    expect(src("routes/tenders.tsx")).toContain("/tenders")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tenders"')
    expect(src("lib/business-lists.ts")).toContain("tender:")
    expect(page).toContain('data-tender="desk"')
    expect(page).toContain("SidePanel")
    expect(panel).toContain("persistSideMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz przetarg")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"169.0": "/tenders"')
  })
})
