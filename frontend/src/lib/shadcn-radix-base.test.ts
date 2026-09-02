import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"

const componentsJson = readFileSync(new URL("../../components.json", import.meta.url), "utf8")
const packageJson = readFileSync(new URL("../../package.json", import.meta.url), "utf8")

describe("shadcn radix pin for 54.0", () => {
  it("pins CLI base to radix and keeps Radix out of Base UI", () => {
    const pin = JSON.parse(componentsJson) as { base?: string }
    expect(pin.base).toBe("radix")
    expect(componentsJson).not.toContain("base-ui")
    expect(packageJson).not.toContain("@base-ui")
  })
})
