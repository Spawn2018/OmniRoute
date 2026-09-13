import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  listFactoringConnectors,
  type FactoringConnectorRow,
} from "@/lib/factoring-connectors-api"
import { getTenantContext } from "@/lib/tenant"
import { FactoringConnectorSave } from "./factoring-connector-form"

const helper = createColumnHelper<FactoringConnectorRow>()

const columns = [
  helper.accessor("connector_code", { header: "Kod" }),
  helper.accessor("system_kind", { header: "Partner" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

const COLUMN_LABELS = {
  connector_code: "Kod",
  system_kind: "Partner",
  source_ref: "Pochodzenie",
}

function FactoringConnectorRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    enabled: args.organizationId !== null,
    queryFn: listFactoringConnectors,
    queryKey: ["factoring-connectors", args.organizationId],
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
        globalFilterPlaceholder="Szukaj konektora faktoringu…"
        tableKey={BUSINESS_LISTS.factoringConnector.tableKey}
      />
    </div>
  )
}

export function FactoringConnectorDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-factoring-connector="desk">
      <CatalogHeading
        title="Faktoring — partner"
        subtitle="BR5.0 factoring_connector · SMEO|other jako dane · nie live HTTP"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="grid gap-6 lg:grid-cols-2">
          <FactoringConnectorSave organizationId={ctx.organizationId} />
          <FactoringConnectorRows organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
