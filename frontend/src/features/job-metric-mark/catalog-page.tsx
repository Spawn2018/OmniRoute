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
  loadJobMetricMarks,
  type JobMetricMarkRow,
} from "@/lib/job-metric-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { JobMetricMarkComposer } from "./mark-form"

const helper = createColumnHelper<JobMetricMarkRow>()
const COLS = [
  helper.accessor("metric_kind", { header: "Metryka" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function JobMetricMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadJobMetricMarks,
    queryKey: ["job-metric-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-jmm="split">
      <section className="space-y-3 border-r border-violet-800/20 pr-4">
        <CatalogHeading
          title="Metryka jobu"
          subtitle="EXP4.21 · time_to_fix|touches|rework|other · bez scoringu"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik metryki jobu — tylko katalog danych.</li>
          <li>Bez scoringu osoby i silnika SQL job.</li>
          <li>Bez kwoty i marży.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow metryki jobu.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              metric_kind: "Metryka",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj metryki jobu…"
            tableKey={BUSINESS_LISTS.jobMetricMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <JobMetricMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
