import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { kekMarkWrite } from "@/lib/tenant-contract-keks-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("kekMarkWrite", () => {
  it("trims HITL slug, wrap token and origin", () => {
    expect(
      kekMarkWrite({
        markSlug: " desk_wrap_pl ",
        wrapToken: " kms ",
        originRef: "tenant:manual",
      }),
    ).toEqual({
      kek_code: "desk_wrap_pl",
      wrap_kind: "kms",
      source_ref: "tenant:manual",
    })
  })
})

describe("tenant_contract_kek surface for 274.0", () => {
  it("records HITL wrap mark on /tenant-contract-keks without secret fields", () => {
    const page = src("features/tenant-contract-kek/catalog-page.tsx")
    const panel = src("features/tenant-contract-kek/tenant-contract-kek-form.tsx")
    const client = src("lib/tenant-contract-keks-api.ts")
    expect(src("routes/tenant-contract-keks.tsx")).toContain("/tenant-contract-keks")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tenant-contract-keks"')
    expect(src("lib/business-lists.ts")).toContain("tenantContractKek")
    expect(page).toContain('data-kek-mark="desk"')
    expect(page).toContain("TenantContractKekDesk")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("CatalogHeading")
    expect(panel).toContain("persistTenantContractKek")
    expect(panel).toContain("Zapisz znacznik KEK")
    expect(panel).not.toContain("<Money")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("type=\"password\"")
    expect(panel).not.toContain("ciphertext")
    expect(panel).not.toContain("unwrap")
    expect(client).not.toContain("ciphertext")
    expect(client).not.toContain("wrapped_dek")
    expect(src("features/ops/ops-index.ts")).toContain('"274.0": "/tenant-contract-keks"')
  })
})
