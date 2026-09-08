import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { lotWrite } from "@/lib/tender-lots-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("lotWrite", () => {
  it("trims lot fields without parsing money", () => {
    expect(
      lotWrite({
        boardStamp: " 11111111-1111-1111-1111-111111111111 ",
        codeStamp: " LOT-1 ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      tender_id: "11111111-1111-1111-1111-111111111111",
      lot_code: "LOT-1",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_lot surface for 170.0", () => {
  it("records lot code on /tender-lots without auto-award", () => {
    const page = src("features/tender-lot/catalog-page.tsx")
    const panel = src("features/tender-lot/lot-form.tsx")
    expect(src("routes/tender-lots.tsx")).toContain("/tender-lots")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-lots"')
    expect(src("lib/business-lists.ts")).toContain("tenderLot")
    expect(page).toContain('data-tender-lot="desk"')
    expect(page).toContain("LotPanel")
    expect(panel).toContain("persistLotMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz partię")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"170.0": "/tender-lots"')
  })
})
