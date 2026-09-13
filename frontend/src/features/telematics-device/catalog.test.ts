import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const root = join(dirname(fileURLToPath(import.meta.url)), "../../..")

function src(rel: string): string {
  return readFileSync(join(root, "src", rel), "utf8")
}

describe("telematics_device surface for 458.0", () => {
  it("ships the catalog route and forbids amount copy", () => {
    expect(src("features/ops/ops-index.ts")).toContain('"458.0": "/telematics-devices"')
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/telematics-devices"')
    expect(src("routes/telematics-devices.tsx")).toContain("TelematicsDeviceDesk")
    expect(src("lib/telematics-devices-api.ts")).not.toContain("amount")
  })
})
