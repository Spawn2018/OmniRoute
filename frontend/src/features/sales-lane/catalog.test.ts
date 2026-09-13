import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function src(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("sales_lane surface for 460.0", () => {
  it("ships the catalog route and forbids amount copy", () => {
    expect(src("features/ops/ops-index.ts")).toContain('"460.0": "/sales-lanes"')
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/sales-lanes"')
    expect(src("routes/sales-lanes.tsx")).toContain("SalesLaneDesk")
    expect(src("lib/sales-lanes-api.ts")).not.toContain("amount")
  })
})
