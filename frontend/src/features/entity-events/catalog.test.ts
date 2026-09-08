import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("entity-event surface for 133.0", () => {
  it("ships /entity-events list without Temporal or live HTTP", () => {
    const page = readFileSync(path.join(srcRoot, "features/entity-events/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/entity-events.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    const api = readFileSync(path.join(srcRoot, "lib/entity-events-api.ts"), "utf8")
    expect(route).toContain("/entity-events")
    expect(nav).toContain("/entity-events")
    expect(lists).toContain("entityEvents")
    expect(ops).toContain("/entity-events")
    expect(page).toContain('data-entity-event="board"')
    expect(page).toContain("recordEntityEvent")
    expect(page).toContain("Zapisz zdarzenie")
    expect(page).not.toContain("temporal")
    expect(page).not.toContain("httpx")
    expect(page).not.toContain("graph.microsoft")
    expect(api).toContain("/api/v1/entity-events")
    expect(api).not.toContain("amount")
  })
})
