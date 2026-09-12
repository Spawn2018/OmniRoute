import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadFunnelMarks, type FunnelMarkRow } from "@/lib/funnel-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { FunnelMarkComposer } from "./mark-form"

const helper = createColumnHelper<FunnelMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod lejka" }),
  helper.accessor("funnel_kind", { header: "lead / quote / win" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function FunnelMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listing = useQuery({
    enabled: ready,
    queryFn: loadFunnelMarks,
    queryKey: ["funnel-marks", orgId],
    retry: false,
  })
  const rows = listing.data ?? []
  const tableOk = ready && listing.error == null

  return (
    <div className="space-y-4 border-t-4 border-teal-700/50 px-4 py-6" data-fn="board">
      <CatalogHeading title="X7 lejek" subtitle="EXP4.14 · lead|quote|win|other · bez CRM live" />
      <p className="text-sm text-muted-foreground">
        Etap lejka sprzedażowego jako dana HITL. Bez attribution live i bez liczenia konwersji.
      </p>
      {!ready ? <TenantSessionNotice /> : <FunnelMarkComposer organizationId={orgId} />}
      {listing.error ? <CatalogError error={listing.error} /> : null}
      {tableOk && rows.length === 0 ? (
        <p className="text-sm text-muted-foreground">Brak etapow lejka.</p>
      ) : null}
      {tableOk ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod lejka",
            funnel_kind: "lead / quote / win",
            source_ref: "Zrodlo",
          }}
          columns={COLS}
          data={rows}
          globalFilterPlaceholder="Filtr lejka…"
          tableKey={BUSINESS_LISTS.funnelMark.tableKey}
        />
      ) : null}
    </div>
  )
}
