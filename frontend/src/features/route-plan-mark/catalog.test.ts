import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function src(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("route_plan_mark surface for 455.0", () => {
  it("ships the catalog route and forbids live solver copy", () => {
    expect(src("features/ops/ops-index.ts")).toContain('"455.0": "/route-plan-marks"')
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/route-plan-marks"')
    expect(src("routes/route-plan-marks.tsx")).toContain("RoutePlanMarkDesk")
    expect(src("lib/route-plan-marks-api.ts")).not.toContain("valhalla")
    expect(src("lib/route-plan-marks-api.ts")).not.toContain("amount")
  })
})
