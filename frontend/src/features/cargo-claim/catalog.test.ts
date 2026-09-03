import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("cargo claim surface for 113.0", () => {
  it("records a cargo_claim on /claims", () => {
    const page = src("features/cargo-claim/catalog-page.tsx")
    expect(src("routes/claims.tsx")).toContain("/claims")
    expect(src("components/layout/sidebar.tsx")).toContain("/claims")
    expect(src("lib/business-lists.ts")).toContain("cargoClaim")
    expect(src("features/ops/ops-index.ts")).toContain("/claims")
    expect(page).toContain('data-cargo-claim="board"')
    expect(page).toContain("listCargoClaims")
    expect(page).toContain("saveCargoClaim")
    expect(page).toContain("Zapisz reklamację")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("leaflet")
    expect(page).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"113.0": "/claims"')
  })
})
