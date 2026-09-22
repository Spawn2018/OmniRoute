import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { ladingWrite } from "@/lib/ocean-bills-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("ladingWrite", () => {
  it("trims HBL marker fields without parsing money", () => {
    expect(
      ladingWrite({
        consignmentToken: "  ship  ",
        houseToken: "HLCUSHA1234567",
        kindToken: "mbl",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      shipment_id: "ship",
      bill_no: "HLCUSHA1234567",
      bill_kind: "mbl",
      source_ref: "tenant:manual",
    })
  })

  it("omits empty bill_no so the pool can issue later", () => {
    expect(
      ladingWrite({
        consignmentToken: "ship",
        houseToken: "  ",
        kindToken: "hbl",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      shipment_id: "ship",
      bill_kind: "hbl",
      source_ref: "tenant:manual",
    })
  })
})

describe("ocean_bill surface for 160.0 and 621.0", () => {
  it("records an HBL marker on /ocean-bills without PDF", () => {
    const page = src("features/ocean-bill/catalog-page.tsx")
    const panel = src("features/ocean-bill/kind-panel.tsx")
    const api = src("lib/ocean-bills-api.ts")
    expect(src("routes/ocean-bills.tsx")).toContain("/ocean-bills")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/ocean-bills"')
    expect(src("lib/business-lists.ts")).toContain("oceanBill")
    expect(page).toContain('data-ocean-bill="board"')
    expect(page).toContain("HouseKindPanel")
    expect(panel).toContain("persistHouseMark")
    expect(panel).toContain('data-ocean-bill="kind-form"')
    expect(panel).toContain("Zapisz konosament")
    expect(panel).toContain("Nadaj HBL")
    expect(panel).toContain("Nadaj MBL")
    expect(panel).toContain("issueHblNumber")
    expect(api).toContain("hbl-number")
    expect(api).toContain("mbl-number")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(panel).not.toContain("buy_amount")
    expect(src("features/ops/ops-index.ts")).toContain('"160.0": "/ocean-bills"')
    expect(src("features/ops/ops-index.ts")).toContain('"621.0": "/ocean-bills"')
  })
})
