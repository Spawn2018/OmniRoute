import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { rolloutSettings } from "@/lib/organization-settings-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("rolloutSettings", () => {
  it("keeps default_currency and drops other keys", () => {
    expect(
      rolloutSettings([
        { setting_key: "other" },
        { setting_key: "default_currency" },
      ]),
    ).toEqual([{ setting_key: "default_currency" }])
  })
})

describe("tenant rollout surface for 50.0", () => {
  it("ships /rollout as allowlisted settings without a rollout table", () => {
    const page = src("features/tenant-rollout/catalog-page.tsx")
    expect(src("routes/rollout.tsx")).toContain("/rollout")
    expect(src("components/layout/sidebar.tsx")).toContain("/rollout")
    expect(src("lib/business-lists.ts")).toContain("tenantRollout")
    expect(src("features/ops/ops-index.ts")).toContain("/rollout")
    expect(page).toContain('data-tenant-rollout="board"')
    expect(page).toContain('t("tenant_rollout.title")')
    expect(page).not.toContain("Wdrożenie tenanta")
    expect(page).toContain("rolloutSettings")
    expect(page).toContain("fetchOrganizationSettings")
    expect(page).toContain('t("tenant_rollout.subtitle")')
    expect(src("lib/i18n.ts")).toContain("default_currency")
    expect(page).not.toContain("upsertOrganizationSetting")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
  })
})
