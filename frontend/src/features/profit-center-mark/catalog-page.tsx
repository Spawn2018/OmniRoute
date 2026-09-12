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
  loadProfitCenterMarks,
  type ProfitCenterMarkRow,
} from "@/lib/profit-center-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ProfitCenterMarkComposer } from "./mark-form"

const helper = createColumnHelper<ProfitCenterMarkRow>()
const COLS = [
  helper.accessor("center_kind", { header: "Rodzaj" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function ProfitCenterMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadProfitCenterMarks,
    queryKey: ["profit-center-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-pcm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Centrum zysku/kosztu"
          subtitle="EXP1 · profit|cost|project|other · bez kolumny shipment"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik centrum zysku, kosztu i projektu — tylko katalog danych.</li>
          <li>Bez kolumny na shipment i bez cost_allocation_mark EXP2.3.</li>
          <li>Odrębny od charge i od ekstrakcji LLM.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow centrum zysku/kosztu.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              center_kind: "Rodzaj",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika centrum zysku/kosztu…"
            tableKey={BUSINESS_LISTS.profitCenterMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <ProfitCenterMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
