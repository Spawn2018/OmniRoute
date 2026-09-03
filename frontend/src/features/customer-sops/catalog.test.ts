import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { customerSopCreateBody } from "@/lib/customer-sops-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("customerSopCreateBody", () => {
  it("trims identifiers and body without sending source_ref", () => {
    expect(
      customerSopCreateBody({
        partyId: "  party-1  ",
        code: " Pre-Alert ",
        title: " Pre alert ",
        body: "  treść  ",
        blocksAuto: true,
      }),
    ).toEqual({
      party_id: "party-1",
      code: "Pre-Alert",
      title: "Pre alert",
      body: "treść",
      blocks_auto: true,
    })
  })
})

describe("customer-sops catalog surface for 11.0", () => {
  it("ships SOP table with draft create, approve, and no money engine", () => {
    const page = readFileSync(
      path.join(srcRoot, "features/customer-sops/catalog-page.tsx"),
      "utf8",
    )
    const route = readFileSync(path.join(srcRoot, "routes/customer-sops.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    const parties = readFileSync(path.join(srcRoot, "features/parties/catalog-page.tsx"), "utf8")
    expect(route).toContain("/customer-sops")
    expect(nav).toContain("/customer-sops")
    expect(lists).toContain("customerSops")
    expect(ops).toContain("/customer-sops")
    expect(parties).toContain("createCustomerSop")
    expect(page).toContain("CatalogLoadedTable")
    expect(page).toContain("approveCustomerSop")
    expect(page).toContain("source_ref")
    expect(page).toContain("Blokuj auto")
    expect(page).toContain("blocks_auto")
    expect(page).not.toContain("amount")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("charge.margin")
    expect(page).not.toContain("generateTask")
  })
})
