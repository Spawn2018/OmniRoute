import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function src(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("sales_lane surface for 492.0", () => {
  it("ships volume_label and forbids amount", () => {
    expect(src("features/ops/ops-index.ts")).toContain('"492.0": "/sales-lanes"')
    expect(src("lib/sales-lanes-api.ts")).toContain("volume_label")
    expect(src("lib/sales-lanes-api.ts")).not.toContain("amount")
  })
})
