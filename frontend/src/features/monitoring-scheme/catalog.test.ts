import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { schemeWrite } from "@/lib/monitoring-schemes-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("schemeWrite", () => {
  it("trims scheme fields without money math", () => {
    expect(
      schemeWrite({
        codeStamp: " sent ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      scheme_code: "sent",
      source_ref: "tenant:manual",
    })
  })
})

describe("monitoring_scheme surface for 187.0", () => {
  it("records a scheme on /monitoring-schemes without SENT XML or amount", () => {
    const page = src("features/monitoring-scheme/catalog-page.tsx")
    const panel = src("features/monitoring-scheme/scheme-form.tsx")
    expect(src("routes/monitoring-schemes.tsx")).toContain("/monitoring-schemes")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/monitoring-schemes"')
    expect(src("lib/business-lists.ts")).toContain("monitoringScheme")
    expect(page).toContain('data-monitoring-scheme="desk"')
    expect(page).toContain("SchemePanel")
    expect(panel).toContain("persistSchemeMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz schemat monitoringu")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"187.0": "/monitoring-schemes"')
  })
})
