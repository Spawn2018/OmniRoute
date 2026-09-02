import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"

const justfile = readFileSync(new URL("../../../justfile", import.meta.url), "utf8")
const workflow = readFileSync(new URL("../../../.github/workflows/gate.yml", import.meta.url), "utf8")
const spec = readFileSync(new URL("../../e2e/critical-paths.spec.ts", import.meta.url), "utf8")

describe("e2e axe gate for 56.0", () => {
  it("pins Playwright in code-gate and Chromium in CI", () => {
    expect(justfile).toMatch(/code-gate:.*frontend-e2e/)
    expect(justfile).toContain("playwright test")
    expect(workflow).toContain("playwright install")
    expect(workflow).toContain("chromium")
    expect(spec).not.toContain("parseFloat")
    expect(spec).not.toContain(".click(")
  })
})
