import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { nbpRateCreateBody } from "@/lib/nbp-rates-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("nbpRateCreateBody", () => {
  it("uppercases ISO currency and trims mid", () => {
    expect(
      nbpRateCreateBody({
        currency: " eur ",
        rateDate: "2026-09-01",
        mid: " 4.2500 ",
      }),
    ).toEqual({
      currency: "EUR",
      rate_date: "2026-09-01",
      mid: "4.2500",
    })
  })
})

describe("nbp rates catalog surface for 6.0", () => {
  it("ships /nbp-rates on DataTableShell with create and resolve by currency and date", () => {
    const page = readFileSync(path.join(srcRoot, "features/nbp-rates/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/nbp-rates.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/nbp-rates")
    expect(nav).toContain("/nbp-rates")
    expect(lists).toContain("nbpRates")
    expect(ops).toContain("/nbp-rates")
    expect(page).toContain("CatalogLoadedTable")
    expect(page).toContain("createNbpRate")
    expect(page).toContain("resolveNbpRate")
    expect(page).toContain("source_ref")
    expect(page).toContain("Sprawdź walutę")
    expect(page).toContain("Sprawdź datę kursu")
    expect(page).not.toContain("amount")
    expect(page).not.toContain("CatalogCreateForm")
  })
})
