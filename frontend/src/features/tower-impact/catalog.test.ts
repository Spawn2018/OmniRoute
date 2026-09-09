import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { impactWrite } from "@/lib/tower-impacts-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("impactWrite", () => {
  it("trims stage and contract status without money math or scoring", () => {
    expect(
      impactWrite({
        stageStamp: " production ",
        pactStamp: " missing ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      chain_stage: "production",
      contract_data_status: "missing",
      source_ref: "tenant:manual",
    })
  })
})

describe("tower_impact surface for 198.0", () => {
  it("records a HITL chain mark on /tower-impacts without Money or scoring", () => {
    const page = src("features/tower-impact/catalog-page.tsx")
    const panel = src("features/tower-impact/impact-form.tsx")
    expect(src("routes/tower-impacts.tsx")).toContain("/tower-impacts")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tower-impacts"')
    expect(src("lib/business-lists.ts")).toContain("towerImpact")
    expect(page).toContain('data-tower-impact="desk"')
    expect(page).toContain("ImpactPanel")
    expect(panel).toContain("persistImpactMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz skutek wieży")
    expect(panel).toContain("brak danych umowy")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"198.0": "/tower-impacts"')
  })
})
