import { createElement } from "react"
import { renderToStaticMarkup } from "react-dom/server"
import { describe, expect, it } from "vitest"
import { OpsIndex } from "@/features/ops/ops-index-page"
import {
  OPS_JOBS,
  ROUTES_BREADTH_STANDING,
  SHIPPED_CHARGE_ROUTES,
} from "@/features/ops/ops-index"

describe("U-routes-breadth standing", () => {
  it("records Charge 1.0–1.2 routes and refuses a 70-module claim", () => {
    // Pełna kopia mapy vs ops-index puchła jscpd — próbki + długość.
    expect(SHIPPED_CHARGE_ROUTES["1.0"]).toBe("/charge-codes")
    expect(SHIPPED_CHARGE_ROUTES["1.1"]).toBe("/rate-lines")
    expect(SHIPPED_CHARGE_ROUTES["1.2"]).toBe("/charges")
    expect(SHIPPED_CHARGE_ROUTES["2.0"]).toBe("/quotations")
    expect(SHIPPED_CHARGE_ROUTES["447.0"]).toBe("/extractions")
    expect(SHIPPED_CHARGE_ROUTES["499.0"]).toBe("/shipper-award-marks")
    expect(SHIPPED_CHARGE_ROUTES["502.0"]).toBe("/extraction-prompt-marks")
    expect(SHIPPED_CHARGE_ROUTES["503.0"]).toBe("/extractions")
    expect(SHIPPED_CHARGE_ROUTES["504.0"]).toBe("/extractions")
    expect(SHIPPED_CHARGE_ROUTES["505.0"]).toBe("/organization-settings")
    expect(SHIPPED_CHARGE_ROUTES["506.0"]).toBe("/extractions")
    expect(SHIPPED_CHARGE_ROUTES["507.0"]).toBe("/extractions")
    expect(SHIPPED_CHARGE_ROUTES["508.0"]).toBe("/extractions")
    expect(SHIPPED_CHARGE_ROUTES["512.0"]).toBe("/extractions")
    expect(SHIPPED_CHARGE_ROUTES["514.0"]).toBe("/extractions")
    expect(SHIPPED_CHARGE_ROUTES["515.0"]).toBe("/extractions")
    expect(SHIPPED_CHARGE_ROUTES["516.0"]).toBe("/allocation-keys")
    expect(SHIPPED_CHARGE_ROUTES["517.0"]).toBe("/cost-category-marks")
    expect(SHIPPED_CHARGE_ROUTES["518.0"]).toBe("/allocation-levels")
    expect(SHIPPED_CHARGE_ROUTES["519.0"]).toBe("/impact-node-marks")
    expect(SHIPPED_CHARGE_ROUTES["520.0"]).toBe("/impact-edge-marks")
    expect(SHIPPED_CHARGE_ROUTES["521.0"]).toBe("/article50-marks")
    expect(SHIPPED_CHARGE_ROUTES["522.0"]).toBe("/data-sources")
    expect(SHIPPED_CHARGE_ROUTES["523.0"]).toBe("/ingest-gate-marks")
    expect(SHIPPED_CHARGE_ROUTES["524.0"]).toBe("/model-feature-marks")
    expect(SHIPPED_CHARGE_ROUTES["525.0"]).toBe("/cfo-narrative-marks")
    expect(SHIPPED_CHARGE_ROUTES["526.0"]).toBe("/kpi-definition-marks")
    expect(SHIPPED_CHARGE_ROUTES["527.0"]).toBe("/margin-floors")
    expect(SHIPPED_CHARGE_ROUTES["528.0"]).toBe("/shipment-clone-marks")
    expect(SHIPPED_CHARGE_ROUTES["529.0"]).toBe("/handover-sbar-marks")
    expect(SHIPPED_CHARGE_ROUTES["530.0"]).toBe("/trip-bill-marks")
    expect(SHIPPED_CHARGE_ROUTES["532.0"]).toBe("/networks")
    expect(SHIPPED_CHARGE_ROUTES["533.0"]).toBe("/networks")
    expect(SHIPPED_CHARGE_ROUTES["534.0"]).toBe("/entity-events")
    expect(SHIPPED_CHARGE_ROUTES["535.0"]).toBe("/networks")
    expect(SHIPPED_CHARGE_ROUTES["536.0"]).toBe("/mail")
    expect(SHIPPED_CHARGE_ROUTES["537.0"]).toBe("/extractions")
    expect(SHIPPED_CHARGE_ROUTES["538.0"]).toBe("/mail")
    expect(SHIPPED_CHARGE_ROUTES["539.0"]).toBe("/charges")
    expect(SHIPPED_CHARGE_ROUTES["540.0"]).toBe("/consignments")
    expect(SHIPPED_CHARGE_ROUTES["541.0"]).toBe("/shipment-packages")
    expect(SHIPPED_CHARGE_ROUTES["542.0"]).toBe("/consignments")
    expect(SHIPPED_CHARGE_ROUTES["543.0"]).toBe("/handover-notes")
    expect(SHIPPED_CHARGE_ROUTES["544.0"]).toBe("/charges")
    expect(SHIPPED_CHARGE_ROUTES["545.0"]).toBe("/product-tickets")
    expect(SHIPPED_CHARGE_ROUTES["546.0"]).toBe("/product-tickets")
    expect(Object.keys(SHIPPED_CHARGE_ROUTES)).toHaveLength(487)

    expect(OPS_JOBS.map((job) => job.route)).toEqual(
      expect.arrayContaining(Object.values(SHIPPED_CHARGE_ROUTES)),
    )
    expect(OPS_JOBS).toHaveLength(319)

    expect(OPS_JOBS.length).not.toBe(157)

    const html = renderToStaticMarkup(
      createElement(OpsIndex, { healthLabel: "ok", healthState: "ok" }),
    )
    expect(html).toContain(ROUTES_BREADTH_STANDING)
    expect(html).toContain('data-routes-breadth="standing"')
    expect(html).not.toContain("70 modułów done")
    expect(html).not.toContain("powierzchnia 2026")
  })
})
