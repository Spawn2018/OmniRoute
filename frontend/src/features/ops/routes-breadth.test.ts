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
    expect(SHIPPED_CHARGE_ROUTES).toEqual({
      "1.0": "/charge-codes",
      "1.1": "/rate-lines",
      "1.2": "/charges",
      "2.0": "/quotations",
      "3.0": "/organization-settings",
      "4.0": "/ports",
      "4.1": "/locations",
      "4.2": "/terminals",
      "5.0": "/parties",
      "5.2": "/commodity-codes",
      "6.0": "/nbp-rates",
      "7.0": "/dangerous-goods",
      "8.0": "/parties",
      "9.0": "/networks",
      "10.0": "/party-scorecards",
      "11.0": "/customer-sops",
      "12.0": "/port-surcharges",
      "13.0": "/channel-quotes",
      "14.0": "/credit-reviews",
      "15.0": "/finance",
      "16.0": "/quotations",
      "17.0": "/quotations",
      "18.0": "/quotations",
      "19.0": "/quotations",
      "20.0": "/quotations",
      "21.0": "/quotations",
      "22.0": "/quotations",
      "23.0": "/quotations",
      "24.0": "/quotations",
      "25.0": "/mail",
      "26.0": "/mail",
      "27.0": "/notifications",
      "28.0": "/shipments",
      "29.0": "/tracking",
      "30.0": "/exceptions",
      "31.0": "/shipment-documents",
      "32.0": "/edi",
      "33.0": "/invoices",
      "34.0": "/quote-invoices",
      "35.0": "/payments",
      "36.0": "/money-cost",
      "37.0": "/fx-differences",
      "38.0": "/cashflows",
      "39.0": "/cost-to-serve",
      "40.0": "/bookkeeping",
      "41.0": "/road",
      "42.0": "/rail",
      "43.0": "/china-rail",
      "44.0": "/lcl",
      "45.0": "/sanctions",
      "46.0": "/gdpr",
      "47.0": "/ai",
      "48.0": "/health",
      "49.0": "/quality",
      "50.0": "/rollout",
      "74.0": "/decisions",
      "75.0": "/notifications",
      "76.0": "/ai",
      "77.0": "/decisions",
    })
    expect(OPS_JOBS.map((job) => job.route)).toEqual(
      expect.arrayContaining(Object.values(SHIPPED_CHARGE_ROUTES)),
    )
    expect(OPS_JOBS).toHaveLength(48)
    expect(OPS_JOBS.length).not.toBe(70)

    const html = renderToStaticMarkup(
      createElement(OpsIndex, { healthLabel: "ok", healthState: "ok" }),
    )
    expect(html).toContain(ROUTES_BREADTH_STANDING)
    expect(html).toContain('data-routes-breadth="standing"')
    expect(html).not.toContain("70 modułów done")
    expect(html).not.toContain("powierzchnia 2026")
  })
})
