import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { makeOutcomeLedgerPayload } from "@/lib/outcome-ledgers-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("makeOutcomeLedgerPayload", () => {
  it("trims ledger fields without money math", () => {
    expect(
      makeOutcomeLedgerPayload({
        targetBc: " shipment ",
        entityId: " aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa ",
        suggestionId: " bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb ",
        kind: " ETA ",
        actualValue: " 45 ",
        sourceRef: "tenant:manual",
      }),
    ).toEqual({
      target_bc: "shipment",
      entity_id: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
      suggestion_id: "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
      outcome_kind: "eta",
      actual_value: "45",
      source_ref: "tenant:manual",
    })
  })
})

describe("outcome_ledger surface for 433.0", () => {
  it("records an actual on /outcome-ledgers without Money", () => {
    const page = src("features/outcome-ledger/catalog-page.tsx")
    const panel = src("features/outcome-ledger/ledger-form.tsx")
    expect(src("routes/outcome-ledgers.tsx")).toContain("/outcome-ledgers")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/outcome-ledgers"')
    expect(src("lib/business-lists.ts")).toContain("outcomeLedger")
    expect(page).toContain('data-outcome-ledger="desk"')
    expect(page).toContain("OutcomeLedgerComposer")
    expect(panel).toContain("createOutcomeLedger")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz ledger wyniku")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"433.0": "/outcome-ledgers"')
  })
})
