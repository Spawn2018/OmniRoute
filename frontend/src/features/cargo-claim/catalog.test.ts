import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("cargo claim surface for 191.0", () => {
  it("records a cargo_claim on /claims with OS&D and CMR dates", () => {
    const page = src("features/cargo-claim/catalog-page.tsx")
    expect(src("routes/claims.tsx")).toContain("/claims")
    expect(src("components/layout/sidebar.tsx")).toContain("/claims")
    expect(src("lib/business-lists.ts")).toContain("cargoClaim")
    expect(src("features/ops/ops-index.ts")).toContain("/claims")
    expect(page).toContain('data-cargo-claim="board"')
    expect(page).toContain("listCargoClaims")
    expect(page).toContain("saveCargoClaim")
    expect(page).toContain("Zapisz reklamację")
    expect(page).toContain("damage_code")
    expect(page).toContain("notice_due_at")
    expect(page).toContain("suit_due_at")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("leaflet")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("timedelta")
    expect(src("features/ops/ops-index.ts")).toContain('"113.0": "/claims"')
    expect(src("features/ops/ops-index.ts")).toContain('"191.0": "/claims"')
  })
})
