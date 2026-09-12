import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { loadErruMarks, type ErruMarkRow } from "@/lib/erru-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ErruMarkComposer } from "./mark-form"

const helper = createColumnHelper<ErruMarkRow>()
const COLS = [
  helper.accessor("check_kind", { header: "Sprawdzenie" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function ErruMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadErruMarks,
    queryKey: ["erru-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-erm="split">
      <section className="space-y-3 border-r border-violet-800/20 pr-4">
        <CatalogHeading
          title="Sprawdzenie ERRU"
          subtitle="EXP4.20 · to_verify|clear|hit|other · bez live ERRU"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik sprawdzenia ERRU — tylko katalog danych.</li>
          <li>Bez live ERRU HTTP i Citizen API.</li>
          <li>Bez scrapingu i scoringu osoby.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow ERRU.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              check_kind: "Sprawdzenie",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj ERRU…"
            tableKey={BUSINESS_LISTS.erruMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <ErruMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
