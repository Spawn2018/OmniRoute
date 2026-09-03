import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { networkCreateBody } from "@/lib/networks-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("networkCreateBody", () => {
  it("splits aliases and blanks optional text", () => {
    expect(
      networkCreateBody({
        code: " WCA ",
        name: " WCA Worldwide ",
        aliasesText: " wca_ww , , ",
        website: "  ",
        regionScope: " PL ",
        isGlobal: true,
      }),
    ).toEqual({
      code: "WCA",
      name: "WCA Worldwide",
      aliases: ["wca_ww"],
      website: null,
      region_scope: "PL",
      is_global: true,
    })
  })
})

describe("networks catalog surface for 9.0", () => {
  it("ships /networks on DataTableShell with create and resolve", () => {
    const page = readFileSync(path.join(srcRoot, "features/networks/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/networks.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/networks")
    expect(nav).toContain("/networks")
    expect(lists).toContain("networks")
    expect(ops).toContain("/networks")
    expect(page).toContain("CatalogLoadedTable")
    expect(page).toContain("createNetwork")
    expect(page).toContain("resolveNetwork")
    expect(page).toContain("source_ref")
    expect(page).not.toContain("amount")
    expect(page).toContain("createNetworkMember")
    expect(page).toContain('data-network-member="catalog"')
    expect(page).toContain("createCarrierInquiry")
    expect(page).toContain('data-carrier-inquiry="catalog"')
    expect(page).not.toContain("cheerio")
    expect(page).not.toContain("httpx")
  })
})
