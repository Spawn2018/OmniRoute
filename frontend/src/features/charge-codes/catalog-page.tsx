import { Link } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  chargeCodeCreateBody,
  createChargeCode,
  fetchChargeCodes,
  resolveChargeCode,
  type ChargeCode,
} from "@/lib/charge-codes-api"
import { getTenantContext } from "@/lib/tenant"

const columnHelper = createColumnHelper<ChargeCode>()

const columns = [
  columnHelper.accessor("code", {
    id: "code",
    header: "Kod",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("name", {
    id: "name",
    header: "Nazwa",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("aliases", {
    id: "aliases",
    header: "Aliasy",
    cell: (info) => info.getValue().join(", ") || "—",
  }),
]

const COLUMN_LABELS = {
  code: "Kod",
  name: "Nazwa",
  aliases: "Aliasy",
}

export function ChargeCodeCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [code, setCode] = useState("")
  const [name, setName] = useState("")
  const [aliasesText, setAliasesText] = useState("")
  const [lookup, setLookup] = useState("")
  const [resolved, setResolved] = useState<ChargeCode | null>(null)

  const query = useQuery({
    queryKey: ["charge-codes", ctx.organizationId],
    queryFn: fetchChargeCodes,
    enabled: Boolean(ctx.organizationId && ctx.userId),
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () => createChargeCode(chargeCodeCreateBody({ code, name, aliasesText })),
    onSuccess: () => {
      setCode("")
      setName("")
      setAliasesText("")
      void queryClient.invalidateQueries({ queryKey: ["charge-codes", ctx.organizationId] })
    },
  })

  const resolveMutation = useMutation({
    mutationFn: () => resolveChargeCode(lookup),
    onSuccess: (row) => {
      setResolved(row)
    },
    onError: () => {
      setResolved(null)
    },
  })

  return (
    <div className="space-y-3">
      <div>
        <h2 className="text-base font-semibold">Katalog kodów opłat</h2>
        <p className="text-xs text-muted-foreground">
          charge_code M-06 · typowany kod, nie luźny string
        </p>
      </div>

      {!ctx.organizationId || !ctx.userId ? (
        <div className="rounded-md border border-border bg-card p-3 text-sm">
          Ustaw identyfikatory sesji na stronie{" "}
          <Link className="underline" to="/session">
            Sesja
          </Link>
          .
        </div>
      ) : null}

      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-4"
        onSubmit={(event) => {
          event.preventDefault()
          createMutation.mutate()
        }}
      >
        <Input
          aria-label="Kod opłaty"
          placeholder="BAF"
          value={code}
          onChange={(event) => setCode(event.target.value)}
          required
        />
        <Input
          aria-label="Nazwa kodu opłaty"
          placeholder="Bunker Adjustment Factor"
          value={name}
          onChange={(event) => setName(event.target.value)}
          required
        />
        <Input
          aria-label="Aliasy kodu opłaty"
          placeholder="BUNKER, BAF_ADJ"
          value={aliasesText}
          onChange={(event) => setAliasesText(event.target.value)}
        />
        <Button type="submit" disabled={createMutation.isPending || !ctx.organizationId}>
          Dodaj kod
        </Button>
      </form>

      {createMutation.isError ? (
        <div className="rounded-md border border-destructive/40 bg-card p-3 text-sm text-destructive">
          {(createMutation.error as Error).message}
        </div>
      ) : null}

      <form
        className="flex gap-2 rounded-md border border-border bg-card p-3"
        onSubmit={(event) => {
          event.preventDefault()
          resolveMutation.mutate()
        }}
      >
        <Input
          aria-label="Sprawdź token kodu opłaty"
          placeholder="sprawdź kod albo alias"
          value={lookup}
          onChange={(event) => setLookup(event.target.value)}
        />
        <Button type="submit" variant="outline" disabled={resolveMutation.isPending || !lookup}>
          Rozwiąż
        </Button>
        {resolved ? (
          <div className="self-center font-mono text-xs">
            {resolved.code} · {resolved.name}
          </div>
        ) : null}
      </form>

      {resolveMutation.isError ? (
        <div className="rounded-md border border-destructive/40 bg-card p-3 text-sm text-destructive">
          {(resolveMutation.error as Error).message}
        </div>
      ) : null}

      {query.isLoading ? <div className="text-sm text-muted-foreground">Ładowanie…</div> : null}

      {query.isError ? (
        <div className="rounded-md border border-destructive/40 bg-card p-3 text-sm text-destructive">
          {(query.error as Error).message}
        </div>
      ) : null}

      {query.data ? (
        <DataTableShell
          tableKey="charge_codes"
          columns={columns}
          data={query.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Szukaj kodu opłaty…"
        />
      ) : null}
    </div>
  )
}
