import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { bundleWrite } from "@/lib/charge-templates-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("bundleWrite", () => {
  it("trims pack fields without parsing money", () => {
    expect(
      bundleWrite({
        packToken: " spot_thc ",
        feeToken: " thc ",
        fromStamp: "2026-01-01",
        untilStamp: "2026-12-31",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      template_code: "spot_thc",
      charge_code: "THC",
      valid_from: "2026-01-01",
      valid_until: "2026-12-31",
      source_ref: "tenant:manual",
    })
  })
})

describe("charge_template surface for 164.0", () => {
    it("records a charge_code collection on /charge-templates with SQL overlap exclusion", () => {
    const page = src("features/charge-template/catalog-page.tsx")
    const panel = src("features/charge-template/bundle-form.tsx")
    expect(src("routes/charge-templates.tsx")).toContain("/charge-templates")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/charge-templates"')
    expect(src("lib/business-lists.ts")).toContain("chargeTemplate")
    expect(page).toContain('data-charge-template="desk"')
    expect(page).toContain("BundleSlotPanel")
    expect(panel).toContain("persistBundleSlot")
    expect(panel).toContain("Zapisz szablon opłat")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("<Money")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"164.0": "/charge-templates"')
    expect(src("features/ops/ops-index.ts")).toContain('"206.0": "/charge-templates"')
    expect(page).toContain("exclusion w SQL")
  })
})
