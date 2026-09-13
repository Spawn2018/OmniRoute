import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function src(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("position_event surface for 457.0", () => {
  it("ships the catalog route and forbids amount copy", () => {
    expect(src("features/ops/ops-index.ts")).toContain('"457.0": "/position-events"')
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/position-events"')
    expect(src("routes/position-events.tsx")).toContain("PositionEventDesk")
    expect(src("lib/position-events-api.ts")).not.toContain("amount")
  })
})
