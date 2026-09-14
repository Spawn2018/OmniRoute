import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildProductTicketMarkWrite } from "@/lib/product-ticket-marks-api"

describe("product_ticket_mark catalog", () => {
  it("maps plaster 480.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["480.0"]).toBe("/product-ticket-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildProductTicketMarkWrite({
        code: " pt_report_01 ",
        kind: " Report ",
        origin: " fixture://product-ticket/1 ",
      }),
    ).toEqual({
      mark_code: "pt_report_01",
      ticket_kind: "report",
      source_ref: "fixture://product-ticket/1",
    })
  })
})
