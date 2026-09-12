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
  loadLineImpactMarks,
  type LineImpactMarkRow,
} from "@/lib/line-impact-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { LineImpactMarkComposer } from "./mark-form"

const helper = createColumnHelper<LineImpactMarkRow>()
const COLS = [
  helper.accessor("impact_kind", { header: "Rodzaj" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function LineImpactMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadLineImpactMarks,
    queryKey: ["line-impact-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-lim="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Skutek linii"
          subtitle="EXP3.3b · line|plant|sku|other · bez SQL"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik skutku linii — tylko katalog danych.</li>
          <li>Bez SQL impact, EBITDA i kwot.</li>
          <li>Bez plant live feed — znacznik gdy dane, nie silnik.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow skutku linii.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              impact_kind: "Rodzaj",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj skutku linii…"
            tableKey={BUSINESS_LISTS.lineImpactMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <LineImpactMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
