import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { circleWrite } from "@/lib/circle-sims-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("circleWrite", () => {
  it("trims HITL fields without money math or km", () => {
    expect(
      circleWrite({
        codeStamp: " backhaul_a ",
        unloadStamp: " plgdy ",
        loadStamp: " deham ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      sim_code: "backhaul_a",
      unload_unlocode: "plgdy",
      load_unlocode: "deham",
      source_ref: "tenant:manual",
    })
  })
})

describe("circle_sim surface for 266.0", () => {
  it("records a HITL circle on /circle-sims without Money or map", () => {
    const page = src("features/circle-sim/catalog-page.tsx")
    const panel = src("features/circle-sim/circle-form.tsx")
    expect(src("routes/circle-sims.tsx")).toContain("/circle-sims")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/circle-sims"')
    expect(src("lib/business-lists.ts")).toContain("circleSim")
    expect(page).toContain('data-circle-sim="desk"')
    expect(page).toContain("CircleDesk")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("CatalogHeading")
    expect(panel).toContain("persistCircleSim")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz kółko")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"266.0": "/circle-sims"')
    expect(src("features/ops/ops-index.ts")).toContain('"454.0": "/circle-sims"')
    expect(page).toContain("listCircleSimPairs")
    expect(page).toContain("para zamyka się w SQL")
  })
})
