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
  createPort,
  fetchPorts,
  portCreateBody,
  resolvePort,
  type Port,
} from "@/lib/ports-api"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { getTenantContext } from "@/lib/tenant"

const columnHelper = createColumnHelper<Port>()

const columns = [
  columnHelper.accessor("unlocode", {
    id: "unlocode",
    header: "UN/LOCODE",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("name", {
    id: "name",
    header: "Nazwa",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("country_code", {
    id: "country_code",
    header: "Kraj",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("function_flags", {
    id: "function_flags",
    header: "Funkcje",
    cell: (info) => info.getValue().join(", ") || "—",
  }),
  columnHelper.accessor("aliases", {
    id: "aliases",
    header: "Aliasy",
    cell: (info) => info.getValue().join(", ") || "—",
  }),
  columnHelper.accessor("is_official", {
    id: "is_official",
    header: "Pochodzenie",
    cell: (info) => (info.getValue() ? "UN/LOCODE" : "własny"),
  }),
  columnHelper.accessor("wpi_number", {
    id: "wpi_number",
    header: "WPI",
    cell: (info) => info.getValue() ?? "—",
  }),
  columnHelper.accessor("harbor_size", {
    id: "harbor_size",
    header: "Wielkość",
    cell: (info) => info.getValue() ?? "—",
  }),
  columnHelper.accessor("harbor_type", {
    id: "harbor_type",
    header: "Typ",
    cell: (info) => info.getValue() ?? "—",
  }),
  columnHelper.accessor("shelter", {
    id: "shelter",
    header: "Schronienie",
    cell: (info) => info.getValue() ?? "—",
  }),
]

const COLUMN_LABELS = {
  unlocode: "UN/LOCODE",
  name: "Nazwa",
  country_code: "Kraj",
  function_flags: "Funkcje",
  aliases: "Aliasy",
  is_official: "Pochodzenie",
  wpi_number: "WPI",
  harbor_size: "Wielkość",
  harbor_type: "Typ",
  shelter: "Schronienie",
}

export function PortCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [search, setSearch] = useState("")
  const [unlocode, setUnlocode] = useState("")
  const [name, setName] = useState("")
  const [countryCode, setCountryCode] = useState("")
  const [aliasesText, setAliasesText] = useState("")
  const [resolved, setResolved] = useState<Port | null>(null)

  const query = useQuery({
    queryKey: ["ports", ctx.organizationId, search],
    queryFn: () => fetchPorts(search),
    enabled: Boolean(ctx.organizationId && ctx.userId),
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () => createPort(portCreateBody({ unlocode, name, countryCode, aliasesText })),
    onSuccess: () => {
      setUnlocode("")
      setName("")
      setCountryCode("")
      setAliasesText("")
      void queryClient.invalidateQueries({ queryKey: ["ports", ctx.organizationId] })
    },
  })

  const resolveMutation = useMutation({
    mutationFn: (token: string) => resolvePort(token),
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
        title="Katalog portów"
        subtitle="port M-05 · UN/LOCODE per tenant, nie luźna nazwa miejscowości"
      />

      {!ctx.organizationId || !ctx.userId ? <TenantSessionNotice /> : null}

      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-5"
        onSubmit={(event) => {
          event.preventDefault()
          createMutation.mutate()
        }}
      >
        <Input
          aria-label="Kod UN/LOCODE"
          placeholder="PLGDY"
          value={unlocode}
          onChange={(event) => setUnlocode(event.target.value)}
          required
        />
        <Input
          aria-label="Nazwa portu"
          placeholder="Gdynia"
          value={name}
          onChange={(event) => setName(event.target.value)}
          required
        />
        <Input
          aria-label="Kod kraju"
          placeholder="PL"
          value={countryCode}
          onChange={(event) => setCountryCode(event.target.value)}
          required
        />
        <Input
          aria-label="Aliasy portu"
          placeholder="Gdingen, Gdynia Port"
          value={aliasesText}
          onChange={(event) => setAliasesText(event.target.value)}
        />
        <Button type="submit" disabled={createMutation.isPending || !ctx.organizationId}>
          Dodaj port
        </Button>
      </form>

      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}

      <ResolveTokenForm
        label="Sprawdź token portu"
        placeholder="Gdingen"
        pending={resolveMutation.isPending}
        resolved={resolved === null ? null : `${resolved.unlocode} · ${resolved.name}`}
        onResolve={(token) => resolveMutation.mutate(token)}
      />

      {resolveMutation.isError ? <CatalogError error={resolveMutation.error} /> : null}

      <form
        className="flex gap-2 rounded-md border border-border bg-card p-3"
        onSubmit={(event) => {
          event.preventDefault()
          void query.refetch()
        }}
      >
        <Input
          aria-label="Szukaj portu w bazie"
          placeholder="szukaj po kodzie albo nazwie"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <Button type="submit" variant="outline">
          Szukaj
        </Button>
      </form>

      {query.isLoading ? <div className="text-sm text-muted-foreground">Ładowanie…</div> : null}

      {query.isError ? <CatalogError error={query.error} /> : null}

      {query.data ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.ports.tableKey}
          columns={columns}
          data={query.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Filtruj pobrane porty…"
        />
      ) : null}
    </div>
  )
}
