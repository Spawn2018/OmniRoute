import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("shipment document surface for 31.0", () => {
  it("ships /shipment-documents as read-only source_ref without PDF", () => {
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
    expect(page).toContain("quotationAcceptancePending")
    expect(page).toContain("source_ref")
    expect(page).not.toContain("pdf")
    expect(page).not.toContain("print")
    expect(page).not.toContain("hbl")
    expect(page).not.toContain("CatalogCreateForm")
  })
})
