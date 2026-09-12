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
  loadNamedPlaceMarks,
  type NamedPlaceMarkRow,
} from "@/lib/named-place-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { NamedPlaceMarkComposer } from "./mark-form"

const helper = createColumnHelper<NamedPlaceMarkRow>()
const COLS = [
  helper.accessor("terms_version", { header: "Wersja" }),
  helper.accessor("named_place", { header: "Miejsce" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function NamedPlaceMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadNamedPlaceMarks,
    queryKey: ["named-place-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-npm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Miejsce nazwane"
          subtitle="EXP0.6 · named_place + 2020|2010 · bez cytatu ICC"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik miejsca nazwanego — tylko katalog danych.</li>
          <li>Bez cytatu ICC i bez mutacji pól na wycenie.</li>
          <li>Odrębny od quotation.named_place (137.0).</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Brak znacznikow miejsca nazwanego.
          </p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              terms_version: "Wersja",
              named_place: "Miejsce",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika miejsca…"
            tableKey={BUSINESS_LISTS.namedPlaceMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <NamedPlaceMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
