import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { erpConnectorWrite } from "@/lib/erp-connectors-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("erpConnectorWrite", () => {
  it("trims HITL fields without money math or SOAP", () => {
    expect(
      erpConnectorWrite({
        codeStamp: " optima_biuro ",
        kindStamp: " optima ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      connector_code: "optima_biuro",
      system_kind: "optima",
      source_ref: "tenant:manual",
    })
  })
})

describe("erp_connector surface for 268.0", () => {
  it("records HITL Optima fixture on /erp-connectors without Money or SOAP", () => {
    const page = src("features/erp-connector/catalog-page.tsx")
    const panel = src("features/erp-connector/erp-connector-form.tsx")
    expect(src("routes/erp-connectors.tsx")).toContain("/erp-connectors")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/erp-connectors"')
    expect(src("lib/business-lists.ts")).toContain("erpConnector")
    expect(page).toContain('data-erp-connector="desk"')
    expect(page).toContain("ErpConnectorDesk")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("CatalogHeading")
    expect(panel).toContain("persistErpConnector")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz konektor Optima")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("httpx")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"268.0": "/erp-connectors"')
  })
})
