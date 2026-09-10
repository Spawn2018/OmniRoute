import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { idpConnectorWrite } from "@/lib/idp-connectors-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("idpConnectorWrite", () => {
  it("trims HITL fields and blanks the optional host", () => {
    expect(
      idpConnectorWrite({
        markCode: " auth0_eu_desk ",
        providerToken: " auth0 ",
        hostLabel: "  ",
        originHint: "tenant:manual",
      }),
    ).toEqual({
      connector_code: "auth0_eu_desk",
      provider_code: "auth0",
      public_domain: null,
      source_ref: "tenant:manual",
    })
  })
})

describe("idp_connector surface for 270.0", () => {
  it("records HITL Auth0 fixture on /idp-connectors without login or OAuth", () => {
    const page = src("features/idp-connector/catalog-page.tsx")
    const panel = src("features/idp-connector/idp-connector-form.tsx")
    expect(src("routes/idp-connectors.tsx")).toContain("/idp-connectors")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/idp-connectors"')
    expect(src("lib/business-lists.ts")).toContain("idpConnector")
    expect(page).toContain('data-idp-connector="board"')
    expect(page).toContain("IdpConnectorDesk")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("CatalogHeading")
    expect(panel).toContain("persistIdpConnector")
    expect(panel).toContain("Zapisz konektor Auth0")
    expect(panel).not.toContain("<Money")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("httpx")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(panel).not.toContain("Zaloguj")
    expect(panel).not.toContain("OAuth")
    expect(panel).not.toContain("redirect")
    expect(src("features/ops/ops-index.ts")).toContain('"270.0": "/idp-connectors"')
    expect(src("lib/idp-connectors-api.ts")).not.toContain("client_secret")
  })
})
