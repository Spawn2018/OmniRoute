import { Link } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
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
  superseded_by: "Zastąpiona przez",
}

export function RateLineCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [chargeCode, setChargeCode] = useState("")
  const [amount, setAmount] = useState("")
  const [currency, setCurrency] = useState("EUR")
  const [sourceRef, setSourceRef] = useState("")
  const [predecessorId, setPredecessorId] = useState("")
  const [nextAmount, setNextAmount] = useState("")
  const [nextCurrency, setNextCurrency] = useState("EUR")
  const [nextSourceRef, setNextSourceRef] = useState("")

  const query = useQuery({
    queryKey: ["rate-lines", ctx.organizationId],
    queryFn: fetchRateLines,
    enabled: Boolean(ctx.organizationId && ctx.userId),
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () =>
      createRateLine(rateLineCreateBody({ chargeCode, amount, currency, sourceRef })),
    onSuccess: () => {
      setChargeCode("")
      setAmount("")
      setSourceRef("")
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
        }),
      ),
    onSuccess: () => {
      setPredecessorId("")
      setNextAmount("")
      setNextSourceRef("")
      void queryClient.invalidateQueries({ queryKey: ["rate-lines", ctx.organizationId] })
    },
  })

  return (
    <div className="space-y-3">
      <div>
        <h2 className="text-base font-semibold">Stawki kupna</h2>
        <p className="text-xs text-muted-foreground">
          rate_line M-07 · niemutowalna · source_ref obowiązkowy · nie tabela charge
        </p>
      </div>

      {ctx.organizationId && ctx.userId ? null : (
        <p className="text-sm">
          Brak sesji tenanta — ustaw ją na{" "}
          <Link className="underline" to="/session">
            Sesja
          </Link>
          .
        </p>
      )}

      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-5"
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
        <Button type="submit" disabled={createMutation.isPending || !ctx.organizationId}>
          Dodaj stawkę
        </Button>
      </form>

      {createMutation.isError ? (
        <p className="text-sm text-destructive">{(createMutation.error as Error).message}</p>
      ) : null}

      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-5"
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
        <Button type="submit" variant="outline" disabled={supersedeMutation.isPending || !predecessorId}>
          Zastąp (nowy wiersz)
        </Button>
      </form>

      {supersedeMutation.isError ? (
        <p className="text-sm text-destructive">{(supersedeMutation.error as Error).message}</p>
      ) : null}

      {query.isPending ? <p className="text-sm text-muted-foreground">Pobieranie stawek…</p> : null}
      {query.isError ? <p className="text-sm text-destructive">{(query.error as Error).message}</p> : null}

      {query.data ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.rateLines.tableKey}
          columns={columns}
          data={query.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Szukaj stawki kupna…"
        />
      ) : null}
    </div>
  )
}
