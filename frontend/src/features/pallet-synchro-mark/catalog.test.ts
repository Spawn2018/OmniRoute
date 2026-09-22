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

describe("630.0 pallet_synchro_mark wiring", () => {
  it("locks SHIPPED to pallet-synchro-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["630.0"]).toBe("/pallet-synchro-marks")
  })

  it("registers ops path, sidebar, desk and keeps API amount-free", () => {
    const opsIndex = load("features/ops/ops-index.ts")
    const sidebar = load("components/layout/sidebar.tsx")
    const routeFile = load("routes/pallet-synchro-marks.tsx")
    const client = load("lib/pallet-synchro-marks-api.ts")
    expect(opsIndex).toContain('"630.0": "/pallet-synchro-marks"')
    expect(sidebar).toContain('to: "/pallet-synchro-marks"')
    expect(routeFile).toContain("PalletSynchroMarkDesk")
    expect(client.includes("amount") || client.includes("margin")).toBe(false)
  })
})
