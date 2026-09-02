import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("observability surface for 48.0", () => {
  it("ships /health as fetchHealth without OpenTelemetry", () => {
    const page = src("features/observability/catalog-page.tsx")
    expect(src("routes/health.tsx")).toContain("/health")
    expect(src("components/layout/sidebar.tsx")).toContain("/health")
    expect(src("lib/business-lists.ts")).toContain("observability")
    expect(src("features/ops/ops-index.ts")).toContain("/health")
    expect(page).toContain('data-observability="board"')
    expect(page).toContain("fetchHealth")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("opentelemetry")
  })
})
