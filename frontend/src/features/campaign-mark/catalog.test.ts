import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function src(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("campaign_mark surface for 462.0", () => {
  it("ships the catalog route and forbids amount copy", () => {
    expect(src("features/ops/ops-index.ts")).toContain('"462.0": "/campaign-marks"')
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/campaign-marks"')
    expect(src("routes/campaign-marks.tsx")).toContain("CampaignMarkDesk")
    expect(src("lib/campaign-marks-api.ts")).not.toContain("amount")
  })
})
