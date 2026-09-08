import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("shipment surface for 28.0 and 90.0", () => {
  it("keeps /shipments job without legs or HBL", () => {
    const page = readFileSync(path.join(srcRoot, "features/shipment/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/shipments.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/shipments")
    expect(nav).toContain("/shipments")
    expect(lists).toContain("shipment")
    expect(ops).toContain("/shipments")
    expect(page).toContain('data-shipment="board"')
    expect(page).not.toContain("shipment_leg")
    expect(page).not.toContain("hbl")
    expect(page).not.toContain("acceptExtractionDraft")
  })

  it("records 90.0 as a live shipment table on /shipments", () => {
    const page = readFileSync(path.join(srcRoot, "features/shipment/catalog-page.tsx"), "utf8")
    const api = readFileSync(path.join(srcRoot, "lib/shipments-api.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(ops).toContain('"90.0": "/shipments"')
    expect(api).toContain("createShipment")
    expect(page).toContain("fetchShipments")
    expect(page).toContain("Zapisz zlecenie")
    expect(page).toContain("ShipmentStakeholderPanel")
    expect(page).toContain("BookingInstructionPanel")
    expect(page).toContain("StopPointPanel")
    expect(page).toContain("FleetResourcePanel")
    expect(ops).toContain('"151.0": "/shipments"')
    const fleet = readFileSync(path.join(srcRoot, "features/shipment/fleet-resource-panel.tsx"), "utf8")
    expect(fleet).toContain('data-resource="fleet"')
    expect(fleet).toContain("Zapisz zasób")
    expect(fleet).not.toContain("parseFloat")
    expect(page).not.toContain("fetchQuotations")
    expect(page).not.toContain("quotationAcceptancePending")
    const panel = readFileSync(path.join(srcRoot, "features/shipment/shipment-stakeholder-panel.tsx"), "utf8")
    expect(panel).toContain('data-shipment-stakeholder="job"')
    expect(panel).toContain("Zapisz stronę")
    expect(panel).toContain("shipmentStakeholderBody")
    expect(panel).not.toContain("sold_to")
    expect(panel).not.toContain("parseFloat")
    const instruction = readFileSync(
      path.join(srcRoot, "features/shipment/booking-instruction-panel.tsx"),
      "utf8",
    )
    expect(ops).toContain('"148.0": "/shipments"')
    expect(instruction).toContain('data-booking-instruction="job"')
    expect(instruction).toContain("Zapisz instrukcję")
    expect(instruction).toContain("bookingInstructionBody")
    expect(instruction).not.toContain("sold_to")
    expect(instruction).not.toContain("parseFloat")
  })
})
