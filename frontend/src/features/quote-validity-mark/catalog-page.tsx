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
  loadQuoteValidityMarks,
  type QuoteValidityMarkRow,
} from "@/lib/quote-validity-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { QuoteValidityMarkComposer } from "./mark-form"

const helper = createColumnHelper<QuoteValidityMarkRow>()
const COLS = [
  helper.accessor("validity_kind", { header: "Stan" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function QuoteValidityMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadQuoteValidityMarks,
    queryKey: ["quote-validity-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-qvm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Quote validity"
          subtitle="EXP1 · open|revised|superseded|other · bez kolumny quotation"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik ważności oferty — tylko katalog danych.</li>
          <li>Bez daty ważności i bez numeru rewizji na wycenie.</li>
          <li>Odrębny od quote_currency_mark i tender_quote.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow quote validity.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              validity_kind: "Stan",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika quote validity…"
            tableKey={BUSINESS_LISTS.quoteValidityMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <QuoteValidityMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
