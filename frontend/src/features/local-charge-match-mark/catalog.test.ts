import { readFileSync } from "node:fs"
import { join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

const here = fileURLToPath(new URL(".", import.meta.url))
const srcRoot = join(here, "../..")

function load(rel: string): string {
  return readFileSync(join(srcRoot, rel), "utf8")
}

describe("640.0 local_charge_match_mark wiring", () => {
  it("locks SHIPPED to local-charge-match-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["640.0"]).toBe("/local-charge-match-marks")
  })

  it("registers ops path, sidebar, desk and keeps API amount-free", () => {
    const opsIndex = load("features/ops/ops-index.ts")
    const sidebar = load("components/layout/sidebar.tsx")
    const routeFile = load("routes/local-charge-match-marks.tsx")
    const client = load("lib/local-charge-match-marks-api.ts")
    expect(opsIndex).toContain('"640.0": "/local-charge-match-marks"')
    expect(sidebar).toContain('to: "/local-charge-match-marks"')
    expect(routeFile).toContain("LocalChargeMatchMarkDesk")
    expect(client.includes("amount")).toBe(false)
    expect(client).toContain("local-charge-match-marks")
  })
})
