import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { listPlanSnapshots, type PlanSnapshotRow } from "@/lib/plan-snapshots-api"
import { getTenantContext } from "@/lib/tenant"
import { SnapshotSave } from "./snapshot-form"

const helper = createColumnHelper<PlanSnapshotRow>()

const columns = [
  helper.accessor("snapshot_code", { header: "Kod" }),
  helper.accessor("author_label", { header: "Autor" }),
  helper.accessor("recorded_at", { header: "Czas" }),
  helper.accessor("shipment_id", { header: "Zlecenie" }),
  helper.accessor("trip_id", { header: "Przejazd" }),
  helper.accessor("resource_id", { header: "Zasób" }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
]

const COLUMN_LABELS = {
  snapshot_code: "Kod",
  author_label: "Autor",
  recorded_at: "Czas",
  shipment_id: "Zlecenie",
  trip_id: "Przejazd",
  resource_id: "Zasób",
  source_ref: "Pochodzenie",
}

function SnapshotRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["plan-snapshots", args.organizationId],
    queryFn: listPlanSnapshots,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <div className="min-w-0 flex-1">
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <DataTableShell
        tableKey={BUSINESS_LISTS.planSnapshot.tableKey}
        columns={columns}
        data={listed.data ?? []}
        columnLabels={COLUMN_LABELS}
        globalFilterPlaceholder="Szukaj migawki…"
      />
    </div>
  )
}

export function SnapshotDesk() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)

  return (
    <section className="flex flex-col gap-4" data-plan-snapshot="desk">
      <CatalogHeading
        title="Migawka planu"
        subtitle="B0b plan_snapshot · wersja jako dane · nie silnik"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? (
        <div className="grid gap-6 lg:grid-cols-2">
          <SnapshotSave organizationId={ctx.organizationId} />
          <SnapshotRows organizationId={ctx.organizationId} />
        </div>
      ) : null}
    </section>
  )
}
