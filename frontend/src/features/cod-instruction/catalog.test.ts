import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { collectionWrite } from "@/lib/cod-instructions-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("collectionWrite", () => {
  it("trims COD marker fields without parsing money", () => {
    expect(
      collectionWrite({
        haulToken: "  ship  ",
        markerToken: "cod_west",
        cashStage: "collected",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      shipment_id: "ship",
      instruction_code: "cod_west",
      collection_status: "collected",
      source_ref: "tenant:manual",
    })
  })
})

describe("cod_instruction surface for 158.0", () => {
  it("records a COD marker on /cod without collection amount", () => {
    const page = src("features/cod-instruction/catalog-page.tsx")
    const panel = src("features/cod-instruction/collection-form.tsx")
    expect(src("routes/cod.tsx")).toContain("/cod")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/cod"')
    expect(src("lib/business-lists.ts")).toContain("codInstruction")
    expect(page).toContain('data-cod="board"')
    expect(page).toContain("CollectionMarkPanel")
    expect(panel).toContain("persistCodMark")
    expect(panel).toContain('data-cod="mark-form"')
    expect(panel).toContain("Zapisz instrukcję pobrania")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(panel).not.toContain("buy_amount")
    expect(src("features/ops/ops-index.ts")).toContain('"158.0": "/cod"')
  })
})
