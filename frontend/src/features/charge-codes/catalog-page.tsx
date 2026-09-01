import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  ResolveTokenForm,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
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
import { BUSINESS_LISTS } from "@/lib/business-lists"
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
    mutationFn: (token: string) => resolveChargeCode(token),
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
        title="Katalog kodów opłat"
        subtitle="charge_code M-06 · typowany kod, nie luźny string"
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

      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}

      <ResolveTokenForm
        label="Sprawdź token kodu opłaty"
        placeholder="sprawdź kod albo alias"
        pending={resolveMutation.isPending}
        resolved={resolved === null ? null : `${resolved.code} · ${resolved.name}`}
        onResolve={(token) => resolveMutation.mutate(token)}
      />

      {resolveMutation.isError ? <CatalogError error={resolveMutation.error} /> : null}

      {query.isLoading ? <div className="text-sm text-muted-foreground">Ładowanie…</div> : null}

      {query.isError ? <CatalogError error={query.error} /> : null}

      {query.data ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.chargeCodes.tableKey}
          columns={columns}
          data={query.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Szukaj kodu opłaty…"
        />
      ) : null}
    </div>
  )
}
