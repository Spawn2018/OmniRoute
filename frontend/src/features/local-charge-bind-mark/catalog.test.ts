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

describe("641.0 local_charge_bind_mark wiring", () => {
  it("locks SHIPPED to local-charge-bind-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["641.0"]).toBe("/local-charge-bind-marks")
  })

  it("registers ops path, sidebar, desk and keeps API amount-free", () => {
    const opsIndex = load("features/ops/ops-index.ts")
    const sidebar = load("components/layout/sidebar.tsx")
    const routeFile = load("routes/local-charge-bind-marks.tsx")
    const client = load("lib/local-charge-bind-marks-api.ts")
    expect(opsIndex).toContain('"641.0": "/local-charge-bind-marks"')
    expect(sidebar).toContain('to: "/local-charge-bind-marks"')
    expect(routeFile).toContain("LocalChargeBindMarkDesk")
    expect(client.includes("amount")).toBe(false)
    expect(client).toContain("local-charge-bind-marks")
  })
})
