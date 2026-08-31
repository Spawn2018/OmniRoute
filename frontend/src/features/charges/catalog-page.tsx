import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { chargeCreateBody, createCharge, fetchCharges, type Charge } from "@/lib/charges-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<Charge>()

function moneyCell(amount: string, currency: string) {
  return <Money amount={amount} currency={currency} />
}

const columns = [
  helper.accessor("charge_code", { header: "Kod opłaty" }),
  helper.accessor("buy_amount", {
    header: "Kupno",
    cell: ({ row }) => moneyCell(row.original.buy_amount, row.original.buy_currency),
  }),
  helper.accessor("sell_amount", {
    header: "Sprzedaż",
    cell: ({ row }) => moneyCell(row.original.sell_amount, row.original.sell_currency),
  }),
  helper.accessor("margin_amount", {
    header: "Marża",
    cell: ({ row }) => moneyCell(row.original.margin_amount, row.original.margin_currency),
  }),
  helper.accessor("rate_line_id", {
    header: "Stawka kupna",
    cell: ({ getValue }) => getValue() ?? "—",
  }),
]

const COLUMN_LABELS = {
  charge_code: "Kod opłaty",
  buy_amount: "Kupno",
  sell_amount: "Sprzedaż",
  margin_amount: "Marża",
  rate_line_id: "Stawka kupna",
}

type Draft = {
  chargeCode: string
  buyAmount: string
  sellAmount: string
  currency: string
  rateLineId: string
}

const EMPTY_DRAFT: Draft = {
  chargeCode: "",
  buyAmount: "",
  sellAmount: "",
  currency: "EUR",
  rateLineId: "",
}

export function ChargeCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [draft, setDraft] = useState<Draft>(EMPTY_DRAFT)
  const signedIn = Boolean(ctx.organizationId && ctx.userId)

  const query = useQuery({
    queryKey: ["charges", ctx.organizationId],
    queryFn: fetchCharges,
    enabled: signedIn,
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () => createCharge(chargeCreateBody(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_DRAFT, currency: draft.currency })
      void queryClient.invalidateQueries({ queryKey: ["charges", ctx.organizationId] })
    },
  })

  const setField = (field: keyof Draft) => (event: { target: { value: string } }) => {
    setDraft((current) => ({ ...current, [field]: event.target.value }))
  }

  return (
    <section className="space-y-3">
      <header>
        <h2 className="text-base font-semibold">Opłaty</h2>
        <p className="text-xs text-muted-foreground">
          charge M-08 · buy i sell na jednym wierszu · marża w kodzie · nie accept HITL
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
          createMutation.mutate()
        }}
      >
        <Input aria-label="Kod opłaty" placeholder="THC" value={draft.chargeCode} onChange={setField("chargeCode")} required />
        <Input aria-label="Kwota kupna" placeholder="10.5000" value={draft.buyAmount} onChange={setField("buyAmount")} required />
        <Input aria-label="Kwota sprzedaży" placeholder="14.0000" value={draft.sellAmount} onChange={setField("sellAmount")} required />
        <Input aria-label="Waluta ISO" placeholder="EUR" value={draft.currency} onChange={setField("currency")} required />
        <Input aria-label="Identyfikator stawki kupna" placeholder="rate_line (opcjonalnie)" value={draft.rateLineId} onChange={setField("rateLineId")} />
        <Button type="submit" disabled={createMutation.isPending || !signedIn}>
          Dodaj opłatę
        </Button>
      </form>

      {createMutation.isError ? (
        <p className="text-sm text-destructive">{(createMutation.error as Error).message}</p>
      ) : null}
      {query.isPending ? <p className="text-sm text-muted-foreground">Pobieranie opłat…</p> : null}
      {query.isError ? <p className="text-sm text-destructive">{(query.error as Error).message}</p> : null}
      {query.data ? (
        <DataTableShell
          tableKey="charges"
          columns={columns}
          data={query.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Szukaj opłaty…"
        />
      ) : null}
    </section>
  )
}
