import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listSapConnectors, type SapConnectorRow } from "@/lib/sap-connectors-api"
import { getTenantContext } from "@/lib/tenant"
import { SapConnectorSave } from "./sap-connector-form"

const cols = createColumnHelper<SapConnectorRow>()

const COLUMNS = [
  cols.accessor("connector_code", { header: "Kod" }),
  cols.accessor("system_kind", { header: "System" }),
  cols.accessor("source_ref", { header: "Pochodzenie" }),
]

const LABELS = {
  connector_code: "Kod",
  system_kind: "System",
  source_ref: "Pochodzenie",
}

function SapTable(args: { organizationId: string | null }) {
  const listed = useQuery({
    enabled: args.organizationId !== null,
    queryFn: listSapConnectors,
    queryKey: ["sap-connectors", args.organizationId],
    retry: false,
  })
  if (listed.error) {
    return <CatalogError error={listed.error} />
  }
  return (
    <DataTableShell
      columnLabels={LABELS}
      columns={COLUMNS}
      data={listed.data ?? []}
      globalFilterPlaceholder="Filtruj konektor SAP/Oracle…"
      tableKey={BUSINESS_LISTS.sapConnector.tableKey}
    />
  )
}

export function SapConnectorDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  return (
    <section className="flex flex-col gap-5" data-sap-connector="board">
      <CatalogHeading
        title="Konektor SAP/Oracle"
        subtitle="CT6 sap_connector · katalog HITL · nie live SOAP · nie sekrety"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="flex flex-col gap-8">
          <SapConnectorSave organizationId={ctx.organizationId} />
          <SapTable organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
