import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

function readSource(rel: string): string {
  return readFileSync(path.join(srcRoot, rel), "utf8")
}

describe("watchtower surface for 94.0", () => {
  it("ships /watchtower as exceptions plus pending S11 without a map library", () => {
    const page = readSource("features/watchtower/catalog-page.tsx")
    const panel = readSource("features/watchtower/map-panel.tsx")
    const route = readSource("routes/watchtower.tsx")
    const nav = readSource("components/layout/sidebar.tsx")
    const lists = readSource("lib/business-lists.ts")
    const ops = readSource("features/ops/ops-index.ts")
    expect(route).toContain("/watchtower")
    expect(nav).toContain("/watchtower")
    expect(lists).toContain("watchtower")
    expect(ops).toContain("/watchtower")
    expect(ops).toContain('"94.0": "/watchtower"')
    expect(page).toContain('data-watchtower="board"')
    expect(page).toContain("fetchOperationalExceptions")
    expect(page).toContain("fetchOperatorDecisions")
    expect(page).toContain("decideOperatorDecision")
    expect(page).toContain("Akceptuj")
    expect(page).toContain("Odrzuć")
    expect(page).toContain("lock_version")
    expect(page).toContain('to="/ai"')
    expect(page).toContain("lazy(() => import(")
    expect(page).toContain("@/features/watchtower/map-panel")
    expect(page).not.toContain('from "@/features/watchtower/map-panel"')
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("eta")
    expect(page).not.toContain("ais")
    expect(page).not.toContain("leaflet")
    expect(page).not.toContain("mapbox")
    expect(panel).toContain("Mapa poza paczką początkową")
    expect(panel).toContain('data-watchtower-map="panel"')
    expect(panel).not.toContain("eta")
    expect(panel).not.toContain("ais")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("mapbox")
  })
})
