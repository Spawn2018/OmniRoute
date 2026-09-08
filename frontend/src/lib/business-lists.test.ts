import { createElement } from "react"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { renderToStaticMarkup } from "react-dom/server"
import { describe, expect, it } from "vitest"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { DEFAULT_TABLE_VIEW_CONFIG } from "@/components/data-table/types"
import {
  BUSINESS_LISTS,
  REQUIRED_BUSINESS_LIST_ROUTES,
  businessListRoutes,
} from "@/lib/business-lists"

function renderDensityShell(allowCondensed = false): string {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  })
  return renderToStaticMarkup(
    createElement(
      QueryClientProvider,
      { client },
      createElement(DataTableShell, {
        tableKey: BUSINESS_LISTS.users.tableKey,
        columns: [{ id: "email", header: "Email" }],
        data: [],
        columnLabels: { email: "Email" },
        allowCondensed,
      }),
    ),
  )
}

describe("business list density", () => {
  it("defaults to compact on the shared table shell", () => {
    expect(DEFAULT_TABLE_VIEW_CONFIG.density).toBe("compact")
    const html = renderDensityShell()
    expect(html).toContain('data-table-density="compact"')
    expect(html).toContain('aria-label="Gęstość tabeli"')
    expect(html).toContain('value="compact"')
    expect(html).toContain('value="comfortable"')
    expect(html).not.toContain('value="condensed"')
  })

  it("offers condensed only when the shell opts in", () => {
    expect(renderDensityShell(true)).toContain('value="condensed"')
  })

  it("covers every existing business list, not only users", () => {
    expect(businessListRoutes().sort()).toEqual([...REQUIRED_BUSINESS_LIST_ROUTES].sort())
    expect(BUSINESS_LISTS.users.tableKey).toBe("tenancy.users")
    expect(BUSINESS_LISTS.chargeCodes.tableKey).toBe("charge_codes")
    expect(BUSINESS_LISTS.commodityCodes.tableKey).toBe("commodity_codes")
    expect(BUSINESS_LISTS.dangerousGoods.tableKey).toBe("dangerous_goods")
    expect(BUSINESS_LISTS.networks.tableKey).toBe("networks")
    expect(BUSINESS_LISTS.nbpRates.tableKey).toBe("nbp_rates")
    expect(BUSINESS_LISTS.rateLines.tableKey).toBe("rate_lines")
    expect(BUSINESS_LISTS.charges.tableKey).toBe("charges")
    expect(BUSINESS_LISTS.channelQuotes.tableKey).toBe("channel_quotes")
    expect(BUSINESS_LISTS.quotations.tableKey).toBe("quotations")
    expect(BUSINESS_LISTS.organizationSettings.tableKey).toBe("organization_settings")
    expect(BUSINESS_LISTS.extractions.tableKey).toBe("extraction.queue")
    expect(BUSINESS_LISTS.ports.tableKey).toBe("ports")
    expect(BUSINESS_LISTS.portSurcharges.tableKey).toBe("port_surcharges")
    expect(BUSINESS_LISTS.partyScorecards.tableKey).toBe("party_scorecards")
    expect(BUSINESS_LISTS.customerSops.tableKey).toBe("customer_sops")
    expect(BUSINESS_LISTS.creditReviews.tableKey).toBe("credit_reviews")
    expect(BUSINESS_LISTS.financeBoard.tableKey).toBe("finance_board")
    expect(BUSINESS_LISTS.salesInvoice.tableKey).toBe("sales_invoice")
    expect(BUSINESS_LISTS.quoteInvoiceSettlement.tableKey).toBe("quote_invoice_settlement")
    expect(BUSINESS_LISTS.bankPayment.tableKey).toBe("bank_payment")
    expect(BUSINESS_LISTS.moneyCost.tableKey).toBe("money_cost")
    expect(BUSINESS_LISTS.fxDifference.tableKey).toBe("fx_difference")
    expect(BUSINESS_LISTS.cashFlow.tableKey).toBe("cash_flow")
    expect(BUSINESS_LISTS.costToServe.tableKey).toBe("cost_to_serve")
    expect(BUSINESS_LISTS.bookkeeping.tableKey).toBe("bookkeeping")
    expect(BUSINESS_LISTS.roadTransport.tableKey).toBe("road_transport")
    expect(BUSINESS_LISTS.intermodalRail.tableKey).toBe("intermodal_rail")
    expect(BUSINESS_LISTS.chinaRail.tableKey).toBe("china_rail")
    expect(BUSINESS_LISTS.oceanLcl.tableKey).toBe("ocean_lcl")
    expect(BUSINESS_LISTS.airFreight.tableKey).toBe("air_freight")
    expect(BUSINESS_LISTS.groupageLines.tableKey).toBe("groupage_line")
    expect(BUSINESS_LISTS.shipmentPackage.tableKey).toBe("shipment_package")
    expect(BUSINESS_LISTS.sanctions.tableKey).toBe("sanctions")
    expect(BUSINESS_LISTS.fraudFlag.tableKey).toBe("fraud_flag")
    expect(BUSINESS_LISTS.gdpr.tableKey).toBe("gdpr")
    expect(BUSINESS_LISTS.aiCopilot.tableKey).toBe("ai_copilot")
    expect(BUSINESS_LISTS.observability.tableKey).toBe("observability")
    expect(BUSINESS_LISTS.extractionQuality.tableKey).toBe("extraction_quality")
    expect(BUSINESS_LISTS.tenantRollout.tableKey).toBe("tenant_rollout")
    expect(BUSINESS_LISTS.mailIntegration.tableKey).toBe("mail_integration")
    expect(BUSINESS_LISTS.operatorNotice.tableKey).toBe("operator_notice")
    expect(BUSINESS_LISTS.shipment.tableKey).toBe("shipment")
    expect(BUSINESS_LISTS.tracking.tableKey).toBe("tracking")
    expect(BUSINESS_LISTS.operationalException.tableKey).toBe("operational_exception")
    expect(BUSINESS_LISTS.cargoClaim.tableKey).toBe("cargo_claim")
    expect(BUSINESS_LISTS.watchtower.tableKey).toBe("watchtower")
    expect(BUSINESS_LISTS.shipmentDocument.tableKey).toBe("shipment_document")
    expect(BUSINESS_LISTS.ediMessage.tableKey).toBe("edi_message")
  })
})
