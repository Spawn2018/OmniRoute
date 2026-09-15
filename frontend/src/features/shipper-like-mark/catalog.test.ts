import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const here = dirname(fileURLToPath(import.meta.url))
const srcRoot = join(here, "../../..")

function readSrc(rel: string): string {
  return readFileSync(join(srcRoot, "src", rel), "utf8")
}

describe("shipper_like_mark surface for 494.0", () => {
  it("wires SHIPPED route and blocks amount field", () => {
    const ops = readSrc("features/ops/ops-index.ts")
    const side = readSrc("components/layout/sidebar.tsx")
    const route = readSrc("routes/shipper-like-marks.tsx")
    const api = readSrc("lib/shipper-like-marks-api.ts")
    expect(ops.includes('"494.0": "/shipper-like-marks"')).toBe(true)
    expect(side.includes('to: "/shipper-like-marks"')).toBe(true)
    expect(route.includes("ShipperLikeMarkDesk")).toBe(true)
    expect(api.includes("amount")).toBe(false)
  })
})
