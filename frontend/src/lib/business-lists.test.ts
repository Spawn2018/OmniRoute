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

function renderDensityShell(): string {
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
  })

  it("covers every existing business list, not only users", () => {
    expect(businessListRoutes().sort()).toEqual([...REQUIRED_BUSINESS_LIST_ROUTES].sort())
    expect(BUSINESS_LISTS.users.tableKey).toBe("tenancy.users")
    expect(BUSINESS_LISTS.chargeCodes.tableKey).toBe("charge_codes")
    expect(BUSINESS_LISTS.rateLines.tableKey).toBe("rate_lines")
    expect(BUSINESS_LISTS.charges.tableKey).toBe("charges")
    expect(BUSINESS_LISTS.extractions.tableKey).toBe("extraction.queue")
  })
})
