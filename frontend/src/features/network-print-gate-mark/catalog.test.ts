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

describe("632.0 network_print_gate_mark wiring", () => {
  it("locks SHIPPED to network-print-gate-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["632.0"]).toBe("/network-print-gate-marks")
  })

  it("registers ops path, sidebar, desk and keeps API amount-free", () => {
    const opsIndex = load("features/ops/ops-index.ts")
    const sidebar = load("components/layout/sidebar.tsx")
    const routeFile = load("routes/network-print-gate-marks.tsx")
    const client = load("lib/network-print-gate-marks-api.ts")
    expect(opsIndex).toContain('"632.0": "/network-print-gate-marks"')
    expect(sidebar).toContain('to: "/network-print-gate-marks"')
    expect(routeFile).toContain("NetworkPrintGateMarkDesk")
    expect(client.includes("amount") || client.includes("margin")).toBe(false)
  })
})
