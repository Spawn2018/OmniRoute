import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { sheetWrite } from "@/lib/document-templates-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("sheetWrite", () => {
  it("trims layout tokens without parseFloat", () => {
    expect(
      sheetWrite({
        kindToken: " cmr ",
        tongueToken: " en ",
        layoutToken: " cmr-en ",
        exitToken: " html_print ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      template_kind: "cmr",
      language: "en",
      layout_ref: "cmr-en",
      output_kind: "html_print",
      source_ref: "tenant:manual",
    })
  })
})

describe("document_template surface for 162.0", () => {
  it("records a layout token on /document-templates without money", () => {
    const page = src("features/document-template/catalog-page.tsx")
    const panel = src("features/document-template/sheet-panel.tsx")
    expect(src("routes/document-templates.tsx")).toContain("/document-templates")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/document-templates"')
    expect(src("lib/business-lists.ts")).toContain("documentTemplate")
    expect(page).toContain('data-document-template="board"')
    expect(page).toContain("SheetKindPanel")
    expect(panel).toContain("persistSheetMark")
    expect(panel).toContain('data-document-template="sheet-form"')
    expect(panel).toContain("Zapisz szablon wydruku")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(panel).not.toContain("buy_amount")
    expect(src("features/ops/ops-index.ts")).toContain('"162.0": "/document-templates"')
  })
})
