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
  loadQuoteCurrencyMarks,
  type QuoteCurrencyMarkRow,
} from "@/lib/quote-currency-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { QuoteCurrencyMarkComposer } from "./mark-form"

const helper = createColumnHelper<QuoteCurrencyMarkRow>()
const COLS = [
  helper.accessor("currency_kind", { header: "Waluta" }),
  helper.accessor("mark_code", { header: "Kod" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function QuoteCurrencyMarkBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadQuoteCurrencyMarks,
    queryKey: ["quote-currency-marks", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-qcm="split">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Quote currency"
          subtitle="EXP1 · account|pay|other · bez kolumny quotation"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL znacznik quote currency — tylko katalog danych.</li>
          <li>Bez kolumny na wycenie i bez NBP.</li>
          <li>Odrębny od spot_contract_mark.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak znacznikow quote currency.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              currency_kind: "Waluta",
              mark_code: "Kod",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj znacznika quote currency…"
            tableKey={BUSINESS_LISTS.bidDecisionMark.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <QuoteCurrencyMarkComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
