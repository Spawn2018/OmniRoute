import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { commodityCodeCreateBody } from "@/lib/commodity-codes-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("commodityCodeCreateBody", () => {
  it("splits aliases on comma and drops blanks", () => {
    expect(
      commodityCodeCreateBody({
        code: " 0805 ",
        name: " Citrus ",
        aliasesText: " 080510 , , 080520 ",
      }),
    ).toEqual({
      code: "0805",
      name: "Citrus",
      aliases: ["080510", "080520"],
    })
  })

  it("sends empty aliases when the field is blank", () => {
    expect(commodityCodeCreateBody({ code: "0901", name: "Coffee", aliasesText: "" })).toEqual({
      code: "0901",
      name: "Coffee",
      aliases: [],
    })
  })
})

describe("commodity codes catalog surface for 5.2", () => {
  it("ships /commodity-codes on DataTableShell with create and resolve", () => {
    const page = readFileSync(path.join(srcRoot, "features/commodity-codes/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/commodity-codes.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/commodity-codes")
    expect(nav).toContain("/commodity-codes")
    expect(lists).toContain("commodityCodes")
    expect(ops).toContain("/commodity-codes")
    expect(page).toContain("CatalogLoadedTable")
    expect(
      readFileSync(path.join(srcRoot, "components/catalog/catalog-parts.tsx"), "utf8"),
    ).toContain("DataTableShell")
    expect(page).toContain("createCommodityCode")
    expect(page).toContain("resolveCommodityCode")
    expect(page).toContain("source_ref")
    expect(page).not.toContain("amount")
  })
})
