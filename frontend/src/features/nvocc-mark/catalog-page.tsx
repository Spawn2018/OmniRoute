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
  loadNvoccMarks,
  type NvoccMarkRow,
} from "@/lib/nvocc-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { NvoccMarkComposer } from "./mark-form"

const helper = createColumnHelper<NvoccMarkRow>()
const COLS = [
  helper.accessor("mark_code", { header: "Kod roli NVOCC" }),
  helper.accessor("nvocc_kind", { header: "Rola house/master" }),
  helper.accessor("source_ref", { header: "Źródło HITL" }),
]

export function NvoccMarkBoard() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listing = useQuery({
    enabled: ready,
    queryFn: loadNvoccMarks,
    queryKey: ["nvocc-marks", orgId],
    retry: false,
  })
  const rows = listing.data ?? []
  const tableReady = ready && listing.error == null

  return (
    <section
      className="space-y-4 border-y border-slate-700/25 bg-slate-50/40 py-5 dark:bg-slate-950/30"
      data-nv="board"
    >
      <CatalogHeading
        title="Katalog NVOCC"
        subtitle="EXP4.7 · nvocc|house|master|other · bez booking live"
      />
      <p className="max-w-2xl text-sm text-muted-foreground">
        Rola NVOCC / house / master jako dana. Nie ustawia `party.is_nvocc` i nie woła
        ocean booking API.
      </p>
      {!ready ? <TenantSessionNotice /> : <NvoccMarkComposer organizationId={orgId} />}
      {listing.error ? <CatalogError error={listing.error} /> : null}
      {tableReady && rows.length === 0 ? (
        <p className="text-sm italic text-muted-foreground">
          Pusty katalog NVOCC — pierwszy wpis tylko HITL.
        </p>
      ) : null}
      {tableReady ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod roli NVOCC",
            nvocc_kind: "Rola house/master",
            source_ref: "Źródło HITL",
          }}
          columns={COLS}
          data={rows}
          globalFilterPlaceholder="Szukaj roli NVOCC…"
          tableKey={BUSINESS_LISTS.nvoccMark.tableKey}
        />
      ) : null}
    </section>
  )
}
