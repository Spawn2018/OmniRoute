import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function src(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("groupage_dispatcher_mark surface for 463.0", () => {
  it("ships the catalog route and forbids amount copy", () => {
    expect(src("features/ops/ops-index.ts")).toContain(
      '"463.0": "/groupage-dispatcher-marks"',
    )
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/groupage-dispatcher-marks"')
    expect(src("routes/groupage-dispatcher-marks.tsx")).toContain("GroupageDispatcherMarkDesk")
    expect(src("lib/groupage-dispatcher-marks-api.ts")).not.toContain("amount")
  })
})
