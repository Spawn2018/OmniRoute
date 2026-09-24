import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { type FormEvent, useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  CatalogSourceRefField,
  ResolveTokenForm,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
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
  columnHelper.accessor("source_ref", {
    id: "source_ref",
    header: "Źródło",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
]

const COLUMN_LABELS = {
  code: "Kod",
  name: "Nazwa",
  aliases: "Aliasy",
  source_ref: "Źródło",
}

export function ChargeCodeCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [code, setCode] = useState("")
  const [name, setName] = useState("")
  const [aliasesText, setAliasesText] = useState("")
  const [sourceRef, setSourceRef] = useState("tenant:manual")
  const [resolved, setResolved] = useState<ChargeCode | null>(null)

  const query = useQuery({
    queryKey: ["charge-codes", ctx.organizationId],
    queryFn: fetchChargeCodes,
    enabled: Boolean(ctx.organizationId && ctx.userId),
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () =>
      createChargeCode(chargeCodeCreateBody({ code, name, aliasesText, sourceRef })),
    onSuccess: () => {
      setCode("")
      setName("")
      setAliasesText("")
      setSourceRef("tenant:manual")
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
        subtitle="charge_code M-06 · typowany kod z source_ref · WAITING/NO_SHOW/DIVERSION/STAMP jak każdy token"
      />

      {!ctx.organizationId || !ctx.userId ? <TenantSessionNotice /> : null}

      <form
        className="grid max-w-lg gap-3"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (ctx.organizationId) createMutation.mutate()
        }}
      >
        <label className="flex flex-col gap-1 text-xs">
          Kod opłaty
          <Input
            aria-label="Kod opłaty"
            className="font-mono"
            placeholder="BAF"
            value={code}
            onChange={(change) => setCode(change.target.value)}
            required
          />
        </label>
        <label className="flex flex-col gap-1 text-xs">
          Nazwa kodu opłaty
          <Input
            aria-label="Nazwa kodu opłaty"
            placeholder="Bunker Adjustment Factor"
            value={name}
            onChange={(change) => setName(change.target.value)}
            required
          />
        </label>
        <label className="flex flex-col gap-1 text-xs">
          Aliasy kodu opłaty
          <Input
            aria-label="Aliasy kodu opłaty"
            placeholder="BUNKER, BAF_ADJ"
            value={aliasesText}
            onChange={(change) => setAliasesText(change.target.value)}
          />
        </label>
        <CatalogSourceRefField
          label="source_ref (tenant:manual albo fixture://charge-code/…)"
          ariaLabel="Pochodzenie kodu opłaty"
          value={sourceRef}
          onChange={setSourceRef}
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

      <CatalogLoadedTable
        loading={query.isLoading}
        error={query.error}
        data={query.data}
        tableKey={BUSINESS_LISTS.chargeCodes.tableKey}
        columns={columns}
        columnLabels={COLUMN_LABELS}
        globalFilterPlaceholder="Szukaj kodu opłaty…"
      />
    </div>
  )
}
