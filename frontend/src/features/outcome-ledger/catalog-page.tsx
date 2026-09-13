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
  loadOutcomeLedgers,
  type OutcomeLedgerRow,
} from "@/lib/outcome-ledgers-api"
import { getTenantContext } from "@/lib/tenant"
import { OutcomeLedgerComposer } from "./ledger-form"

const helper = createColumnHelper<OutcomeLedgerRow>()
const COLS = [
  helper.accessor("outcome_kind", { header: "Rodzaj" }),
  helper.accessor("target_bc", { header: "Kontekst" }),
  helper.accessor("actual_value", { header: "Fakt" }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function OutcomeLedgerBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadOutcomeLedgers,
    queryKey: ["outcome-ledgers", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]" data-outcome-ledger="desk">
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Ledger wyniku"
          subtitle="AI1.1 · eta|rate|route|other · actual_value Decimal · bez CRPS"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL zapis tego, co się naprawdę stało — tylko dane.</li>
          <li>Fakt jako tekst dziesiętny. Bez CRPS liczonego i bez kwoty.</li>
          <li>UUID podpowiedzi jest daną, nie powiązaniem. Złączenie = AI2.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak wierszy ledgeru wyniku.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              outcome_kind: "Rodzaj",
              target_bc: "Kontekst",
              actual_value: "Fakt",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj wyniku…"
            tableKey={BUSINESS_LISTS.outcomeLedger.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <OutcomeLedgerComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
