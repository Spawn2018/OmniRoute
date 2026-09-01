import { useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import {
  TenantSessionNotice,
  CatalogHeading,
  CatalogError,
  ResolveTokenForm,
} from "@/components/catalog/catalog-parts"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { getTenantContext } from "@/lib/tenant"
import {
  createTerminal,
  fetchTerminals,
  resolveTerminal,
  terminalCreateBody,
  type Terminal,
} from "@/lib/terminals-api"

const columnHelper = createColumnHelper<Terminal>()

const columns = [
  columnHelper.accessor("name", {
    id: "name",
    header: "Nazwa",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("isps_code", {
    id: "isps_code",
    header: "ISPS",
    cell: (info) => <span className="font-mono text-xs">{info.getValue() ?? "—"}</span>,
  }),
  columnHelper.accessor("operator_name", {
    id: "operator_name",
    header: "Operator",
    cell: (info) => info.getValue() ?? "—",
  }),
  columnHelper.accessor("port_id", {
    id: "port_id",
    header: "Port",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
]

const COLUMN_LABELS = {
  name: "Nazwa",
  isps_code: "ISPS",
  operator_name: "Operator",
  port_id: "Port",
}

export function TerminalCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [portFilter, setPortFilter] = useState("")
  const [portId, setPortId] = useState("")
  const [name, setName] = useState("")
  const [ispsCode, setIspsCode] = useState("")
  const [operatorName, setOperatorName] = useState("")
  const [resolved, setResolved] = useState<Terminal | null>(null)

  const query = useQuery({
    queryKey: ["terminals", ctx.organizationId, portFilter],
    queryFn: () => fetchTerminals(portFilter),
    enabled: Boolean(ctx.organizationId && ctx.userId),
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () =>
      createTerminal(terminalCreateBody({ portId, name, ispsCode, operatorName })),
    onSuccess: () => {
      setPortId("")
      setName("")
      setIspsCode("")
      setOperatorName("")
      void queryClient.invalidateQueries({ queryKey: ["terminals", ctx.organizationId] })
    },
  })

  const resolveMutation = useMutation({
    mutationFn: (token: string) => resolveTerminal(token),
    onSuccess: (row) => {
      setResolved(row)
    },
    onError: () => {
      setResolved(null)
    },
  })

  const resolvedLabel =
    resolved === null ? null : `${resolved.isps_code ?? "—"} · ${resolved.name}`

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Katalog terminali"
        subtitle="terminal M-05 · ISPS per tenant, operator jako tekst"
      />

      {!ctx.organizationId || !ctx.userId ? <TenantSessionNotice /> : null}

      <label className="flex items-center gap-2 text-sm">
        Filtruj po porcie
        <Input
          aria-label="Filtruj terminale po porcie"
          placeholder="port_id"
          value={portFilter}
          onChange={(event) => setPortFilter(event.target.value)}
        />
      </label>

      {query.isLoading ? <p className="text-sm text-muted-foreground">Ładowanie…</p> : null}
      {query.isError ? <CatalogError error={query.error} /> : null}

      {query.data ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.terminals.tableKey}
          columns={columns}
          data={query.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Filtruj pobrane terminale…"
        />
      ) : null}

      <fieldset className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-2">
        <legend className="px-1 text-sm font-medium">Nowy terminal</legend>
        <form
          className="contents"
          onSubmit={(event) => {
            event.preventDefault()
            createMutation.mutate()
          }}
        >
          <Input
            aria-label="Identyfikator portu"
            placeholder="port_id"
            value={portId}
            onChange={(event) => setPortId(event.target.value)}
            required
          />
          <Input
            aria-label="Nazwa terminalu"
            placeholder="BCT Gdynia"
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
          />
          <Input
            aria-label="Kod ISPS"
            placeholder="PLGDY-BCT"
            value={ispsCode}
            onChange={(event) => setIspsCode(event.target.value)}
          />
          <Input
            aria-label="Operator terminalu"
            placeholder="BCT"
            value={operatorName}
            onChange={(event) => setOperatorName(event.target.value)}
          />
          <Button type="submit" disabled={createMutation.isPending || !ctx.organizationId}>
            Dodaj terminal
          </Button>
        </form>
      </fieldset>

      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}

      <ResolveTokenForm
        label="Sprawdź kod ISPS"
        placeholder="PLGDY-BCT"
        pending={resolveMutation.isPending}
        resolved={resolvedLabel}
        onResolve={(token) => resolveMutation.mutate(token)}
      />

      {resolveMutation.isError ? <CatalogError error={resolveMutation.error} /> : null}
    </div>
  )
}
