import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { formatInstant, t } from "@/lib/i18n"

const lib = readFileSync(new URL("./i18n.ts", import.meta.url), "utf8")
const packageJson = readFileSync(new URL("../../package.json", import.meta.url), "utf8")

describe("ui_message catalog for 55.0", () => {
  it("returns pl copy and rejects a missing key", () => {
    expect(t("extraction_quality.title")).toBe("Jakość ekstrakcji")
    expect(t("tenant_rollout.title")).toBe("Wdrożenie tenanta")
    expect(() => t("missing.key")).toThrow(/brak klucza i18n/)
  })

  it("formats an ISO instant in pl-PL without Number on amounts", () => {
    const shown = formatInstant("2026-09-02T12:00:00.000Z")
    expect(shown).toMatch(/9/)
    expect(shown).toMatch(/2026/)
    expect(formatInstant("not-an-instant")).toBe("")
    expect(lib).not.toContain("parseFloat")
    expect(lib).not.toContain("Number(")
    expect(packageJson).not.toContain("i18next")
  })
})
