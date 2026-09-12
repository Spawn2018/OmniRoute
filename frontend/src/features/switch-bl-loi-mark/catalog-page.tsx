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
  loadSwitchBlLoiMarks,
  type SwitchBlLoiMarkRow,
} from "@/lib/switch-bl-loi-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { SwitchBlLoiComposer } from "./mark-form"

const cols = createColumnHelper<SwitchBlLoiMarkRow>()
const SBL_COLUMNS = [
  cols.accessor("mark_code", { header: "Kod instrumentu" }),
  cols.accessor("instrument_kind", { header: "BL / LOI / switch" }),
  cols.accessor("source_ref", { header: "Ref HITL" }),
]

export function SwitchBlLoiBoard() {
  const session = getTenantContext()
  const orgId = session.organizationId
  const ready = Boolean(orgId && session.userId)
  const query = useQuery({
    enabled: ready,
    queryFn: loadSwitchBlLoiMarks,
    queryKey: ["switch-bl-loi-marks", orgId],
    retry: false,
  })

  const rows = query.data ?? []
  const emptyHint =
    ready && query.error == null && rows.length === 0
      ? "Brak instrumentow — dodaj BL, LOI albo switch HITL."
      : null

  return (
    <article className="grid gap-4 md:grid-cols-[minmax(0,1fr)]" data-sbl="ledger">
      <header className="space-y-1 border-b border-slate-300/40 pb-3">
        <CatalogHeading
          title="Switch BL i LOI"
          subtitle="EXP3.9 · instrument HITL bl|loi|switch|other · bez live"
        />
        <p className="text-[11px] text-muted-foreground">
          Katalog znacznikow dokumentu — nie ocean_bill i nie kwota.
        </p>
      </header>
      {ready ? <SwitchBlLoiComposer organizationId={orgId} /> : <TenantSessionNotice />}
      {query.error ? <CatalogError error={query.error} /> : null}
      {emptyHint ? <p className="text-sm text-muted-foreground">{emptyHint}</p> : null}
      {ready && query.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod instrumentu",
            instrument_kind: "BL / LOI / switch",
            source_ref: "Ref HITL",
          }}
          columns={SBL_COLUMNS}
          data={rows}
          globalFilterPlaceholder="Filtruj instrumenty BL/LOI…"
          tableKey={BUSINESS_LISTS.switchBlLoiMark.tableKey}
        />
      ) : null}
    </article>
  )
}
