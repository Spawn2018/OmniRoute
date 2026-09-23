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

describe("638.0 trip_variance_mark wiring", () => {
  it("locks SHIPPED to trip-variance-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["638.0"]).toBe("/trip-variance-marks")
  })

  it("registers ops path, sidebar, desk and keeps API amount-free", () => {
    const opsIndex = load("features/ops/ops-index.ts")
    const sidebar = load("components/layout/sidebar.tsx")
    const routeFile = load("routes/trip-variance-marks.tsx")
    const client = load("lib/trip-variance-marks-api.ts")
    expect(opsIndex).toContain('"638.0": "/trip-variance-marks"')
    expect(sidebar).toContain('to: "/trip-variance-marks"')
    expect(routeFile).toContain("TripVarianceMarkDesk")
    expect(client.includes("amount") || client.includes("margin")).toBe(false)
  })
})
