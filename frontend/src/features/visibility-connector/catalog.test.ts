import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { visibilityFixtureBody } from "@/lib/visibility-connectors-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("visibilityFixtureBody", () => {
  it("trims HITL slug, vendor token and origin", () => {
    expect(
      visibilityFixtureBody({
        deskSlug: " p44_desk_pl ",
        vendorToken: " p44 ",
        originPointer: "tenant:manual",
      }),
    ).toEqual({
      connector_code: "p44_desk_pl",
      system_kind: "p44",
      source_ref: "tenant:manual",
    })
  })
})

describe("visibility_connector surface for 275.0/294.0", () => {
  it("records HITL vendor tokens on /visibility-connectors without secret fields", () => {
    const page = src("features/visibility-connector/catalog-page.tsx")
    const panel = src("features/visibility-connector/visibility-connector-form.tsx")
    const client = src("lib/visibility-connectors-api.ts")
    expect(src("routes/visibility-connectors.tsx")).toContain("/visibility-connectors")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/visibility-connectors"')
    expect(src("lib/business-lists.ts")).toContain("visibilityConnector")
    expect(page).toContain('data-visibility-fixture="board"')
    expect(page).toContain("VisibilityConnectorDesk")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("CatalogHeading")
    expect(panel).toContain("persistVisibilityConnector")
    expect(panel).toContain("Zapisz konektor widoczności")
    expect(panel).toContain('type="radio"')
    expect(panel).toContain("fourkites")
    expect(panel).toContain("shippeo")
    expect(panel).not.toContain("<Money")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("api_key")
    expect(panel).not.toContain("Śledź live")
    expect(client).not.toContain("ciphertext")
    expect(client).not.toContain("base_url")
    expect(src("features/ops/ops-index.ts")).toContain('"275.0": "/visibility-connectors"')
  })
})
