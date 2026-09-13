import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function src(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("tracking_consent surface for 459.0", () => {
  it("ships the catalog route and forbids amount copy", () => {
    expect(src("features/ops/ops-index.ts")).toContain('"459.0": "/tracking-consents"')
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tracking-consents"')
    expect(src("routes/tracking-consents.tsx")).toContain("TrackingConsentDesk")
    expect(src("lib/tracking-consents-api.ts")).not.toContain("amount")
  })
})
