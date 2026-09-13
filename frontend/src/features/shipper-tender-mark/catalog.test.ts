import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function src(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("shipper_tender_mark surface for 461.0", () => {
  it("ships the catalog route and forbids amount copy", () => {
    expect(src("features/ops/ops-index.ts")).toContain('"461.0": "/shipper-tender-marks"')
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/shipper-tender-marks"')
    expect(src("routes/shipper-tender-marks.tsx")).toContain("ShipperTenderMarkDesk")
    expect(src("lib/shipper-tender-marks-api.ts")).not.toContain("amount")
  })
})
