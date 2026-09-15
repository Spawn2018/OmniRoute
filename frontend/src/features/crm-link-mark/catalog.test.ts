import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function readSrc(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("crm_link_mark surface for 496.0", () => {
  it("ships the catalog route and forbids amount copy", () => {
    const ops = readSrc("features/ops/ops-index.ts")
    const side = readSrc("components/layout/sidebar.tsx")
    const route = readSrc("routes/crm-link-marks.tsx")
    const api = readSrc("lib/crm-link-marks-api.ts")
    expect(ops.includes('"496.0": "/crm-link-marks"')).toBe(true)
    expect(side.includes('to: "/crm-link-marks"')).toBe(true)
    expect(route.includes("CrmLinkMarkDesk")).toBe(true)
    expect(api.includes("amount")).toBe(false)
  })
})
