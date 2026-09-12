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
  loadEDoreczeniaMarks,
  type EDoreczeniaMarkRow,
} from "@/lib/e-doreczenia-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { EDoreczeniaMarkComposer } from "./mark-form"

const helper = createColumnHelper<EDoreczeniaMarkRow>()
const COLS = [
  helper.accessor("delivery_kind", { header: "Rodzaj" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function EDoreczeniaMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadEDoreczeniaMarks,
    queryKey: ["e-doreczenia-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-edm="split">
      <section className="space-y-3 border-r border-violet-800/20 pr-4">
        <CatalogHeading
          title="e-Doręczenia"
          subtitle="EXP2.19 · edoreczenia|receipt|other · bez live"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik e-Doręczenia — tylko katalog danych.</li>
          <li>Bez bajtów PDF, kwot i live ADE.</li>
          <li>Bez HTTP do Poczty Polskiej / e-Doręczeń.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow e-Doręczenia.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              delivery_kind: "Rodzaj",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj e-Doręczenia…"
            tableKey={BUSINESS_LISTS.eDoreczeniaMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <EDoreczeniaMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
