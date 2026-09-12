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
  loadMultiManningMarks,
  type MultiManningMarkRow,
} from "@/lib/multi-manning-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { MultiManningMarkComposer } from "./mark-form"

const helper = createColumnHelper<MultiManningMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod zalogi" }),
  helper.accessor("manning_kind", { header: "Tryb dual/relay/team" }),
  helper.accessor("source_ref", { header: "Zrodlo HITL" }),
]

export function MultiManningMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const sessionOk = Boolean(orgId && ctx.userId)
  const crewQuery = useQuery({
    enabled: sessionOk,
    queryFn: loadMultiManningMarks,
    queryKey: ["multi-manning-marks", orgId],
    retry: false,
  })
  const crewRows = crewQuery.data ?? []
  const showCrew = sessionOk && crewQuery.error == null

  return (
    <section
      className="grid gap-4 border-l-4 border-amber-700/50 bg-amber-50/20 py-4 pl-4 dark:bg-amber-950/15"
      data-mm="board"
    >
      <CatalogHeading
        title="Multi-manning"
        subtitle="EXP4.8 · dual|relay|team|other · bez tacho DDD"
      />
      <p className="max-w-xl text-sm leading-snug text-muted-foreground">
        Tryb zalogi jako katalog HITL. Nie pisze trip.driver2 i nie czyta tachografu.
      </p>
      {!sessionOk ? (
        <TenantSessionNotice />
      ) : (
        <MultiManningMarkComposer organizationId={orgId} />
      )}
      {crewQuery.error ? <CatalogError error={crewQuery.error} /> : null}
      {showCrew && crewRows.length === 0 ? (
        <p className="text-xs uppercase tracking-wide text-muted-foreground">
          Katalog multi-manning pusty
        </p>
      ) : null}
      {showCrew ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod zalogi",
            manning_kind: "Tryb dual/relay/team",
            source_ref: "Zrodlo HITL",
          }}
          columns={COLS}
          data={crewRows}
          globalFilterPlaceholder="Szukaj trybu zalogi…"
          tableKey={BUSINESS_LISTS.multiManningMark.tableKey}
        />
      ) : null}
    </section>
  )
}
