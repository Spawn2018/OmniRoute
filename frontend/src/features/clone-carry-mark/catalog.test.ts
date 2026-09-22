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

describe("631.0 clone_carry_mark wiring", () => {
  it("locks SHIPPED to clone-carry-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["631.0"]).toBe("/clone-carry-marks")
  })

  it("registers ops path, sidebar, desk and keeps API amount-free", () => {
    const opsIndex = load("features/ops/ops-index.ts")
    const sidebar = load("components/layout/sidebar.tsx")
    const routeFile = load("routes/clone-carry-marks.tsx")
    const client = load("lib/clone-carry-marks-api.ts")
    expect(opsIndex).toContain('"631.0": "/clone-carry-marks"')
    expect(sidebar).toContain('to: "/clone-carry-marks"')
    expect(routeFile).toContain("CloneCarryMarkDesk")
    expect(client.includes("amount") || client.includes("margin")).toBe(false)
  })
})
