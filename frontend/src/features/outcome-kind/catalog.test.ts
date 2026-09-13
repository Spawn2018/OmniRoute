import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { makeOutcomeKindPayload } from "@/lib/outcome-kinds-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("makeOutcomeKindPayload", () => {
  it("trims kind fields without money math", () => {
    expect(
      makeOutcomeKindPayload({
        kindCode: " tender ",
        sourceRef: "tenant:manual",
      }),
    ).toEqual({
      kind_code: "tender",
      source_ref: "tenant:manual",
    })
  })
})

describe("outcome_kind surface for 441.0", () => {
  it("records an open kind on /outcome-kinds without Money", () => {
    const page = src("features/outcome-kind/catalog-page.tsx")
    const panel = src("features/outcome-kind/kind-form.tsx")
    expect(src("routes/outcome-kinds.tsx")).toContain("/outcome-kinds")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/outcome-kinds"')
    expect(src("lib/business-lists.ts")).toContain("outcomeKind")
    expect(page).toContain('data-outcome-kind="desk"')
    expect(page).toContain("OutcomeKindComposer")
    expect(panel).toContain("createOutcomeKind")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz rodzaj wyniku")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"441.0": "/outcome-kinds"')
  })
})
