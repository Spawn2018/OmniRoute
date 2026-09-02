import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("shipment surface for 28.0", () => {
  it("ships /shipments as read-only quoted work without a shipment table", () => {
    const page = readFileSync(path.join(srcRoot, "features/shipment/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/shipments.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/shipments")
    expect(nav).toContain("/shipments")
    expect(lists).toContain("shipment")
    expect(ops).toContain("/shipments")
    expect(page).toContain('data-shipment="board"')
    expect(page).toContain("fetchQuotations")
    expect(page).toContain("quotationAcceptancePending")
    expect(page).toContain("Money")
    expect(page).not.toContain("shipment_leg")
    expect(page).not.toContain("hbl")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("acceptExtractionDraft")
  })
})
