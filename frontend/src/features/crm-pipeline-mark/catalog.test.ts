import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function src(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("crm_pipeline_mark surface for 490.0", () => {
  it("ships the catalog route and forbids amount copy", () => {
    expect(src("features/ops/ops-index.ts")).toContain('"490.0": "/crm-pipeline-marks"')
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/crm-pipeline-marks"')
    expect(src("routes/crm-pipeline-marks.tsx")).toContain("CrmPipelineMarkDesk")
    expect(src("lib/crm-pipeline-marks-api.ts")).not.toContain("amount")
  })
})
