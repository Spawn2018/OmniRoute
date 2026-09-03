import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("shipment surface for 28.0 and 90.0", () => {
  it("keeps /shipments job without legs or HBL", () => {
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
    expect(page).not.toContain("shipment_leg")
    expect(page).not.toContain("hbl")
    expect(page).not.toContain("acceptExtractionDraft")
  })

  it("records 90.0 as a live shipment table on /shipments", () => {
    const page = readFileSync(path.join(srcRoot, "features/shipment/catalog-page.tsx"), "utf8")
    const api = readFileSync(path.join(srcRoot, "lib/shipments-api.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(ops).toContain('"90.0": "/shipments"')
    expect(api).toContain("createShipment")
    expect(page).toContain("fetchShipments")
    expect(page).toContain("Zapisz zlecenie")
    expect(page).not.toContain("fetchQuotations")
    expect(page).not.toContain("quotationAcceptancePending")
  })
})
