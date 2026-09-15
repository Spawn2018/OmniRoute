import { readFileSync } from "node:fs"
import { join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const here = fileURLToPath(new URL(".", import.meta.url))
const srcRoot = join(here, "../..")

function load(rel: string): string {
  return readFileSync(join(srcRoot, rel), "utf8")
}

describe("498.0 shipper_bind_mark wiring", () => {
  it("registers ops path, sidebar, desk and keeps API amount-free", () => {
    const opsIndex = load("features/ops/ops-index.ts")
    const sidebar = load("components/layout/sidebar.tsx")
    const routeFile = load("routes/shipper-bind-marks.tsx")
    const client = load("lib/shipper-bind-marks-api.ts")
    expect(opsIndex).toContain('"498.0": "/shipper-bind-marks"')
    expect(sidebar).toContain('to: "/shipper-bind-marks"')
    expect(routeFile).toContain("ShipperBindMarkDesk")
    expect(client.includes("amount") || client.includes("margin")).toBe(false)
  })
})
