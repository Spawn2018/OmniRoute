import { readFileSync } from "node:fs"
import { join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcDir = join(fileURLToPath(new URL("../../", import.meta.url)))

describe("shipper_award_mark · plaster 499.0", () => {
  it("keeps HITL wiring without money fields", () => {
    const ops = readFileSync(join(srcDir, "features/ops/ops-index.ts"), "utf8")
    const nav = readFileSync(join(srcDir, "components/layout/sidebar.tsx"), "utf8")
    const page = readFileSync(join(srcDir, "routes/shipper-award-marks.tsx"), "utf8")
    const client = readFileSync(join(srcDir, "lib/shipper-award-marks-api.ts"), "utf8")
    expect(ops.includes("499.0") && ops.includes("/shipper-award-marks")).toBe(true)
    expect(nav.includes("/shipper-award-marks")).toBe(true)
    expect(page.includes("ShipperAwardMarkDesk")).toBe(true)
    expect(/amount|margin|float/.test(client)).toBe(false)
  })
})
