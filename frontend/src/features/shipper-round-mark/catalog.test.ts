import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function src(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("shipper_round_mark surface for 493.0", () => {
  it("ships the catalog route and forbids amount copy", () => {
    expect(src("features/ops/ops-index.ts")).toContain('"493.0": "/shipper-round-marks"')
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/shipper-round-marks"')
    expect(src("routes/shipper-round-marks.tsx")).toContain("ShipperRoundMarkDesk")
    expect(src("lib/shipper-round-marks-api.ts")).not.toContain("amount")
  })
})
