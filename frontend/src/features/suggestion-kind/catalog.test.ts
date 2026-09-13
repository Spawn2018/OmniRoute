import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { makeSuggestionKindPayload } from "@/lib/suggestion-kinds-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("makeSuggestionKindPayload", () => {
  it("trims kind fields without money math", () => {
    expect(
      makeSuggestionKindPayload({
        kindCode: " tender_twin ",
        sourceRef: "tenant:manual",
      }),
    ).toEqual({
      kind_code: "tender_twin",
      source_ref: "tenant:manual",
    })
  })
})

describe("suggestion_kind surface for 436.0", () => {
  it("records an open kind on /suggestion-kinds without Money", () => {
    const page = src("features/suggestion-kind/catalog-page.tsx")
    const panel = src("features/suggestion-kind/ledger-form.tsx")
    expect(src("routes/suggestion-kinds.tsx")).toContain("/suggestion-kinds")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/suggestion-kinds"')
    expect(src("lib/business-lists.ts")).toContain("suggestionKind")
    expect(page).toContain('data-suggestion-kind="desk"')
    expect(page).toContain("SuggestionKindComposer")
    expect(panel).toContain("createSuggestionKind")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz rodzaj podpowiedzi")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"436.0": "/suggestion-kinds"')
  })
})
