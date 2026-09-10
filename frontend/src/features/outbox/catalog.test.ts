import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("outbox surface for 79.0", () => {
  it("ships /outbox list without Temporal or live HTTP", () => {
    const page = readFileSync(path.join(srcRoot, "features/outbox/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/outbox.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    const api = readFileSync(path.join(srcRoot, "lib/outbox-events-api.ts"), "utf8")
    expect(route).toContain("/outbox")
    expect(nav).toContain("/outbox")
    expect(lists).toContain("outboxEvents")
    expect(ops).toContain("/outbox")
    expect(ops).toContain('"264.0": "/outbox"')
    expect(page).toContain('data-outbox="board"')
    expect(page).toContain("recordOutboxEvent")
    expect(page).toContain("Zapisz zdarzenie")
    expect(page).not.toContain("temporal")
    expect(page).not.toContain("httpx")
    expect(page).not.toContain("graph.microsoft")
    expect(api).toContain("/api/v1/outbox-events")
    expect(api).not.toContain("amount")
  })
})
