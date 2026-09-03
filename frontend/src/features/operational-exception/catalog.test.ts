import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("operational exception surface for 30.0 and 93.0", () => {
  it("keeps /exceptions without a map or AIS", () => {
    const page = readFileSync(path.join(srcRoot, "features/operational-exception/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/exceptions.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/exceptions")
    expect(nav).toContain("/exceptions")
    expect(lists).toContain("operationalException")
    expect(ops).toContain("/exceptions")
    expect(page).toContain('data-operational-exception="board"')
    expect(page).not.toContain("eta")
    expect(page).not.toContain("ais")
    expect(page).not.toContain("leaflet")
    expect(page).not.toContain("mapbox")
    expect(page).not.toContain("CatalogCreateForm")
  })

  it("records 93.0 as live operational exceptions on /exceptions", () => {
    const page = readFileSync(path.join(srcRoot, "features/operational-exception/catalog-page.tsx"), "utf8")
    const api = readFileSync(path.join(srcRoot, "lib/operational-exceptions-api.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(ops).toContain('"93.0": "/exceptions"')
    expect(api).toContain("createOperationalException")
    expect(page).toContain("fetchOperationalExceptions")
    expect(page).toContain("Zapisz wyjątek")
    expect(page).not.toContain("quotationOperationalExceptions")
    expect(page).not.toContain("fetchQuotations")
  })
})
