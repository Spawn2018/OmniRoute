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
  loadTachoOfficeMarks,
  type TachoOfficeMarkRow,
} from "@/lib/tacho-office-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { TachoOfficeMarkComposer } from "./mark-form"

const helper = createColumnHelper<TachoOfficeMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod biura tacho" }),
  helper.accessor("tacho_kind", { header: "Office / card / DDD" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function TachoOfficeMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listing = useQuery({
    enabled: ready,
    queryFn: loadTachoOfficeMarks,
    queryKey: ["tacho-office-marks", orgId],
    retry: false,
  })
  const rows = listing.data ?? []
  const tableOk = ready && listing.error == null

  return (
    <section
      className="space-y-3 border border-zinc-700/25 bg-zinc-50/50 p-5 dark:bg-zinc-950/30"
      data-to="board"
    >
      <CatalogHeading
        title="Tacho Office"
        subtitle="EXP4.10 · office|card|ddd|other · bez live DDD"
      />
      <p className="text-sm text-muted-foreground">
        Katalog znacznika biura tacho. Apka nie poprawia tachografu i nie parsuje DDD.
      </p>
      {!ready ? (
        <TenantSessionNotice />
      ) : (
        <TachoOfficeMarkComposer organizationId={orgId} />
      )}
      {listing.error ? <CatalogError error={listing.error} /> : null}
      {tableOk && rows.length === 0 ? (
        <p className="text-sm text-muted-foreground">Pusty katalog tacho office.</p>
      ) : null}
      {tableOk ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod biura tacho",
            tacho_kind: "Office / card / DDD",
            source_ref: "Zrodlo",
          }}
          columns={COLS}
          data={rows}
          globalFilterPlaceholder="Szukaj tacho office…"
          tableKey={BUSINESS_LISTS.tachoOfficeMark.tableKey}
        />
      ) : null}
    </section>
  )
}
