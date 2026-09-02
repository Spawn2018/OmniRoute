import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { gdprSubjects } from "@/lib/api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("gdprSubjects", () => {
  it("keeps users with email and drops blank", () => {
    expect(
      gdprSubjects([
        { email: "" },
        { email: "a@b.c" },
      ]),
    ).toEqual([{ email: "a@b.c" }])
  })
})

describe("gdpr surface for 46.0", () => {
  it("ships /gdpr as tenant emails without an erasure table", () => {
    const page = src("features/gdpr/catalog-page.tsx")
    expect(src("routes/gdpr.tsx")).toContain("/gdpr")
    expect(src("components/layout/sidebar.tsx")).toContain("/gdpr")
    expect(src("lib/business-lists.ts")).toContain("gdpr")
    expect(src("features/ops/ops-index.ts")).toContain("/gdpr")
    expect(page).toContain('data-gdpr="board"')
    expect(page).toContain("gdprSubjects")
    expect(page).toContain("fetchTenancyUsers")
    expect(page).toContain("email")
    expect(page).toContain("display_name")
    expect(page).not.toContain("password_hash")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
  })
})
