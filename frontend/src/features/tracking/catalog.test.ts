import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("tracking surface for 29.0 and 91.0", () => {
  it("keeps /tracking without a map or ETA", () => {
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
    expect(page).not.toContain("eta")
    expect(page).not.toContain("leaflet")
    expect(page).not.toContain("mapbox")
    expect(page).not.toContain("shipment_leg")
  })

  it("records 91.0 as live tracking events on /tracking", () => {
    const page = readFileSync(path.join(srcRoot, "features/tracking/catalog-page.tsx"), "utf8")
    const api = readFileSync(path.join(srcRoot, "lib/tracking-events-api.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(ops).toContain('"91.0": "/tracking"')
    expect(api).toContain("createTrackingEvent")
    expect(page).toContain("fetchTrackingEvents")
    expect(page).toContain("Zapisz zdarzenie")
    expect(page).not.toContain("quotationLanes")
    expect(page).not.toContain("fetchPorts")
  })
})
