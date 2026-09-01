import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import {
  CatalogCreateForm,
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  ResolveTokenForm,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import {
  commodityCodeCreateBody,
  createCommodityCode,
  fetchCommodityCodes,
  resolveCommodityCode,
  type CommodityCode,
} from "@/lib/commodity-codes-api"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { getTenantContext } from "@/lib/tenant"

const columnHelper = createColumnHelper<CommodityCode>()

const columns = [
  columnHelper.accessor("code", {
    id: "code",
    header: "Kod CN",
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
    header: "Pochodzenie",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
]

const COLUMN_LABELS = {
  code: "Kod CN",
  name: "Nazwa",
  aliases: "Aliasy",
  source_ref: "Pochodzenie",
}

export function CommodityCodeCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [code, setCode] = useState("")
  const [name, setName] = useState("")
  const [aliasesText, setAliasesText] = useState("")
  const [resolved, setResolved] = useState<CommodityCode | null>(null)

  const query = useQuery({
    queryKey: ["commodity-codes", ctx.organizationId],
    queryFn: fetchCommodityCodes,
    enabled: Boolean(ctx.organizationId && ctx.userId),
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () => createCommodityCode(commodityCodeCreateBody({ code, name, aliasesText })),
    onSuccess: () => {
      setCode("")
      setName("")
      setAliasesText("")
      void queryClient.invalidateQueries({ queryKey: ["commodity-codes", ctx.organizationId] })
    },
  })

  const resolveMutation = useMutation({
    mutationFn: (token: string) => resolveCommodityCode(token),
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
        title="Katalog kodów towarowych"
        subtitle="commodity_code M-09 · HS/CN cyframi, nie luźna nazwa · nie podpina wyceny"
      />

      {!ctx.organizationId || !ctx.userId ? <TenantSessionNotice /> : null}

      <CatalogCreateForm
        code={code}
        name={name}
        aliasesText={aliasesText}
        onCodeChange={setCode}
        onNameChange={setName}
        onAliasesChange={setAliasesText}
        codeLabel="Kod towarowy"
        nameLabel="Nazwa kodu towarowego"
        aliasesLabel="Aliasy kodu towarowego"
        codePlaceholder="0805"
        namePlaceholder="Owoce cytrusowe"
        aliasesPlaceholder="080510"
        submitLabel="Dodaj kod"
        pending={createMutation.isPending}
        disabled={!ctx.organizationId}
        onSubmit={() => createMutation.mutate()}
      />

      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}

      <ResolveTokenForm
        label="Sprawdź kod CN"
        placeholder="0805 albo alias"
        pending={resolveMutation.isPending}
        resolved={resolved === null ? null : `${resolved.code} · ${resolved.name}`}
        onResolve={(token) => resolveMutation.mutate(token)}
      />

      {resolveMutation.isError ? <CatalogError error={resolveMutation.error} /> : null}

      <CatalogLoadedTable
        loading={query.isLoading}
        error={query.error}
        data={query.data}
        tableKey={BUSINESS_LISTS.commodityCodes.tableKey}
        columns={columns}
        columnLabels={COLUMN_LABELS}
        globalFilterPlaceholder="Szukaj kodu towarowego…"
      />
    </div>
  )
}
