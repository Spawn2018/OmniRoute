import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { makeTwinKindPayload } from "@/lib/twin-kinds-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("makeTwinKindPayload", () => {
  it("trims kind fields without money math", () => {
    expect(
      makeTwinKindPayload({
        kindCode: " tender ",
        sourceRef: "tenant:manual",
      }),
    ).toEqual({
      kind_code: "tender",
      source_ref: "tenant:manual",
    })
  })
})

describe("twin_kind surface for 437.0", () => {
  it("records an open kind on /twin-kinds without Money", () => {
    const page = src("features/twin-kind/catalog-page.tsx")
    const panel = src("features/twin-kind/ledger-form.tsx")
    expect(src("routes/twin-kinds.tsx")).toContain("/twin-kinds")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/twin-kinds"')
    expect(src("lib/business-lists.ts")).toContain("twinKind")
    expect(page).toContain('data-twin-kind="desk"')
    expect(page).toContain("TwinKindComposer")
    expect(panel).toContain("createTwinKind")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz rodzaj bliźniaka")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"437.0": "/twin-kinds"')
  })
})
