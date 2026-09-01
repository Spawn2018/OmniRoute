import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { portSurchargeCreateBody } from "@/lib/port-surcharges-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("portSurchargeCreateBody", () => {
  it("trims fields and uppercases currency without sending source_ref", () => {
    expect(
      portSurchargeCreateBody({
        portId: "  port-1  ",
        code: " THC ",
        title: " Terminal handling ",
        appliesWhen: "  weekend  ",
        amount: " 85.0000 ",
        currency: " eur ",
      }),
    ).toEqual({
      port_id: "port-1",
      code: "THC",
      title: "Terminal handling",
      applies_when: "weekend",
      amount: "85.0000",
      currency: "EUR",
    })
  })
})

describe("port-surcharges catalog surface for 12.0", () => {
  it("ships extra table with amount, resolve, ports panel, and no charge engine", () => {
    const page = readFileSync(
      path.join(srcRoot, "features/port-surcharges/catalog-page.tsx"),
      "utf8",
    )
    const route = readFileSync(path.join(srcRoot, "routes/port-surcharges.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    const ports = readFileSync(path.join(srcRoot, "features/geography/ports-page.tsx"), "utf8")
    expect(route).toContain("/port-surcharges")
    expect(nav).toContain("/port-surcharges")
    expect(lists).toContain("portSurcharges")
    expect(ops).toContain("/port-surcharges")
    expect(ports).toContain("createPortSurcharge")
    expect(page).toContain("CatalogLoadedTable")
    expect(page).toContain("createPortSurcharge")
    expect(page).toContain("resolvePortSurcharge")
    expect(page).toContain("source_ref")
    expect(page).toContain("amount")
    expect(page).toContain("<Money")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("charge.margin")
    expect(page).not.toContain("buy_amount")
  })
})
