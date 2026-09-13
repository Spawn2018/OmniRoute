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
  loadSuggestionLedgers,
  type SuggestionLedgerRow,
} from "@/lib/suggestion-ledgers-api"
import { getTenantContext } from "@/lib/tenant"
import { SuggestionLedgerComposer } from "./ledger-form"

const helper = createColumnHelper<SuggestionLedgerRow>()
const COLS = [
  helper.accessor("suggestion_kind", { header: "Rodzaj" }),
  helper.accessor("target_bc", { header: "Kontekst" }),
  helper.accessor("interval_low", { header: "Low" }),
  helper.accessor("interval_high", { header: "High" }),
  helper.accessor("reaction", { header: "Reakcja" }),
  helper.accessor("changed_to", { header: "Zmiana" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function SuggestionLedgerBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadSuggestionLedgers,
    queryKey: ["suggestion-ledgers", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-suggestion-ledger="desk">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Ledger podpowiedzi"
          subtitle="AI1.0 · kind ze słownika · accept|modify|reject · bez zapisu LLM"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL zapis podpowiedzi i reakcji człowieka — tylko dane.</li>
          <li>Przedział jako tekst dziesiętny. Bez CRPS liczonego i bez kwoty.</li>
          <li>Odrębny od prediction_ledger i operator_decision.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak wierszy ledgeru podpowiedzi.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              suggestion_kind: "Rodzaj",
              target_bc: "Kontekst",
              interval_low: "Low",
              interval_high: "High",
              reaction: "Reakcja",
              changed_to: "Zmiana",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj podpowiedzi…"
            tableKey={BUSINESS_LISTS.suggestionLedger.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <SuggestionLedgerComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
