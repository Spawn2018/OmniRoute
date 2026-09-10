import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listExchangeConnectors, type ExchangeConnectorRow } from "@/lib/exchange-connectors-api"
import { getTenantContext } from "@/lib/tenant"
import { ExchangeConnectorSave } from "./exchange-connector-form"

const helper = createColumnHelper<ExchangeConnectorRow>()

const columns = [
  helper.accessor("connector_code", { header: "Kod" }),
  helper.accessor("system_kind", { header: "Tablica" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

const COLUMN_LABELS = {
  connector_code: "Kod",
  system_kind: "Tablica",
  source_ref: "Pochodzenie",
}

function TransEuBoardRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    enabled: args.organizationId !== null,
    queryFn: listExchangeConnectors,
    queryKey: ["exchange-connectors", args.organizationId],
    retry: false,
  })
  const rows = listed.data ?? []
  return (
    <div className="min-w-0 flex-1">
      {listed.error ? <CatalogError error={listed.error} /> : null}
      <DataTableShell
        columnLabels={COLUMN_LABELS}
        columns={columns}
        data={rows}
        globalFilterPlaceholder="Szukaj konektora giełdy…"
        tableKey={BUSINESS_LISTS.exchangeConnector.tableKey}
      />
    </div>
  )
}

export function ExchangeConnectorDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-exchange-connector="fixture-desk">
      <CatalogHeading
        title="Konektor giełdy"
        subtitle="S55 exchange_connector · kind trans_eu jako dane · nie live HTTP · nie portal klienta"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="grid gap-6 lg:grid-cols-2">
          <ExchangeConnectorSave organizationId={ctx.organizationId} />
          <TransEuBoardRows organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
