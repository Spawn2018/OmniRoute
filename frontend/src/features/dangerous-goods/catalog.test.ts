import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { dangerousGoodCreateBody } from "@/lib/dangerous-goods-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("dangerousGoodCreateBody", () => {
  it("splits UN aliases on comma and drops blanks", () => {
    expect(
      dangerousGoodCreateBody({
        unNumber: " UN1203 ",
        imdgClass: " 3 ",
        name: " Petrol ",
        aliasesText: " 1213 , , 1263 ",
      }),
    ).toEqual({
      un_number: "UN1203",
      imdg_class: "3",
      name: "Petrol",
      aliases: ["1213", "1263"],
    })
  })

  it("sends empty aliases when the field is blank", () => {
    expect(
      dangerousGoodCreateBody({
        unNumber: "1203",
        imdgClass: "3",
        name: "Petrol",
        aliasesText: "",
      }),
    ).toEqual({
      un_number: "1203",
      imdg_class: "3",
      name: "Petrol",
      aliases: [],
    })
  })
})

describe("dangerous goods catalog surface for 7.0", () => {
  it("ships /dangerous-goods on DataTableShell with create and resolve", () => {
    const page = readFileSync(path.join(srcRoot, "features/dangerous-goods/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/dangerous-goods.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/dangerous-goods")
    expect(nav).toContain("/dangerous-goods")
    expect(lists).toContain("dangerousGoods")
    expect(ops).toContain("/dangerous-goods")
    expect(page).toContain("CatalogLoadedTable")
    expect(page).toContain("createDangerousGood")
    expect(page).toContain("resolveDangerousGood")
    expect(page).toContain("ResolveTokenForm")
    expect(page).toContain("source_ref")
    expect(page).toContain("un_number")
    expect(page).toContain("imdg_class")
    expect(page).not.toContain("amount")
    expect(page).not.toContain("CatalogCreateForm")
  })
})
