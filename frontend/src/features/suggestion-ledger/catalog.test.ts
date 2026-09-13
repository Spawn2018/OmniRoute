import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { makeSuggestionLedgerPayload } from "@/lib/suggestion-ledgers-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("makeSuggestionLedgerPayload", () => {
  it("trims ledger fields without money math", () => {
    expect(
      makeSuggestionLedgerPayload({
        targetBc: " shipment ",
        entityId: " aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa ",
        kind: " ETA ",
        intervalLow: " 30 ",
        intervalHigh: " 90 ",
        modelVersion: " hist_eta ",
        promptVersion: " prompt_v1 ",
        reaction: " ACCEPT ",
        changedTo: " none ",
        sourceRef: "tenant:manual",
      }),
    ).toEqual({
      target_bc: "shipment",
      entity_id: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
      suggestion_kind: "eta",
      interval_low: "30",
      interval_high: "90",
      model_version: "hist_eta",
      prompt_version: "prompt_v1",
      reaction: "accept",
      changed_to: "none",
      source_ref: "tenant:manual",
    })
  })
})

describe("suggestion_ledger surface for 432.0", () => {
  it("records an interval reaction on /suggestion-ledgers without Money", () => {
    const page = src("features/suggestion-ledger/catalog-page.tsx")
    const panel = src("features/suggestion-ledger/ledger-form.tsx")
    expect(src("routes/suggestion-ledgers.tsx")).toContain("/suggestion-ledgers")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/suggestion-ledgers"')
    expect(src("lib/business-lists.ts")).toContain("suggestionLedger")
    expect(page).toContain('data-suggestion-ledger="desk"')
    expect(page).toContain("SuggestionLedgerComposer")
    expect(panel).toContain("createSuggestionLedger")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz ledger podpowiedzi")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"432.0": "/suggestion-ledgers"')
  })
})
