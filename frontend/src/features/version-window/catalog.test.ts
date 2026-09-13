import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("version_window surface for 445.0", () => {
  it("lists daily averages on /version-windows without composer or Money", () => {
    const page = src("features/version-window/catalog-page.tsx")
    expect(src("routes/version-windows.tsx")).toContain("/version-windows")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/version-windows"')
    expect(src("lib/business-lists.ts")).toContain("versionWindow")
    expect(page).toContain('data-version-window="desk"')
    expect(page).not.toContain("Composer")
    expect(page).not.toContain("createVersionWindow")
    expect(page).not.toContain("<Money")
    expect(page).not.toContain("parseFloat")
    expect(src("lib/version-windows-api.ts")).not.toContain("method: \"POST\"")
    expect(src("features/ops/ops-index.ts")).toContain('"445.0": "/version-windows"')
  })
})
