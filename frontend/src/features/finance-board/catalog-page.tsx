import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { createColumnHelper } from "@tanstack/react-table"
import {
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchCharges, type Charge } from "@/lib/charges-api"
import { fetchCreditReviews, type CreditReview } from "@/lib/credit-reviews-api"
import { fetchNbpRates, type NbpRate } from "@/lib/nbp-rates-api"
import { fetchParties, type Party } from "@/lib/parties-api"
import { fetchSalesInvoices, type SalesInvoice } from "@/lib/sales-invoices-api"
import { getTenantContext } from "@/lib/tenant"

const chargeCols = createColumnHelper<Charge>()

const CHARGE_COLUMNS = [
  chargeCols.accessor("charge_code", { id: "charge_code", header: "Kod" }),
  chargeCols.accessor("margin_amount", {
    id: "margin_amount",
    header: "Marża",
    cell: ({ row }) => (
      <Money amount={row.original.margin_amount} currency={row.original.margin_currency} />
    ),
  }),
]

const CHARGE_LABELS = { charge_code: "Kod opłaty", margin_amount: "Marża z charge.margin" }

function RateFacts(args: { rows: NbpRate[] | undefined }) {
  return (
    <section className="rounded-md border border-border p-3">
      <h2 className="mb-2 text-sm font-medium">Kursy NBP</h2>
      <ul className="space-y-1 font-mono text-xs">
        {(args.rows ?? []).map((row) => (
          <li key={row.id}>
            {row.currency} · {row.rate_date} · {row.mid}
          </li>
        ))}
      </ul>
    </section>
  )
}

function LimitFacts(args: { rows: Party[] | undefined }) {
  return (
    <section className="rounded-md border border-border p-3">
      <h2 className="mb-2 text-sm font-medium">Limity kontrahentów (odczyt)</h2>
      <ul className="space-y-1 text-sm">
        {(args.rows ?? []).map((row) => (
          <li key={row.id} className="flex flex-wrap gap-2 text-xs">
            <span>{row.legal_name}</span>
            {row.credit_limit !== null && row.credit_currency !== null ? (
              <Money amount={row.credit_limit} currency={row.credit_currency} />
            ) : (
              <span className="text-muted-foreground">brak limitu</span>
            )}
          </li>
        ))}
      </ul>
    </section>
  )
}

function ReviewFacts(args: { rows: CreditReview[] | undefined }) {
  return (
    <section className="rounded-md border border-border bg-muted/30 p-3">
      <h2 className="mb-2 text-sm font-medium">Recenzje kredytowe</h2>
      {(args.rows ?? []).map((row) => (
        <p key={row.id} className="font-mono text-xs">
          {row.review_date} · {row.decision}
        </p>
      ))}
    </section>
  )
}

function InvoiceFacts(args: { rows: SalesInvoice[] | undefined }) {
  return (
    <section className="rounded-md border border-border p-3">
      <h2 className="mb-2 text-sm font-medium">Faktury</h2>
      <p className="mb-3 text-xs">
        <Link className="underline" to="/invoices">
          Zapis faktury zostaje na /invoices
        </Link>
      </p>
      <dl className="grid gap-3 text-sm" data-finance-invoices="facts">
        {(args.rows ?? []).map((row) => (
          <div key={row.id} className="grid grid-cols-[minmax(0,auto)_1fr] gap-x-4">
            <dt className="font-mono text-xs">{row.invoice_ref}</dt>
            <dd className="text-xs text-muted-foreground">
              {row.invoice_kind}
              {row.ksef_ref !== null ? ` · ${row.ksef_ref}` : " · bez numeru sesji"}
            </dd>
          </div>
        ))}
      </dl>
    </section>
  )
}

function NarrativeSection(args: {
  charges: Charge[] | undefined
  invoices: SalesInvoice[] | undefined
  rates: NbpRate[] | undefined
}) {
  return (
    <section className="rounded-md border border-border p-3" data-finance="narrative">
      <h2 className="mb-2 text-sm font-medium">Narracja po SQL</h2>
      <p className="mb-2 text-xs">
        Marża zostaje na wierszu charge. Model nie liczy i nie sumuje faktur.
      </p>
      {(args.charges ?? []).map((row) => (
        <p key={row.id} className="text-xs">
          Opłata {row.charge_code}:{" "}
          <Money amount={row.margin_amount} currency={row.margin_currency} />
        </p>
      ))}
      {(args.invoices ?? []).map((row) => (
        <p key={`inv-${row.id}`} className="text-xs">
          Faktura {row.invoice_ref} bez kwoty na tablicy.
        </p>
      ))}
      {(args.rates ?? []).map((row) => (
        <p key={`fx-${row.id}`} className="text-xs">
          Kurs {row.currency} z dnia {row.rate_date} (nbp_rate).
        </p>
      ))}
    </section>
  )
}

function useFinanceBoardQueries() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const charges = useQuery({
    queryKey: ["finance-board-charges", ctx.organizationId],
    queryFn: fetchCharges,
    enabled: ready,
    retry: false,
  })
  const rates = useQuery({
    queryKey: ["finance-board-nbp", ctx.organizationId],
    queryFn: fetchNbpRates,
    enabled: ready,
    retry: false,
  })
  const parties = useQuery({
    queryKey: ["finance-board-parties", ctx.organizationId],
    queryFn: fetchParties,
    enabled: ready,
    retry: false,
  })
  const reviews = useQuery({
    queryKey: ["finance-board-reviews", ctx.organizationId],
    queryFn: fetchCreditReviews,
    enabled: ready,
    retry: false,
  })
  const invoices = useQuery({
    queryKey: ["finance-board-invoices", ctx.organizationId],
    queryFn: fetchSalesInvoices,
    enabled: ready,
    retry: false,
  })
  return { ready, charges, rates, parties, reviews, invoices }
}

export function FinanceBoardPage() {
  const board = useFinanceBoardQueries()
  return (
    <div className="flex flex-col gap-4">
      <CatalogHeading
        title="Tablica finansowa"
        subtitle="finance_board M-15 · odczyt faktów z katalogów · narracja po SQL · LLM nie liczy"
      />
      {!board.ready ? <TenantSessionNotice /> : null}
      {board.rates.isError ? <CatalogError error={board.rates.error} /> : null}
      {board.parties.isError ? <CatalogError error={board.parties.error} /> : null}
      {board.reviews.isError ? <CatalogError error={board.reviews.error} /> : null}
      {board.invoices.isError ? <CatalogError error={board.invoices.error} /> : null}
      <CatalogLoadedTable
        tableKey={BUSINESS_LISTS.financeBoard.tableKey}
        globalFilterPlaceholder="Szukaj kodu opłaty…"
        columnLabels={CHARGE_LABELS}
        columns={CHARGE_COLUMNS}
        data={board.charges.data}
        error={board.charges.error}
        loading={board.charges.isLoading}
      />
      <RateFacts rows={board.rates.data} />
      <LimitFacts rows={board.parties.data} />
      <ReviewFacts rows={board.reviews.data} />
      <InvoiceFacts rows={board.invoices.data} />
      <NarrativeSection
        charges={board.charges.data}
        invoices={board.invoices.data}
        rates={board.rates.data}
      />
    </div>
  )
}
