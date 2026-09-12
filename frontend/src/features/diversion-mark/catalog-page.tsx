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
  loadDiversionMarks,
  type DiversionMarkRow,
} from "@/lib/diversion-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { DiversionMarkComposer } from "./mark-form"

const helper = createColumnHelper<DiversionMarkRow>()
const COLS = [
  helper.accessor("stance_kind", { header: "Postawa" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function DiversionMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadDiversionMarks,
    queryKey: ["diversion-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-dvm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Diversion"
          subtitle="EXP1 · diversion|reroute|other · bez FK shipment"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik diversion — tylko katalog danych.</li>
          <li>Bez FK shipment i bez cargo_value.</li>
          <li>Odrębny od diversion_of_shipment_id na zleceniu.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow diversion.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              stance_kind: "Postawa",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika diversion…"
            tableKey={BUSINESS_LISTS.diversionMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <DiversionMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
