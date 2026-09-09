import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { methodWrite } from "@/lib/carbon-methods-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("methodWrite", () => {
  it("trims carbon method fields without money math", () => {
    expect(
      methodWrite({
        codeStamp: " glec ",
        versionStamp: " 2023 ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      method_code: "glec",
      method_version: "2023",
      source_ref: "tenant:manual",
    })
  })
})

describe("carbon_method surface for 190.0", () => {
  it("records a GLEC method on /carbon-methods without kg or amount", () => {
    const page = src("features/carbon-method/catalog-page.tsx")
    const panel = src("features/carbon-method/method-form.tsx")
    expect(src("routes/carbon-methods.tsx")).toContain("/carbon-methods")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/carbon-methods"')
    expect(src("lib/business-lists.ts")).toContain("carbonMethod")
    expect(page).toContain('data-carbon-method="desk"')
    expect(page).toContain("MethodPanel")
    expect(panel).toContain("persistMethodMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz metodykę CO₂")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"190.0": "/carbon-methods"')
  })
})
