import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchTripVarianceMarks,
  type TripVarianceMarkRow,
} from "@/lib/trip-variance-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { TripVarianceMarkSave } from "./mark-form"

const bindCol = createColumnHelper<TripVarianceMarkRow>()

const BIND_COLUMNS = [
  bindCol.accessor("mark_code", { header: "Kod" }),
  bindCol.accessor("variance_kind", { header: "Wariancja" }),
  bindCol.accessor("source_ref", { header: "source_ref" }),
]

export function TripVarianceMarkDesk() {
  const session = getTenantContext()
  const organizationId = session.organizationId
  const sessionReady = Boolean(organizationId && session.userId)
  const catalog = useQuery({
    enabled: sessionReady,
    queryFn: fetchTripVarianceMarks,
    queryKey: ["trip-variance-marks", organizationId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-4" data-trip-variance-mark="desk">
      <CatalogHeading
        title="Wariancje przejazdu"
        subtitle="P5 leftover P5b trip_variance_mark · HITL · nie SQL na charge · nie druga marża"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      {sessionReady ? <TripVarianceMarkSave organizationId={organizationId} /> : null}
      {catalog.error ? <CatalogError error={catalog.error} /> : null}
      {sessionReady && catalog.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            variance_kind: "Wariancja",
            source_ref: "source_ref",
          }}
          columns={BIND_COLUMNS}
          data={catalog.data ?? []}
          globalFilterPlaceholder="Filtr wariancji…"
          tableKey={BUSINESS_LISTS.tripVarianceMark.tableKey}
        />
      ) : null}
    </section>
  )
}
