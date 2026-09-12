import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadLezMarks, type LezMarkRow } from "@/lib/lez-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { LezMarkComposer } from "./mark-form"

const helper = createColumnHelper<LezMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod LEZ" }),
  helper.accessor("lez_kind", { header: "LEZ / ban / zone" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function LezMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listing = useQuery({
    enabled: ready,
    queryFn: loadLezMarks,
    queryKey: ["lez-marks", orgId],
    retry: false,
  })
  const rows = listing.data ?? []
  const tableOk = ready && listing.error == null

  return (
    <section
      className="space-y-4 border-b-2 border-emerald-800/30 bg-emerald-50/30 p-4 dark:bg-emerald-950/20"
      data-lz="board"
    >
      <CatalogHeading
        title="LEZ / zakazy"
        subtitle="EXP4.11 · lez|ban|zone|other · bez mapa live"
      />
      <p className="text-sm text-muted-foreground">
        Znacznik strefy niskoemisyjnej / zakazu jako dana HITL. Bez geofence GPS i bez
        scrapingu mapy.
      </p>
      {!ready ? <TenantSessionNotice /> : <LezMarkComposer organizationId={orgId} />}
      {listing.error ? <CatalogError error={listing.error} /> : null}
      {tableOk && rows.length === 0 ? (
        <p className="text-sm text-muted-foreground">Brak znacznikow LEZ.</p>
      ) : null}
      {tableOk ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod LEZ",
            lez_kind: "LEZ / ban / zone",
            source_ref: "Zrodlo",
          }}
          columns={COLS}
          data={rows}
          globalFilterPlaceholder="Filtr LEZ…"
          tableKey={BUSINESS_LISTS.lezMark.tableKey}
        />
      ) : null}
    </section>
  )
}
