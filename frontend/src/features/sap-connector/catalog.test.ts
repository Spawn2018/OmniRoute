import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { sapConnectorBody } from "@/lib/sap-connectors-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("sapConnectorBody", () => {
  it("trims HITL fields and lowercases system", () => {
    expect(
      sapConnectorBody({
        connectorSlug: " sap_pl_01 ",
        systemKind: " Oracle ",
        originPointer: "tenant:manual",
      }),
    ).toEqual({
      connector_code: "sap_pl_01",
      system_kind: "oracle",
      source_ref: "tenant:manual",
    })
  })
})

describe("sap_connector surface for 281.0", () => {
  it("records HITL connector on /sap-connectors without secrets or money", () => {
    const page = src("features/sap-connector/catalog-page.tsx")
    const panel = src("features/sap-connector/sap-connector-form.tsx")
    const client = src("lib/sap-connectors-api.ts")
    expect(src("routes/sap-connectors.tsx")).toContain("/sap-connectors")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/sap-connectors"')
    expect(src("lib/business-lists.ts")).toContain("sapConnector")
    expect(page).toContain('data-sap-connector="board"')
    expect(page).toContain("SapConnectorDesk")
    expect(panel).toContain("persistSapConnector")
    expect(panel).toContain("Zapisz konektor SAP/Oracle")
    expect(panel).not.toContain("<Money")
    expect(panel).not.toContain("base_url")
    expect(client).not.toContain("api_key")
    expect(client).not.toContain("base_url")
    expect(src("features/ops/ops-index.ts")).toContain('"281.0": "/sap-connectors"')
  })
})
