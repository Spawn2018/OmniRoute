import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  createRateLine,
  fetchRateLines,
  rateLineCreateBody,
  rateLineSupersedeBody,
  supersedeRateLine,
  type RateLine,
} from "@/lib/rate-lines-api"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { getTenantContext } from "@/lib/tenant"

const columnHelper = createColumnHelper<RateLine>()

const columns = [
  columnHelper.accessor("charge_code", {
    id: "charge_code",
    header: "Kod opłaty",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("amount", {
    id: "amount",
    header: "Kwota kupna",
    cell: (info) => <Money amount={info.getValue()} currency={info.row.original.currency} />,
  }),
  columnHelper.accessor("source_ref", {
    id: "source_ref",
    header: "Pochodzenie",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("allotment_teu", {
    id: "allotment_teu",
    header: "Alokacja TEU",
    cell: (info) => info.getValue() ?? "—",
  }),
  columnHelper.accessor("spot_or_contract", {
    id: "spot_or_contract",
    header: "Spot / kontrakt",
    cell: (info) => info.getValue() ?? "—",
  }),
  columnHelper.accessor("index_id", {
    id: "index_id",
    header: "Indeks FSC",
    cell: (info) => info.getValue() ?? "—",
  }),
  columnHelper.accessor("fuel_index_id", {
    id: "fuel_index_id",
    header: "FK indeksu",
    cell: (info) => info.getValue() ?? "—",
  }),
  columnHelper.accessor("superseded_by", {
    id: "superseded_by",
    header: "Zastąpiona przez",
    cell: (info) => info.getValue() ?? "—",
  }),
]

const COLUMN_LABELS = {
  charge_code: "Kod opłaty",
  amount: "Kwota kupna",
  source_ref: "Pochodzenie",
  allotment_teu: "Alokacja TEU",
  spot_or_contract: "Spot / kontrakt",
  index_id: "Indeks FSC",
  fuel_index_id: "FK indeksu",
  superseded_by: "Zastąpiona przez",
}

export function RateLineCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [chargeCode, setChargeCode] = useState("")
  const [amount, setAmount] = useState("")
  const [currency, setCurrency] = useState("EUR")
  const [sourceRef, setSourceRef] = useState("")
  const [allotmentTeu, setAllotmentTeu] = useState("")
  const [spotOrContract, setSpotOrContract] = useState("")
  const [indexId, setIndexId] = useState("")
  const [fuelIndexId, setFuelIndexId] = useState("")
  const [predecessorId, setPredecessorId] = useState("")
  const [nextAmount, setNextAmount] = useState("")
  const [nextCurrency, setNextCurrency] = useState("EUR")
  const [nextSourceRef, setNextSourceRef] = useState("")
  const [nextAllotmentTeu, setNextAllotmentTeu] = useState("")
  const [nextSpotOrContract, setNextSpotOrContract] = useState("")
  const [nextIndexId, setNextIndexId] = useState("")
  const [nextFuelIndexId, setNextFuelIndexId] = useState("")

  const query = useQuery({
    queryKey: ["rate-lines", ctx.organizationId],
    queryFn: fetchRateLines,
    enabled: Boolean(ctx.organizationId && ctx.userId),
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () =>
      createRateLine(
        rateLineCreateBody({
          chargeCode,
          amount,
          currency,
          sourceRef,
          allotmentTeu,
          spotOrContract,
          indexId,
          fuelIndexId,
        }),
      ),
    onSuccess: () => {
      setChargeCode("")
      setAmount("")
      setSourceRef("")
      setAllotmentTeu("")
      setSpotOrContract("")
      setIndexId("")
      setFuelIndexId("")
      void queryClient.invalidateQueries({ queryKey: ["rate-lines", ctx.organizationId] })
    },
  })

  const supersedeMutation = useMutation({
    mutationFn: () =>
      supersedeRateLine(
        predecessorId.trim(),
        rateLineSupersedeBody({
          amount: nextAmount,
          currency: nextCurrency,
          sourceRef: nextSourceRef,
          allotmentTeu: nextAllotmentTeu,
          spotOrContract: nextSpotOrContract,
          indexId: nextIndexId,
          fuelIndexId: nextFuelIndexId,
        }),
      ),
    onSuccess: () => {
      setPredecessorId("")
      setNextAmount("")
      setNextSourceRef("")
      setNextAllotmentTeu("")
      setNextSpotOrContract("")
      setNextIndexId("")
      setNextFuelIndexId("")
      void queryClient.invalidateQueries({ queryKey: ["rate-lines", ctx.organizationId] })
    },
  })

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Stawki kupna"
        subtitle="rate_line M-07 · niemutowalna · source_ref · opcjonalny allotment_teu · opcjonalny spot_or_contract · opcjonalny index_id · opcjonalny fuel_index_id · nie charge"
      />

      {ctx.organizationId && ctx.userId ? null : <TenantSessionNotice />}

      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-9"
        onSubmit={(event) => {
          event.preventDefault()
          createMutation.mutate()
        }}
      >
        <Input
          aria-label="Kod opłaty"
          placeholder="THC"
          value={chargeCode}
          onChange={(event) => setChargeCode(event.target.value)}
          required
        />
        <Input
          aria-label="Kwota kupna"
          placeholder="10.5000"
          value={amount}
          onChange={(event) => setAmount(event.target.value)}
          required
        />
        <Input
          aria-label="Waluta ISO"
          placeholder="EUR"
          value={currency}
          onChange={(event) => setCurrency(event.target.value)}
          required
        />
        <Input
          aria-label="Pochodzenie stawki"
          placeholder="tariff://msc-2026"
          value={sourceRef}
          onChange={(event) => setSourceRef(event.target.value)}
          required
        />
        <Input
          aria-label="Alokacja TEU"
          placeholder="12.5"
          value={allotmentTeu}
          onChange={(event) => setAllotmentTeu(event.target.value)}
        />
        <Input
          aria-label="Spot lub kontrakt"
          placeholder="spot|contract|other"
          value={spotOrContract}
          onChange={(event) => setSpotOrContract(event.target.value)}
        />
        <Input
          aria-label="Pin indeksu FSC"
          placeholder="FSC-Q3-2026"
          value={indexId}
          onChange={(event) => setIndexId(event.target.value)}
        />
        <Input
          aria-label="Identyfikator indeksu paliwowego"
          placeholder="uuid fuel_index"
          value={fuelIndexId}
          onChange={(event) => setFuelIndexId(event.target.value)}
        />
        <Button type="submit" disabled={createMutation.isPending || !ctx.organizationId}>
          Dodaj stawkę
        </Button>
      </form>

      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}

      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-9"
        onSubmit={(event) => {
          event.preventDefault()
          supersedeMutation.mutate()
        }}
      >
        <Input
          aria-label="Identyfikator stawki do zastąpienia"
          placeholder="id stawki"
          value={predecessorId}
          onChange={(event) => setPredecessorId(event.target.value)}
          required
        />
        <Input
          aria-label="Nowa kwota kupna"
          placeholder="11.0000"
          value={nextAmount}
          onChange={(event) => setNextAmount(event.target.value)}
          required
        />
        <Input
          aria-label="Nowa waluta ISO"
          placeholder="EUR"
          value={nextCurrency}
          onChange={(event) => setNextCurrency(event.target.value)}
          required
        />
        <Input
          aria-label="Nowe pochodzenie stawki"
          placeholder="tariff://msc-2026-rev"
          value={nextSourceRef}
          onChange={(event) => setNextSourceRef(event.target.value)}
          required
        />
        <Input
          aria-label="Nowa alokacja TEU"
          placeholder="20"
          value={nextAllotmentTeu}
          onChange={(event) => setNextAllotmentTeu(event.target.value)}
        />
        <Input
          aria-label="Nowy spot lub kontrakt"
          placeholder="spot|contract|other"
          value={nextSpotOrContract}
          onChange={(event) => setNextSpotOrContract(event.target.value)}
        />
        <Input
          aria-label="Nowy pin indeksu FSC"
          placeholder="FSC-Q4-2026"
          value={nextIndexId}
          onChange={(event) => setNextIndexId(event.target.value)}
        />
        <Input
          aria-label="Nowy identyfikator indeksu paliwowego"
          placeholder="uuid fuel_index"
          value={nextFuelIndexId}
          onChange={(event) => setNextFuelIndexId(event.target.value)}
        />
        <Button type="submit" variant="outline" disabled={supersedeMutation.isPending || !predecessorId}>
          Zastąp (nowy wiersz)
        </Button>
      </form>

      {supersedeMutation.isError ? <CatalogError error={supersedeMutation.error} /> : null}

      {query.isPending ? <p className="text-sm text-muted-foreground">Pobieranie stawek…</p> : null}
      {query.isError ? <CatalogError error={query.error} /> : null}

      {query.data ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.rateLines.tableKey}
          data={query.data}
          columns={columns}
          columnLabels={COLUMN_LABELS}
          allowCondensed
        />
      ) : null}
    </div>
  )
}
