import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { asnBody } from "@/lib/asns-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("asnBody", () => {
  it("trims HITL fields and turns blank labels into null", () => {
    expect(
      asnBody({
        purchaseOrderId: " 11111111-1111-1111-1111-111111111111 ",
        asnSlug: " asn_01 ",
        plantText: " Gdańsk ",
        carrierText: "  ",
        shipRefText: "",
        guideSlug: " lane_pl_de ",
        originPointer: "tenant:manual",
      }),
    ).toEqual({
      purchase_order_id: "11111111-1111-1111-1111-111111111111",
      asn_code: "asn_01",
      plant_label: "Gdańsk",
      carrier_label: null,
      ship_ref_label: null,
      guide_code: "lane_pl_de",
      source_ref: "tenant:manual",
    })
  })
})

describe("asn surface for 278.0 / 286.0", () => {
  it("records HITL awizo on /asns without shipment or money", () => {
    const page = src("features/asn/catalog-page.tsx")
    const panel = src("features/asn/asn-form.tsx")
    const client = src("lib/asns-api.ts")
    expect(src("routes/asns.tsx")).toContain("/asns")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/asns"')
    expect(src("lib/business-lists.ts")).toContain("asn:")
    expect(page).toContain('data-asn="board"')
    expect(page).toContain("AsnDesk")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("CatalogHeading")
    expect(page).toContain("guide_code")
    expect(panel).toContain("persistAsn")
    expect(panel).toContain("guideSlug")
    expect(panel).toContain("Zapisz awizo wysyłki")
    expect(panel).not.toContain("<Money")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("Utwórz zlecenie")
    expect(panel).not.toContain("Wyślij EDI")
    expect(client).not.toContain("shipment_id")
    expect(client).not.toContain("amount")
    expect(client).toContain("guide_code")
    expect(src("features/ops/ops-index.ts")).toContain('"286.0": "/asns"')
  })
})
