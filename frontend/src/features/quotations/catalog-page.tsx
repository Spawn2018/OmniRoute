import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { createQuotation, fetchQuotations, quotationCreateBody, type Quotation } from "@/lib/quotations-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<Quotation>()

const columns = [
  helper.accessor("charge_code", { header: "Kod opłaty" }),
  helper.accessor("amount", {
    header: "Kwota ze stawki",
    cell: ({ row }) => <Money amount={row.original.amount} currency={row.original.currency} />,
  }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
  helper.accessor("rate_line_id", { header: "Stawka" }),
]

const COLUMN_LABELS = {
  charge_code: "Kod opłaty",
  amount: "Kwota ze stawki",
  source_ref: "Pochodzenie",
  rate_line_id: "Stawka",
}

export function QuotationCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [chargeCode, setChargeCode] = useState("")
  const signedIn = Boolean(ctx.organizationId && ctx.userId)

  const query = useQuery({
    queryKey: ["quotations", ctx.organizationId],
    queryFn: fetchQuotations,
    enabled: signedIn,
    retry: false,
  })

  const quoteMutation = useMutation({
    mutationFn: () => createQuotation(quotationCreateBody(chargeCode)),
    onSuccess: () => {
      setChargeCode("")
      void queryClient.invalidateQueries({ queryKey: ["quotations", ctx.organizationId] })
    },
  })

  return (
    <section className="space-y-3">
      <header>
        <h2 className="text-base font-semibold">Wyceny</h2>
        <p className="text-xs text-muted-foreground">
          quotation M-21 · kwota z bieżącego rate_line w SQL · nie licz w formularzu
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
        <Button type="submit" disabled={quoteMutation.isPending || !signedIn}>
          Wycen z bieżącej stawki
        </Button>
      </form>

      {quoteMutation.isError ? (
        <p className="text-sm text-destructive">{(quoteMutation.error as Error).message}</p>
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
