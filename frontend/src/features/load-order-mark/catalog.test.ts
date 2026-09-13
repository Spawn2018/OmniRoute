import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const here = path.dirname(fileURLToPath(import.meta.url))
const frontendSrc = path.resolve(here, "../..")

describe("464.0 load_order_mark operator surface", () => {
  it("registers the HITL list and keeps amount out of the client", () => {
    const ops = readFileSync(path.join(frontendSrc, "features/ops/ops-index.ts"), "utf8")
    const side = readFileSync(path.join(frontendSrc, "components/layout/sidebar.tsx"), "utf8")
    const route = readFileSync(path.join(frontendSrc, "routes/load-order-marks.tsx"), "utf8")
    const client = readFileSync(path.join(frontendSrc, "lib/load-order-marks-api.ts"), "utf8")
    expect(ops.includes('"464.0": "/load-order-marks"')).toBe(true)
    expect(side.includes('to: "/load-order-marks"')).toBe(true)
    expect(route.includes("LoadOrderMarkDesk")).toBe(true)
    expect(client.includes("amount")).toBe(false)
  })
})
