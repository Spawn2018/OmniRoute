import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function src(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("crm_activity surface for 489.0", () => {
  it("ships the catalog route and forbids pipeline copy", () => {
    expect(src("features/ops/ops-index.ts")).toContain('"489.0": "/crm-activities"')
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/crm-activities"')
    expect(src("routes/crm-activities.tsx")).toContain("CrmActivityDesk")
    expect(src("lib/crm-activities-api.ts")).not.toContain("pipeline")
    expect(src("lib/crm-activities-api.ts")).not.toContain("amount")
  })
})
