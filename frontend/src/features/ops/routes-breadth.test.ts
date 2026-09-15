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
    expect(Object.keys(SHIPPED_CHARGE_ROUTES)).toHaveLength(459)

    expect(OPS_JOBS.map((job) => job.route)).toEqual(
      expect.arrayContaining(Object.values(SHIPPED_CHARGE_ROUTES)),
    )
    expect(OPS_JOBS).toHaveLength(304)

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
