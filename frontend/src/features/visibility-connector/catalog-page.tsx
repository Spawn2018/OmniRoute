import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { getTenantContext } from "@/lib/tenant"
import { listVisibilityFixtures, type VisibilityFixtureRow } from "@/lib/visibility-connectors-api"
import { VisibilityConnectorSave } from "./visibility-connector-form"

const cols = createColumnHelper<VisibilityFixtureRow>()

const VISIBILITY_COLUMNS = [
  cols.accessor("connector_code", { header: "Kod" }),
  cols.accessor("system_kind", { header: "Vendor" }),
  cols.accessor("source_ref", { header: "Pochodzenie" }),
]

const VISIBILITY_LABELS = {
  connector_code: "Kod",
  system_kind: "Vendor",
  source_ref: "Pochodzenie",
}

function VisibilityFixtureTable(args: { organizationId: string | null }) {
  const listed = useQuery({
    enabled: args.organizationId !== null,
    queryFn: listVisibilityFixtures,
    queryKey: ["visibility-fixtures", args.organizationId],
    retry: false,
  })
  if (listed.error) {
    return <CatalogError error={listed.error} />
  }
  return (
    <DataTableShell
      columnLabels={VISIBILITY_LABELS}
      columns={VISIBILITY_COLUMNS}
      data={listed.data ?? []}
      globalFilterPlaceholder="Filtruj konektor widoczności…"
      tableKey={BUSINESS_LISTS.visibilityConnector.tableKey}
    />
  )
}

export function VisibilityConnectorDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-5" data-visibility-fixture="board">
      <CatalogHeading
        title="Konektor widoczności"
        subtitle="CT7 visibility_connector · tokeny p44/fourkites/shippeo · nie live track · nie AIS"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="flex flex-col gap-8">
          <VisibilityConnectorSave organizationId={ctx.organizationId} />
          <VisibilityFixtureTable organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
