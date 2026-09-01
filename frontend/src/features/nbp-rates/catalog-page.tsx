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
  createNbpRate,
  fetchNbpRates,
  nbpRateCreateBody,
  resolveNbpRate,
  type NbpRate,
} from "@/lib/nbp-rates-api"
import { getTenantContext } from "@/lib/tenant"

const columnHelper = createColumnHelper<NbpRate>()

const columns = [
  columnHelper.accessor("currency", {
    id: "currency",
    header: "Waluta",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("rate_date", {
    id: "rate_date",
    header: "Data tabeli A",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("mid", {
    id: "mid",
    header: "Kurs średni",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("source_ref", {
    id: "source_ref",
    header: "Pochodzenie",
    cell: (info) => info.getValue(),
  }),
]

const COLUMN_LABELS = {
  currency: "Waluta ISO",
  rate_date: "Dzień tabeli A",
  mid: "Kurs średni tabeli A",
  source_ref: "source_ref",
}

export function NbpRateCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [currency, setCurrency] = useState("")
  const [rateDate, setRateDate] = useState("")
  const [mid, setMid] = useState("")
  const [lookupCurrency, setLookupCurrency] = useState("")
  const [lookupDate, setLookupDate] = useState("")
  const [resolved, setResolved] = useState<NbpRate | null>(null)

  const query = useQuery({
    queryKey: ["nbp-rates", ctx.organizationId],
    queryFn: fetchNbpRates,
    enabled: Boolean(ctx.organizationId && ctx.userId),
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () => createNbpRate(nbpRateCreateBody({ currency, rateDate, mid })),
    onSuccess: () => {
      setCurrency("")
      setRateDate("")
      setMid("")
      void queryClient.invalidateQueries({ queryKey: ["nbp-rates", ctx.organizationId] })
    },
  })

  const resolveMutation = useMutation({
    mutationFn: () => resolveNbpRate(lookupCurrency.trim().toUpperCase(), lookupDate),
    onSuccess: (row) => {
      setResolved(row)
    },
    onError: () => {
      setResolved(null)
    },
  })

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Katalog kursów NBP"
        subtitle="nbp_rate M-23 · tabela A, mid Decimal · nie przelicza wyceny"
      />

      {!ctx.organizationId || !ctx.userId ? <TenantSessionNotice /> : null}

      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-4"
        onSubmit={(event) => {
          event.preventDefault()
          createMutation.mutate()
        }}
      >
        <Input
          aria-label="Waluta ISO"
          placeholder="EUR"
          maxLength={3}
          value={currency}
          onChange={(event) => setCurrency(event.target.value)}
          required
        />
        <Input
          aria-label="Data tabeli A"
          type="date"
          value={rateDate}
          onChange={(event) => setRateDate(event.target.value)}
          required
        />
        <Input
          aria-label="Kurs średni"
          placeholder="4.2500"
          inputMode="decimal"
          value={mid}
          onChange={(event) => setMid(event.target.value)}
          required
        />
        <Button type="submit" disabled={createMutation.isPending || !ctx.organizationId}>
          Dodaj kurs
        </Button>
      </form>

      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}

      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-3"
        onSubmit={(event) => {
          event.preventDefault()
          resolveMutation.mutate()
        }}
      >
        <Input
          aria-label="Sprawdź walutę"
          placeholder="USD"
          maxLength={3}
          value={lookupCurrency}
          onChange={(event) => setLookupCurrency(event.target.value)}
        />
        <Input
          aria-label="Sprawdź datę kursu"
          type="date"
          value={lookupDate}
          onChange={(event) => setLookupDate(event.target.value)}
        />
        <Button
          type="submit"
          variant="outline"
          disabled={resolveMutation.isPending || !lookupCurrency || !lookupDate}
        >
          Rozwiąż
        </Button>
        {resolved ? (
          <div className="font-mono text-xs md:col-span-3">
            {resolved.currency} · {resolved.rate_date} · {resolved.mid}
          </div>
        ) : null}
      </form>

      {resolveMutation.isError ? <CatalogError error={resolveMutation.error} /> : null}

      <CatalogLoadedTable
        tableKey={BUSINESS_LISTS.nbpRates.tableKey}
        globalFilterPlaceholder="Szukaj waluty albo daty kursu…"
        columnLabels={COLUMN_LABELS}
        columns={columns}
        data={query.data}
        error={query.error}
        loading={query.isLoading}
      />
    </div>
  )
}
