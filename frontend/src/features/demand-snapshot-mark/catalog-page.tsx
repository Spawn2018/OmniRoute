import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadDemandSnapshotMarks,
  type DemandSnapshotMarkRow,
} from "@/lib/demand-snapshot-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { DemandSnapshotMarkComposer } from "./mark-form"

const helper = createColumnHelper<DemandSnapshotMarkRow>()
const DSM_COLS = [
  helper.accessor("mark_code", { header: "Kod snapshotu" }),
  helper.accessor("snapshot_kind", { header: "Forecast / booking" }),
  helper.accessor("source_ref", { header: "Zrodlo HITL" }),
]

export function DemandSnapshotMarkBoard() {
  const session = getTenantContext()
  const organizationId = session.organizationId
  const ready = Boolean(organizationId && session.userId)
  const catalog = useQuery({
    enabled: ready,
    queryFn: loadDemandSnapshotMarks,
    queryKey: ["demand-snapshot-marks", organizationId],
    retry: false,
  })
  const rows = catalog.data ?? []

  return (
    <section className="space-y-4 rounded-lg bg-sky-50/50 p-3 dark:bg-sky-950/15" data-dsm="desk">
      <CatalogHeading
        title="Znaczniki demand snapshot"
        subtitle="EXP3.13 · HITL forecast|booking|actual|other · bez demand SQL"
      />
      <p className="max-w-xl text-xs text-muted-foreground">
        Katalog rodzaju snapshotu popytu — nie silnik forecast i nie WMS.
      </p>
      {ready ? (
        <DemandSnapshotMarkComposer organizationId={organizationId} />
      ) : (
        <TenantSessionNotice />
      )}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {ready && !catalog.error && rows.length === 0 ? (
        <p className="text-sm text-muted-foreground">
          Pusta lista — zapisz pierwszy znacznik demand snapshot.
        </p>
      ) : null}
      {ready && !catalog.error ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod snapshotu",
            snapshot_kind: "Forecast / booking",
            source_ref: "Zrodlo HITL",
          }}
          columns={DSM_COLS}
          data={rows}
          globalFilterPlaceholder="Filtruj kody snapshotu…"
          tableKey={BUSINESS_LISTS.demandSnapshotMark.tableKey}
        />
      ) : null}
    </section>
  )
}
