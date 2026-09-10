import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { purchaseOrderBody } from "@/lib/purchase-orders-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("purchaseOrderBody", () => {
  it("trims HITL slug and turns blank plant into null", () => {
    expect(
      purchaseOrderBody({
        poSlug: " po_gdansk_01 ",
        plantText: " Gdańsk ",
        originPointer: "tenant:manual",
      }),
    ).toEqual({
      po_code: "po_gdansk_01",
      plant_label: "Gdańsk",
      source_ref: "tenant:manual",
    })
    expect(
      purchaseOrderBody({
        poSlug: "po_no_plant",
        plantText: "  ",
        originPointer: "fixture://purchase-order/a",
      }).plant_label,
    ).toBeNull()
  })
})

describe("purchase_order surface for 276.0", () => {
  it("records HITL header on /purchase-orders without line or ASN fields", () => {
    const page = src("features/purchase-order/catalog-page.tsx")
    const panel = src("features/purchase-order/purchase-order-form.tsx")
    const client = src("lib/purchase-orders-api.ts")
    expect(src("routes/purchase-orders.tsx")).toContain("/purchase-orders")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/purchase-orders"')
    expect(src("lib/business-lists.ts")).toContain("purchaseOrder")
    expect(page).toContain('data-purchase-order="board"')
    expect(page).toContain("PurchaseOrderDesk")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("CatalogHeading")
    expect(panel).toContain("persistPurchaseOrder")
    expect(panel).toContain("Zapisz zamówienie zakupu")
    expect(panel).not.toContain("<Money")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("Utwórz zlecenie")
    expect(panel).not.toContain("sku")
    expect(client).not.toContain("asn")
    expect(client).not.toContain("shipment_id")
    expect(src("features/ops/ops-index.ts")).toContain('"276.0": "/purchase-orders"')
  })
})
