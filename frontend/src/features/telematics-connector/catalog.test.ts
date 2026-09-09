import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { connectorWrite } from "@/lib/telematics-connectors-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("connectorWrite", () => {
  it("trims regime and provider without money math or coordinates", () => {
    expect(
      connectorWrite({
        kindStamp: " omni_telematic ",
        providerStamp: " ikol ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      observation_kind: "omni_telematic",
      provider_code: "ikol",
      source_ref: "tenant:manual",
    })
  })
})

describe("telematics_connector surface for 197.0", () => {
  it("records a HITL connector on /telematics-connectors without Money or poll", () => {
    const page = src("features/telematics-connector/catalog-page.tsx")
    const panel = src("features/telematics-connector/connector-form.tsx")
    expect(src("routes/telematics-connectors.tsx")).toContain("/telematics-connectors")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/telematics-connectors"')
    expect(src("lib/business-lists.ts")).toContain("telematicsConnector")
    expect(page).toContain('data-telematics-connector="desk"')
    expect(page).toContain("ConnectorPanel")
    expect(panel).toContain("persistConnectorMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz konektor GPS")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("lng")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"197.0": "/telematics-connectors"')
  })
})
