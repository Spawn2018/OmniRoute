import { readFileSync } from "node:fs"
import { join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const here = fileURLToPath(new URL(".", import.meta.url))
const srcRoot = join(here, "../..")

function load(rel: string): string {
  return readFileSync(join(srcRoot, rel), "utf8")
}

describe("497.0 sales_bind_mark wiring", () => {
  it("registers ops path, sidebar, desk and keeps API amount-free", () => {
    const opsIndex = load("features/ops/ops-index.ts")
    const sidebar = load("components/layout/sidebar.tsx")
    const routeFile = load("routes/sales-bind-marks.tsx")
    const client = load("lib/sales-bind-marks-api.ts")
    expect(opsIndex).toContain('"497.0": "/sales-bind-marks"')
    expect(sidebar).toContain('to: "/sales-bind-marks"')
    expect(routeFile).toContain("SalesBindMarkDesk")
    expect(client.includes("amount") || client.includes("margin")).toBe(false)
  })
})
