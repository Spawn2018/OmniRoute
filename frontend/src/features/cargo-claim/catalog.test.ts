import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("cargo claim surface for 645.0", () => {
  it("records a cargo_claim on /claims with OS&D, CMR dates and evidence HITL", () => {
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
    expect(page).toContain("evidence_gps")
    expect(page).toContain("evidence_temp")
    expect(page).toContain("evidence_photo")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("leaflet")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("timedelta")
    expect(src("features/ops/ops-index.ts")).toContain('"113.0": "/claims"')
    expect(src("features/ops/ops-index.ts")).toContain('"191.0": "/claims"')
    expect(SHIPPED_CHARGE_ROUTES["645.0"]).toBe("/claims")
  })
})
