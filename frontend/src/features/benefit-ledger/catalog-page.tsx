import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Money } from "@/components/money"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  loadBenefitLedgers,
  type BenefitLedgerRow,
} from "@/lib/benefit-ledgers-api"
import { getTenantContext } from "@/lib/tenant"
import { BenefitLedgerComposer } from "./ledger-form"

const helper = createColumnHelper<BenefitLedgerRow>()
const COLS = [
  helper.accessor("benefit_code", { header: "Kod" }),
  helper.accessor("method_label", { header: "Metoda" }),
  helper.accessor("hours_saved", { header: "Godziny" }),
  helper.display({
    id: "saved_amount",
    header: "Kwota",
    cell: (info) => (
      <Money
        amount={info.row.original.saved_amount}
        currency={info.row.original.saved_currency}
      />
    ),
  }),
  helper.accessor("source_ref", { header: "Ref" }),
]

export function BenefitLedgerBoard() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const sessionReady = Boolean(organizationId && tenant.userId)
  const query = useQuery({
    enabled: sessionReady,
    queryFn: loadBenefitLedgers,
    queryKey: ["benefit-ledgers", organizationId],
    retry: false,
  })
  const catalog = query.data ?? []
  const showTable = sessionReady && query.error == null

  return (
    <div
      className="grid gap-6 lg:grid-cols-[1fr_minmax(0,22rem)]"
      data-benefit-ledger="desk"
    >
      <section className="space-y-3 border-r border-sky-800/20 pr-4">
        <CatalogHeading
          title="Ledger oszczędności"
          subtitle="AI1.3 · method_label + Decimal · bez SQL z charge"
        />
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>HITL zapis oszczędności — operator wpisuje liczby.</li>
          <li>Metoda punktu odniesienia jest obowiązkowa. Bez niej liczba jest nieweryfikowalna.</li>
          <li>Marża zostaje na charge. Serwis nie liczy z charge ani z LLM.</li>
        </ul>
        {query.error ? <CatalogError error={query.error} /> : null}
        {showTable && catalog.length === 0 ? (
          <p className="text-sm text-muted-foreground">Brak wierszy ledgeru oszczędności.</p>
        ) : null}
        {showTable ? (
          <DataTableShell
            columnLabels={{
              benefit_code: "Kod",
              method_label: "Metoda",
              hours_saved: "Godziny",
              saved_amount: "Kwota",
              source_ref: "Ref",
            }}
            columns={COLS}
            data={catalog}
            globalFilterPlaceholder="Szukaj oszczędności…"
            tableKey={BUSINESS_LISTS.benefitLedger.tableKey}
          />
        ) : null}
      </section>
      <aside className="space-y-2">
        {!sessionReady ? (
          <TenantSessionNotice />
        ) : (
          <BenefitLedgerComposer organizationId={organizationId} />
        )}
      </aside>
    </div>
  )
}
