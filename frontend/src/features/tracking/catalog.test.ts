import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("tracking surface for 29.0", () => {
  it("ships /tracking as read-only POL/POD lanes without a map", () => {
    const page = readFileSync(path.join(srcRoot, "features/tracking/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/tracking.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/tracking")
    expect(nav).toContain("/tracking")
    expect(lists).toContain("tracking")
    expect(ops).toContain("/tracking")
    expect(page).toContain('data-tracking="board"')
    expect(page).toContain("quotationLanes")
    expect(page).toContain("fetchPorts")
    expect(page).not.toContain("eta")
    expect(page).not.toContain("leaflet")
    expect(page).not.toContain("mapbox")
    expect(page).not.toContain("shipment_leg")
    expect(page).not.toContain("CatalogCreateForm")
  })
})
