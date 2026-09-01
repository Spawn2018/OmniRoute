import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  channelQuoteCreateBody,
  createChannelQuote,
  fetchChannelQuotes,
  resolveChannelQuote,
  type ChannelQuote,
} from "@/lib/channel-quotes-api"
import { getTenantContext } from "@/lib/tenant"
import { Money } from "@/components/money"

const columnHelper = createColumnHelper<ChannelQuote>()

const columns = [
  columnHelper.accessor("party_id", {
    id: "party_id",
    header: "Armator",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("origin_port_id", {
    id: "origin_port_id",
    header: "POL",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("destination_port_id", {
    id: "destination_port_id",
    header: "POD",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("quote_date", {
    id: "quote_date",
    header: "Dzień oferty",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.display({
    id: "amount",
    header: "Oferta",
    cell: (info) => {
      const row = info.row.original
      return <Money amount={row.amount} currency={row.currency} />
    },
  }),
  columnHelper.accessor("source_ref", {
    id: "source_ref",
    header: "Pochodzenie",
    cell: (info) => info.getValue(),
  }),
]

const COLUMN_LABELS = {
  party_id: "Armator",
  origin_port_id: "POL",
  destination_port_id: "POD",
  quote_date: "Dzień oferty",
  amount: "Oferta",
  source_ref: "source_ref",
}

export function ChannelQuoteCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [partyId, setPartyId] = useState("")
  const [originPortId, setOriginPortId] = useState("")
  const [destinationPortId, setDestinationPortId] = useState("")
  const [quoteDate, setQuoteDate] = useState("")
  const [amount, setAmount] = useState("")
  const [currency, setCurrency] = useState("")
  const [lookupPartyId, setLookupPartyId] = useState("")
  const [lookupOrigin, setLookupOrigin] = useState("")
  const [lookupDestination, setLookupDestination] = useState("")
  const [lookupDate, setLookupDate] = useState("")
  const [resolved, setResolved] = useState<ChannelQuote | null>(null)
  const canWrite = Boolean(ctx.organizationId && ctx.userId)

  const query = useQuery({
    queryKey: ["channel-quotes", ctx.organizationId],
    queryFn: fetchChannelQuotes,
    enabled: canWrite,
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () =>
      createChannelQuote(
        channelQuoteCreateBody({
          partyId,
          originPortId,
          destinationPortId,
          quoteDate,
          amount,
          currency,
        }),
      ),
    onSuccess: () => {
      setPartyId("")
      setOriginPortId("")
      setDestinationPortId("")
      setQuoteDate("")
      setAmount("")
      setCurrency("")
      void queryClient.invalidateQueries({ queryKey: ["channel-quotes", ctx.organizationId] })
    },
  })

  const resolveMutation = useMutation({
    mutationFn: () =>
      resolveChannelQuote({
        partyId: lookupPartyId.trim(),
        originPortId: lookupOrigin.trim(),
        destinationPortId: lookupDestination.trim(),
        onDate: lookupDate,
      }),
    onSuccess: (row) => setResolved(row),
    onError: () => setResolved(null),
  })

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Oferty z kanału armatora"
        subtitle="channel_quote M-19 · katalog oferty · nie live HTTP · nie stawka kupna"
      />
      {canWrite ? null : <TenantSessionNotice />}
      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-2"
        onSubmit={(event) => {
          event.preventDefault()
          if (canWrite) createMutation.mutate()
        }}
      >
        <Input
          aria-label="Identyfikator armatora oferty"
          placeholder="party_id"
          value={partyId}
          onChange={(event) => setPartyId(event.target.value)}
          required
        />
        <Input
          aria-label="Port załadunku oferty"
          placeholder="origin_port_id"
          value={originPortId}
          onChange={(event) => setOriginPortId(event.target.value)}
          required
        />
        <Input
          aria-label="Port wyładunku oferty"
          placeholder="destination_port_id"
          value={destinationPortId}
          onChange={(event) => setDestinationPortId(event.target.value)}
          required
        />
        <Input
          aria-label="Data oferty"
          type="date"
          value={quoteDate}
          onChange={(event) => setQuoteDate(event.target.value)}
          required
        />
        <Input
          aria-label="Kwota oferty"
          placeholder="1200.0000"
          inputMode="decimal"
          value={amount}
          onChange={(event) => setAmount(event.target.value)}
          required
        />
        <Input
          aria-label="Waluta oferty"
          placeholder="USD"
          maxLength={3}
          value={currency}
          onChange={(event) => setCurrency(event.target.value)}
          required
        />
        <Button type="submit" disabled={createMutation.isPending || !canWrite}>
          Dodaj ofertę
        </Button>
      </form>
      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}
      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-2"
        onSubmit={(event) => {
          event.preventDefault()
          resolveMutation.mutate()
        }}
      >
        <Input
          aria-label="Sprawdź armatora oferty"
          placeholder="party_id"
          value={lookupPartyId}
          onChange={(event) => setLookupPartyId(event.target.value)}
        />
        <Input
          aria-label="Sprawdź POL oferty"
          placeholder="origin_port_id"
          value={lookupOrigin}
          onChange={(event) => setLookupOrigin(event.target.value)}
        />
        <Input
          aria-label="Sprawdź POD oferty"
          placeholder="destination_port_id"
          value={lookupDestination}
          onChange={(event) => setLookupDestination(event.target.value)}
        />
        <Input
          aria-label="Sprawdź datę oferty"
          type="date"
          value={lookupDate}
          onChange={(event) => setLookupDate(event.target.value)}
        />
        <Button
          type="submit"
          variant="outline"
          disabled={
            resolveMutation.isPending
            || lookupPartyId.length === 0
            || lookupOrigin.length === 0
            || lookupDestination.length === 0
            || lookupDate.length === 0
          }
        >
          Rozwiąż
        </Button>
        {resolved ? (
          <p className="font-mono text-xs md:col-span-2">
            {resolved.quote_date} · {resolved.amount} {resolved.currency}
          </p>
        ) : null}
      </form>
      {resolveMutation.isError ? <CatalogError error={resolveMutation.error} /> : null}
      <CatalogLoadedTable
        tableKey={BUSINESS_LISTS.channelQuotes.tableKey}
        globalFilterPlaceholder="Szukaj oferty z kanału…"
        columnLabels={COLUMN_LABELS}
        columns={columns}
        data={query.data}
        error={query.error}
        loading={query.isLoading}
      />
    </div>
  )
}
