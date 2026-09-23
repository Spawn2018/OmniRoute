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

describe("635.0 local_charge_warning_mark wiring", () => {
  it("locks SHIPPED to local-charge-warning-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["635.0"]).toBe("/local-charge-warning-marks")
  })

  it("registers ops path, sidebar, desk and keeps API amount-free", () => {
    const opsIndex = load("features/ops/ops-index.ts")
    const sidebar = load("components/layout/sidebar.tsx")
    const routeFile = load("routes/local-charge-warning-marks.tsx")
    const client = load("lib/local-charge-warning-marks-api.ts")
    expect(opsIndex).toContain('"635.0": "/local-charge-warning-marks"')
    expect(sidebar).toContain('to: "/local-charge-warning-marks"')
    expect(routeFile).toContain("LocalChargeWarningMarkDesk")
    expect(client.includes("amount") || client.includes("margin")).toBe(false)
  })
})
