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
  loadUnSegregationMarks,
  type UnSegregationMarkRow,
} from "@/lib/un-segregation-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { UnSegregationMarkComposer } from "./mark-form"

const helper = createColumnHelper<UnSegregationMarkRow>()
const COLS = [
  helper.accessor("segregate_kind", { header: "Rodzaj" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function UnSegregationMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadUnSegregationMarks,
    queryKey: ["un-segregation-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-usm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Segregacja UN"
          subtitle="EXP0.9 · tunnel|segregation|compat|other · bez solver OR"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik tunel/segregacja UN — tylko katalog danych.</li>
          <li>Bez solvera OR i bez LLM-VRP.</li>
          <li>Odrębny od load_plan_mark i oog_mark.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow segregacji UN.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              segregate_kind: "Rodzaj",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika segregacji…"
            tableKey={BUSINESS_LISTS.unSegregationMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <UnSegregationMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
