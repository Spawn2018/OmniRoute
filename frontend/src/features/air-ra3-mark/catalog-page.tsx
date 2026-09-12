import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadAirRa3Marks, type AirRa3MarkRow } from "@/lib/air-ra3-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { AirRa3MarkComposer } from "./mark-form"

const helper = createColumnHelper<AirRa3MarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod air" }),
  helper.accessor("air_kind", { header: "RA3 / lithium" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

export function AirRa3MarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const canLoad = Boolean(orgId && ctx.userId)
  const query = useQuery({
    enabled: canLoad,
    queryFn: loadAirRa3Marks,
    queryKey: ["air-ra3-marks", orgId],
    retry: false,
  })
  const marks = query.data ?? []
  const showTable = canLoad && query.error == null

  return (
    <section
      className="space-y-5 rounded-md border border-indigo-900/15 bg-indigo-50/35 p-4 dark:bg-indigo-950/20"
      data-air3="board"
    >
      <CatalogHeading
        title="Air RA3 / lithium"
        subtitle="EXP4.1 · air_kind ra3|lithium|known_consignor|other · bez IATA live"
      />
      <p className="text-xs leading-relaxed text-muted-foreground">
        Znacznik kwalifikacji lotniczej. Nie scrape RA3 i nie klasy UN z LLM.
      </p>
      {!canLoad ? <TenantSessionNotice /> : <AirRa3MarkComposer organizationId={orgId} />}
      {query.error ? <CatalogError error={query.error} /> : null}
      {showTable && marks.length === 0 ? (
        <p className="rounded border border-dashed border-indigo-800/30 p-2 text-sm text-muted-foreground">
          Brak znaczników air — dodaj pierwszy wpis HITL.
        </p>
      ) : null}
      {showTable ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod air",
            air_kind: "RA3 / lithium",
            source_ref: "Źródło",
          }}
          columns={COLS}
          data={marks}
          globalFilterPlaceholder="Filtr air RA3…"
          tableKey={BUSINESS_LISTS.airRa3Mark.tableKey}
        />
      ) : null}
    </section>
  )
}
