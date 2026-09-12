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
  loadHighValueMarks,
  type HighValueMarkRow,
} from "@/lib/high-value-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { HighValueMarkComposer } from "./mark-form"

const helper = createColumnHelper<HighValueMarkRow>()
const COLS = [
  helper.accessor("protocol_kind", { header: "Rodzaj" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function HighValueMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadHighValueMarks,
    queryKey: ["high-value-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-hvm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Protokol high-value"
          subtitle="EXP1 · high_value|protocol|other · bez kolumny shipment"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik protokolu high-value — tylko katalog danych.</li>
          <li>Bez kolumny na shipment i bez cargo_value Decimal.</li>
          <li>Odrębny od charge i od ekstrakcji LLM.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow protokolu high-value.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              protocol_kind: "Rodzaj",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika protokolu high-value…"
            tableKey={BUSINESS_LISTS.highValueMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <HighValueMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
