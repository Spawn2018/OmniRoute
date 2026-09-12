import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadAbSusMarks, type AbSusMarkRow } from "@/lib/ab-sus-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { AbSusMarkComposer } from "./mark-form"

const helper = createColumnHelper<AbSusMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod probe" }),
  helper.accessor("trial_kind", { header: "ab / sus / cohort" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function AbSusMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listing = useQuery({
    enabled: ready,
    queryFn: loadAbSusMarks,
    queryKey: ["ab-sus-marks", orgId],
    retry: false,
  })
  const rows = listing.data ?? []
  const tableOk = ready && listing.error == null

  return (
    <section
      className="space-y-5 bg-slate-100/40 px-4 py-5 dark:bg-slate-950/30"
      data-abs="board"
    >
      <div className="flex flex-wrap items-end justify-between gap-3 border-b border-slate-400/40 pb-3">
        <CatalogHeading
          title="A/B + SUS"
          subtitle="EXP4.13 · ab|sus|cohort|other · bez live survey"
        />
        <p className="max-w-md text-sm text-muted-foreground">
          Znacznik probe A/B lub SUS jako dana HITL. Bez silnika eksperymentu i bez
          liczenia score.
        </p>
      </div>
      {!ready ? <TenantSessionNotice /> : <AbSusMarkComposer organizationId={orgId} />}
      {listing.error ? <CatalogError error={listing.error} /> : null}
      {tableOk && rows.length === 0 ? (
        <p className="text-sm text-muted-foreground">Brak probe A/B+SUS.</p>
      ) : null}
      {tableOk ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod probe",
            trial_kind: "ab / sus / cohort",
            source_ref: "Zrodlo",
          }}
          columns={COLS}
          data={rows}
          globalFilterPlaceholder="Filtr probe…"
          tableKey={BUSINESS_LISTS.abSusMark.tableKey}
        />
      ) : null}
    </section>
  )
}
