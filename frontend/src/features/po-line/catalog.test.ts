import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { poLineBody } from "@/lib/po-lines-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("poLineBody", () => {
  it("trims HITL fields and turns blank labels into null", () => {
    expect(
      poLineBody({
        purchaseOrderId: " 11111111-1111-1111-1111-111111111111 ",
        lineSlug: " line_01 ",
        skuText: " SKU-4401 ",
        qtyText: " 12.5 ",
        uomText: " pcs ",
        plantText: " Gdańsk ",
        batchText: "  ",
        serialText: "",
        cooText: " PL ",
        originPointer: "tenant:manual",
      }),
    ).toEqual({
      purchase_order_id: "11111111-1111-1111-1111-111111111111",
      line_code: "line_01",
      sku_code: "SKU-4401",
      qty: "12.5",
      uom_code: "pcs",
      plant_label: "Gdańsk",
      batch_label: null,
      serial_label: null,
      coo_label: "PL",
      source_ref: "tenant:manual",
    })
  })
})

describe("po_line surface for 277.0", () => {
  it("records HITL line on /po-lines without ASN or money", () => {
    const page = src("features/po-line/catalog-page.tsx")
    const panel = src("features/po-line/po-line-form.tsx")
    const client = src("lib/po-lines-api.ts")
    expect(src("routes/po-lines.tsx")).toContain("/po-lines")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/po-lines"')
    expect(src("lib/business-lists.ts")).toContain("poLine")
    expect(page).toContain('data-po-line="board"')
    expect(page).toContain("PoLineDesk")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("CatalogHeading")
    expect(panel).toContain("persistPoLine")
    expect(panel).toContain("Zapisz linię zamówienia")
    expect(panel).not.toContain("<Money")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("Utwórz zlecenie")
    expect(client).not.toContain("asn")
    expect(client).not.toContain("shipment_id")
    expect(client).not.toContain("amount")
    expect(src("features/ops/ops-index.ts")).toContain('"277.0": "/po-lines"')
  })
})
