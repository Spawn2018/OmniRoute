import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("planning map surface for 261.0", () => {
  it("ships /planning with a lazy trip overlay and no tile library", () => {
    const page = src("features/planning/catalog-page.tsx")
    const panel = src("features/planning/map-panel.tsx")
    const ops = src("features/ops/ops-index.ts")
    expect(src("routes/planning.tsx")).toMatch(/\/planning/)
    expect(src("components/layout/sidebar.tsx")).toMatch(/to: "\/planning"/)
    expect(src("lib/business-lists.ts")).toMatch(/planning:/)
    expect(page).toMatch(/data-planning="board"/)
    expect(page).toMatch(/lazy\(\(\) => import\("/)
    expect(page).toMatch(/@\/features\/planning\/map-panel/)
    expect(page).not.toMatch(/from "@\/features\/planning\/map-panel"/)
    expect(page).toMatch(/data-planning="gate"/)
    expect(panel).toMatch(/data-planning="map"/)
    expect(panel).toMatch(/fetchTrips/)
    expect(panel).toMatch(/planning-trip-labels/)
    expect(/leaflet|mapbox|tile\.openstreetmap\.org|parseFloat|buy_amount/.test(page + panel)).toBe(
      false,
    )
    expect(ops).toMatch(/"261\.0": "\/planning"/)
  })
})
