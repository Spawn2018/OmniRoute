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

describe("637.0 handover_bind_mark wiring", () => {
  it("locks SHIPPED to handover-bind-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["637.0"]).toBe("/handover-bind-marks")
  })

  it("registers ops path, sidebar, desk and keeps API amount-free", () => {
    const opsIndex = load("features/ops/ops-index.ts")
    const sidebar = load("components/layout/sidebar.tsx")
    const routeFile = load("routes/handover-bind-marks.tsx")
    const client = load("lib/handover-bind-marks-api.ts")
    expect(opsIndex).toContain('"637.0": "/handover-bind-marks"')
    expect(sidebar).toContain('to: "/handover-bind-marks"')
    expect(routeFile).toContain("HandoverBindMarkDesk")
    expect(client.includes("amount") || client.includes("margin")).toBe(false)
  })
})
