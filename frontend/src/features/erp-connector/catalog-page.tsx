import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listErpConnectors, type ErpConnectorRow } from "@/lib/erp-connectors-api"
import { getTenantContext } from "@/lib/tenant"
import { ErpConnectorSave } from "./erp-connector-form"

const helper = createColumnHelper<ErpConnectorRow>()

const columns = [
  helper.accessor("connector_code", { header: "Kod" }),
  helper.accessor("system_kind", { header: "System" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

const COLUMN_LABELS = {
  connector_code: "Kod",
  system_kind: "System",
  source_ref: "Pochodzenie",
}

function ErpConnectorRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["erp-connectors", args.organizationId],
    queryFn: listErpConnectors,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <div className="min-w-0 flex-1">
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <DataTableShell
        tableKey={BUSINESS_LISTS.erpConnector.tableKey}
        columns={columns}
        data={listed.data ?? []}
        columnLabels={COLUMN_LABELS}
        globalFilterPlaceholder="Szukaj konektora Optima…"
      />
    </div>
  )
}

export function ErpConnectorDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-erp-connector="desk">
      <CatalogHeading
        title="Konektor Optima"
        subtitle="F9 erp_connector · kind optima jako dane · nie live SOAP"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="grid gap-6 lg:grid-cols-2">
          <ErpConnectorSave organizationId={ctx.organizationId} />
          <ErpConnectorRows organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
