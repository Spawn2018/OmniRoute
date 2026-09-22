import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("shipment document surface for 31.0 and 92.0", () => {
  it("keeps /shipment-documents without PDF or HBL", () => {
    const page = readFileSync(path.join(srcRoot, "features/shipment-document/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/shipment-documents.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/shipment-documents")
    expect(nav).toContain("/shipment-documents")
    expect(lists).toContain("shipmentDocument")
    expect(ops).toContain("/shipment-documents")
    expect(page).toContain('data-shipment-document="board"')
    expect(page).toContain("source_ref")
    expect(page).not.toContain("pdf")
    expect(page).not.toContain("print")
    expect(page).not.toContain("hbl")
    expect(page).not.toContain("CatalogCreateForm")
  })

  it("records 92.0 as live shipment documents on /shipment-documents", () => {
    const page = readFileSync(path.join(srcRoot, "features/shipment-document/catalog-page.tsx"), "utf8")
    const api = readFileSync(path.join(srcRoot, "lib/shipment-documents-api.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(ops).toContain('"92.0": "/shipment-documents"')
    expect(ops).toContain('"624.0": "/shipment-documents"')
    expect(api).toContain("createShipmentDocument")
    expect(page).toContain("fetchShipmentDocuments")
    expect(page).toContain("Zapisz dokument")
    expect(page).not.toContain("quotationAcceptancePending")
    expect(page).not.toContain("fetchQuotations")
  })
})
