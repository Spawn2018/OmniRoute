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

describe("639.0 margin_match_mark wiring", () => {
  it("locks SHIPPED to margin-match-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["639.0"]).toBe("/margin-match-marks")
  })

  it("registers ops path, sidebar, desk and keeps API amount-free", () => {
    const opsIndex = load("features/ops/ops-index.ts")
    const sidebar = load("components/layout/sidebar.tsx")
    const routeFile = load("routes/margin-match-marks.tsx")
    const client = load("lib/margin-match-marks-api.ts")
    expect(opsIndex).toContain('"639.0": "/margin-match-marks"')
    expect(sidebar).toContain('to: "/margin-match-marks"')
    expect(routeFile).toContain("MarginMatchMarkDesk")
    expect(client.includes("amount")).toBe(false)
    expect(client).toContain("margin-match-marks")
  })
})
