import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { sanctionsParties } from "@/lib/parties-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("sanctionsParties", () => {
  it("keeps active counterparties and drops inactive", () => {
    expect(
      sanctionsParties([
        { is_active: false },
        { is_active: true },
      ]),
    ).toEqual([{ is_active: true }])
  })
})

describe("sanctions surface for 45.0", () => {
  it("ships /sanctions as active parties without an OFAC table", () => {
    const page = src("features/sanctions/catalog-page.tsx")
    expect(src("routes/sanctions.tsx")).toContain("/sanctions")
    expect(src("components/layout/sidebar.tsx")).toContain("/sanctions")
    expect(src("lib/business-lists.ts")).toContain("sanctions")
    expect(src("features/ops/ops-index.ts")).toContain("/sanctions")
    expect(page).toContain('data-sanctions="board"')
    expect(page).toContain("sanctionsParties")
    expect(page).toContain("fetchParties")
    expect(page).toContain("tax_id")
    expect(page).toContain("country_code")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("ofac")
  })
})
