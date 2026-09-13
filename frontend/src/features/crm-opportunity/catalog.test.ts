import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function src(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("crm_opportunity surface for 456.0", () => {
  it("ships the catalog route and forbids pipeline copy", () => {
    expect(src("features/ops/ops-index.ts")).toContain('"456.0": "/crm-opportunities"')
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/crm-opportunities"')
    expect(src("routes/crm-opportunities.tsx")).toContain("CrmOpportunityDesk")
    expect(src("lib/crm-opportunities-api.ts")).not.toContain("pipeline")
    expect(src("lib/crm-opportunities-api.ts")).not.toContain("amount")
  })
})
