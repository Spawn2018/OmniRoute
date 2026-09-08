import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { cellWrite } from "@/lib/tender-matrix-cells-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("cellWrite", () => {
  it("trims cell fields without parsing money", () => {
    expect(
      cellWrite({
        boardStamp: " 11111111-1111-1111-1111-111111111111 ",
        codeStamp: " ocean_fcl ",
        cashStamp: "10.5000",
        ccyStamp: "eur",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      tender_id: "11111111-1111-1111-1111-111111111111",
      cell_code: "ocean_fcl",
      amount: "10.5000",
      currency: "EUR",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_matrix_cell surface for 174.0", () => {
  it("records Decimal amount on /tender-matrix-cells without LLM or sum", () => {
    const page = src("features/tender-matrix-cell/catalog-page.tsx")
    const panel = src("features/tender-matrix-cell/cell-form.tsx")
    expect(src("routes/tender-matrix-cells.tsx")).toContain("/tender-matrix-cells")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-matrix-cells"')
    expect(src("lib/business-lists.ts")).toContain("tenderMatrixCell")
    expect(page).toContain('data-tender-matrix-cell="desk"')
    expect(page).toContain("CellPanel")
    expect(panel).toContain("persistCellMark")
    expect(panel).toContain("<Money")
    expect(panel).toContain("Zapisz komórkę")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain(".sum(")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"174.0": "/tender-matrix-cells"')
  })
})
