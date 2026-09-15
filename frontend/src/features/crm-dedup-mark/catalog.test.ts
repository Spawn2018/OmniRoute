import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function readSrc(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("crm_dedup_mark surface for 495.0", () => {
  it("ships the catalog route and forbids amount copy", () => {
    const ops = readSrc("features/ops/ops-index.ts")
    const side = readSrc("components/layout/sidebar.tsx")
    const route = readSrc("routes/crm-dedup-marks.tsx")
    const api = readSrc("lib/crm-dedup-marks-api.ts")
    expect(ops.includes('"495.0": "/crm-dedup-marks"')).toBe(true)
    expect(side.includes('to: "/crm-dedup-marks"')).toBe(true)
    expect(route.includes("CrmDedupMarkDesk")).toBe(true)
    expect(api.includes("amount")).toBe(false)
  })
})
