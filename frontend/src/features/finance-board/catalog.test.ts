import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("finance-board surface for 15.0", () => {
  it("ships /finance as read-only facts without calculating margin", () => {
    const page = readFileSync(path.join(srcRoot, "features/finance-board/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/finance.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/finance")
    expect(nav).toContain("/finance")
    expect(lists).toContain("financeBoard")
    expect(ops).toContain("/finance")
    expect(page).toContain("CatalogLoadedTable")
    expect(page).toContain("fetchCharges")
    expect(page).toContain("fetchNbpRates")
    expect(page).toContain("fetchParties")
    expect(page).toContain("fetchCreditReviews")
    expect(page).toContain("margin_amount")
    expect(page).toContain("<Money")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("createCharge")
    expect(page).not.toContain("buy_amount -")
    expect(page).not.toContain("score")
    expect(page).not.toContain("openai")
  })
})
