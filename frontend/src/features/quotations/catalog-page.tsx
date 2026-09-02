import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { resolveNbpRate, type NbpRate } from "@/lib/nbp-rates-api"
import { fetchParties } from "@/lib/parties-api"
import { fetchPorts } from "@/lib/ports-api"
import {
  createQuotation,
  fetchQuotations,
  quotationCreateBody,
  quotationCurrencies,
  quotationSkipsNbpCatalog,
  type Quotation,
} from "@/lib/quotations-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<Quotation>()

const columns = [
  helper.accessor("charge_code", { header: "Kod opłaty" }),
  helper.accessor("amount", {
    header: "Kwota ze stawki",
    cell: ({ row }) => <Money amount={row.original.amount} currency={row.original.currency} />,
  }),
  helper.accessor("party_id", {
    header: "Kontrahent",
    cell: ({ row }) => <span className="font-mono text-xs">{row.original.party_id ?? "—"}</span>,
  }),
  helper.accessor("origin_port_id", {
    header: "POL",
    cell: ({ row }) => <span className="font-mono text-xs">{row.original.origin_port_id ?? "—"}</span>,
  }),
  helper.accessor("destination_port_id", {
    header: "POD",
    cell: ({ row }) => (
      <span className="font-mono text-xs">{row.original.destination_port_id ?? "—"}</span>
    ),
  }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
  helper.accessor("rate_line_id", { header: "Stawka" }),
]

const COLUMN_LABELS = {
  charge_code: "Kod opłaty",
  amount: "Kwota ze stawki",
  party_id: "Kontrahent",
  origin_port_id: "POL",
  destination_port_id: "POD",
  source_ref: "Pochodzenie",
  rate_line_id: "Stawka",
}

function OfferNbpFieldset(args: { currencies: string[]; signedIn: boolean }) {
  const [offerCurrency, setOfferCurrency] = useState("")
  const [offerOnDate, setOfferOnDate] = useState("")
  const [offerNbp, setOfferNbp] = useState<NbpRate | null>(null)
  const [plnSkip, setPlnSkip] = useState(false)

  const nbpLookup = useMutation({
    mutationFn: () => resolveNbpRate(offerCurrency.trim().toUpperCase(), offerOnDate),
    onSuccess: (row) => {
      setOfferNbp(row)
    },
    onError: () => {
      setOfferNbp(null)
    },
  })

  return (
    <fieldset className="flex flex-col gap-2 rounded-md border border-border bg-card p-3">
      <legend className="px-1 text-sm font-medium">Kurs NBP waluty oferty</legend>
      <p className="text-xs text-muted-foreground">
        ISO z wiersza wyceny · resolve katalogu 6.0 · nie przeliczaj amount
      </p>
      {args.currencies.length === 0 ? (
        <p className="text-sm text-muted-foreground">Najpierw wycena — waluta ze stawki.</p>
      ) : (
        <form
          className="flex flex-col gap-2 md:flex-row md:flex-wrap md:items-end"
          onSubmit={(event) => {
            event.preventDefault()
            if (quotationSkipsNbpCatalog(offerCurrency)) {
              setPlnSkip(true)
              setOfferNbp(null)
              return
            }
            setPlnSkip(false)
            nbpLookup.mutate()
          }}
        >
          <label className="flex flex-col gap-1 text-xs">
            quotation.currency
            <select
              aria-label="Waluta oferty"
              className="h-8 rounded-md border border-border bg-card px-2 text-sm"
              value={offerCurrency}
              onChange={(event) => setOfferCurrency(event.target.value)}
              required
            >
              <option value="">Waluta z listy wycen</option>
              {args.currencies.map((iso) => (
                <option key={iso} value={iso}>
                  {iso}
                </option>
              ))}
            </select>
          </label>
          <Input
            aria-label="Dzień kursu oferty"
            type="date"
            value={offerOnDate}
            onChange={(event) => setOfferOnDate(event.target.value)}
            required
          />
          <Button type="submit" disabled={nbpLookup.isPending || !args.signedIn}>
            Pokaż kurs NBP
          </Button>
        </form>
      )}
      {plnSkip ? (
        <p className="text-sm text-muted-foreground">PLN — katalog 6.0 nie trzyma kursu PLN</p>
      ) : null}
      {nbpLookup.isError && !plnSkip ? (
        <p className="text-sm text-destructive">{(nbpLookup.error as Error).message}</p>
      ) : null}
      {offerNbp ? (
        <p className="font-mono text-xs">
          {offerNbp.currency} {offerNbp.mid} {offerNbp.rate_date} {offerNbp.source_ref}
        </p>
      ) : null}
    </fieldset>
  )
}

export function QuotationCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [chargeCode, setChargeCode] = useState("")
  const [partyId, setPartyId] = useState("")
  const [originPortId, setOriginPortId] = useState("")
  const [destinationPortId, setDestinationPortId] = useState("")
  const [filterPartyId, setFilterPartyId] = useState("")
  const [filterOriginPortId, setFilterOriginPortId] = useState("")
  const [filterDestinationPortId, setFilterDestinationPortId] = useState("")
  const signedIn = Boolean(ctx.organizationId && ctx.userId)

  const partiesQuery = useQuery({
    queryKey: ["parties-picker", ctx.organizationId],
    queryFn: fetchParties,
    enabled: signedIn,
    retry: false,
  })

  const portsQuery = useQuery({
    queryKey: ["ports-picker", ctx.organizationId],
    queryFn: () => fetchPorts(""),
    enabled: signedIn,
    retry: false,
  })

  const query = useQuery({
    queryKey: [
      "quotations",
      ctx.organizationId,
      filterPartyId,
      filterOriginPortId,
      filterDestinationPortId,
    ],
    queryFn: () =>
      fetchQuotations({
        partyId: filterPartyId,
        originPortId: filterOriginPortId,
        destinationPortId: filterDestinationPortId,
      }),
    enabled: signedIn,
    retry: false,
  })

  const quoteMutation = useMutation({
    mutationFn: () =>
      createQuotation(
        quotationCreateBody({
          chargeCode,
          originPortId,
          destinationPortId,
          partyId,
        }),
      ),
    onSuccess: () => {
      setChargeCode("")
      void queryClient.invalidateQueries({ queryKey: ["quotations", ctx.organizationId] })
    },
  })

  const parties = partiesQuery.data ?? []
  const ports = portsQuery.data ?? []

  return (
    <section className="space-y-3">
      <header>
        <h2 className="text-base font-semibold">Wyceny</h2>
        <p className="text-xs text-muted-foreground">
          quotation M-21 · kwota z bieżącego rate_line w SQL · kurs NBP z katalogu 6.0 · nie mnoż kwoty
          w formularzu
        </p>
      </header>

      {signedIn ? null : (
        <p className="text-sm">
          Najpierw ustaw tenant na stronie <Link className="underline" to="/session">Sesja</Link>.
        </p>
      )}

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          quoteMutation.mutate()
        }}
      >
        <Input
          aria-label="Kod opłaty"
          placeholder="THC"
          value={chargeCode}
          onChange={(event) => setChargeCode(event.target.value)}
          required
        />
        <label className="flex flex-col gap-1 text-xs">
          party_id
          <select
            aria-label="Kontrahent"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={partyId}
            onChange={(event) => setPartyId(event.target.value)}
            required
          >
            <option value="">Kontrahent</option>
            {parties.map((party) => (
              <option key={party.id} value={party.id}>
                {party.legal_name}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          origin_port_id
          <select
            aria-label="Port załadunku"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={originPortId}
            onChange={(event) => setOriginPortId(event.target.value)}
            required
          >
            <option value="">POL</option>
            {ports.map((port) => (
              <option key={port.id} value={port.id}>
                {port.unlocode} {port.name}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          destination_port_id
          <select
            aria-label="Port wyładunku"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={destinationPortId}
            onChange={(event) => setDestinationPortId(event.target.value)}
            required
          >
            <option value="">POD</option>
            {ports.map((port) => (
              <option key={port.id} value={port.id}>
                {port.unlocode} {port.name}
              </option>
            ))}
          </select>
        </label>
        <Button type="submit" disabled={quoteMutation.isPending || !signedIn}>
          Wycen z bieżącej stawki
        </Button>
      </form>

      <div className="flex flex-col gap-2 md:flex-row md:flex-wrap">
        <label className="flex flex-col gap-1 text-xs">
          filtr party_id
          <select
            aria-label="Filtr kontrahenta"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={filterPartyId}
            onChange={(event) => setFilterPartyId(event.target.value)}
          >
            <option value="">Wszyscy kontrahenci</option>
            {parties.map((party) => (
              <option key={party.id} value={party.id}>
                {party.legal_name}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          filtr origin_port_id
          <select
            aria-label="Filtr POL"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={filterOriginPortId}
            onChange={(event) => setFilterOriginPortId(event.target.value)}
          >
            <option value="">Wszystkie POL</option>
            {ports.map((port) => (
              <option key={port.id} value={port.id}>
                {port.unlocode} {port.name}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          filtr destination_port_id
          <select
            aria-label="Filtr POD"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={filterDestinationPortId}
            onChange={(event) => setFilterDestinationPortId(event.target.value)}
          >
            <option value="">Wszystkie POD</option>
            {ports.map((port) => (
              <option key={port.id} value={port.id}>
                {port.unlocode} {port.name}
              </option>
            ))}
          </select>
        </label>
      </div>

      {quoteMutation.isError ? (
        <p className="text-sm text-destructive">{(quoteMutation.error as Error).message}</p>
      ) : null}

      {query.data ? (
        <OfferNbpFieldset currencies={quotationCurrencies(query.data)} signedIn={signedIn} />
      ) : null}

      {query.isPending ? <p className="text-sm text-muted-foreground">Pobieranie wycen…</p> : null}
      {query.isError ? <p className="text-sm text-destructive">{(query.error as Error).message}</p> : null}
      {query.data ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.quotations.tableKey}
          columns={columns}
          data={query.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Szukaj wyceny…"
        />
      ) : null}
    </section>
  )
}
