import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { parcelWrite } from "@/lib/shipment-packages-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("parcelWrite", () => {
  it("trims scan fields without parsing money", () => {
    expect(
      parcelWrite({
        orderKey: "  ship  ",
        haltRef: " halt ",
        parcelToken: "box_1",
        stageMark: "at_stop",
        scanMark: "omni://shipment-package/box_1",
        originNote: "tenant:manual",
      }),
    ).toEqual({
      shipment_id: "ship",
      stop_id: "halt",
      package_code: "box_1",
      package_status: "at_stop",
      scan_token: "omni://shipment-package/box_1",
      source_ref: "tenant:manual",
    })
  })
})

describe("shipment_package surface for 156.0", () => {
  it("records a scan on /shipment-packages without WMS", () => {
    const page = src("features/shipment-package/catalog-page.tsx")
    const panel = src("features/shipment-package/scan-panel.tsx")
    expect(src("routes/shipment-packages.tsx")).toContain("/shipment-packages")
    expect(src("components/layout/sidebar.tsx")).toContain("/shipment-packages")
    expect(src("lib/business-lists.ts")).toContain("shipmentPackage")
    expect(page).toContain('data-parcel="desk"')
    expect(page).toContain("ParcelScanPanel")
    expect(panel).toContain("persistParcel")
    expect(panel).toContain('data-parcel="scan-form"')
    expect(panel).toContain("Zapisz skan paczki")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(panel).not.toContain("wms")
    expect(src("features/ops/ops-index.ts")).toContain('"156.0": "/shipment-packages"')
    expect(src("features/ops/ops-index.ts")).toContain('"541.0": "/shipment-packages"')
  })
})
