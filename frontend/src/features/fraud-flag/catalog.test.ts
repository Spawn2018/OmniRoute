import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("fraud flag surface for 114.0", () => {
  it("records a fraud_flag on /fraud", () => {
    const page = src("features/fraud-flag/catalog-page.tsx")
    expect(src("routes/fraud.tsx")).toContain("/fraud")
    expect(src("components/layout/sidebar.tsx")).toContain("/fraud")
    expect(src("lib/business-lists.ts")).toContain("fraudFlag")
    expect(src("features/ops/ops-index.ts")).toContain("/fraud")
    expect(page).toContain('data-fraud-flag="board"')
    expect(page).toContain("listFraudFlags")
    expect(page).toContain("saveFraudFlag")
    expect(page).toContain("Zapisz flagę")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("leaflet")
    expect(page).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"114.0": "/fraud"')
  })
})
