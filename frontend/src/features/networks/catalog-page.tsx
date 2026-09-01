import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  createNetwork,
  fetchNetworks,
  networkCreateBody,
  resolveNetwork,
  type FreightNetwork,
} from "@/lib/networks-api"
import { getTenantContext } from "@/lib/tenant"
import {
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  ResolveTokenForm,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"

const helper = createColumnHelper<FreightNetwork>()
const columns = [
  helper.accessor("code", {
    header: "Kod",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  helper.accessor("name", { header: "Nazwa sieci" }),
  helper.accessor("is_global", {
    header: "Globalna",
    cell: (info) => (info.getValue() ? "tak" : "nie"),
  }),
  helper.accessor("region_scope", {
    header: "Zakres",
    cell: (info) => info.getValue() ?? "—",
  }),
  helper.accessor("aliases", {
    header: "Aliasy",
    cell: (info) => info.getValue().join(" · ") || "brak",
  }),
  helper.accessor("source_ref", { header: "Źródło" }),
]
const COLUMN_LABELS = {
  code: "Kod",
  name: "Nazwa sieci",
  is_global: "Globalna",
  region_scope: "Zakres",
  aliases: "Aliasy",
  source_ref: "Źródło",
}

const EMPTY_DRAFT = {
  code: "",
  name: "",
  aliasesText: "",
  website: "",
  regionScope: "",
  isGlobal: false,
}

export function NetworkCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_DRAFT)
  const [resolved, setResolved] = useState<FreightNetwork | null>(null)
  const sessionReady = Boolean(ctx.organizationId && ctx.userId)

  const query = useQuery({
    queryKey: ["networks", ctx.organizationId],
    queryFn: fetchNetworks,
    enabled: sessionReady,
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () => createNetwork(networkCreateBody(draft)),
    onSuccess: () => {
      setDraft(EMPTY_DRAFT)
      void queryClient.invalidateQueries({ queryKey: ["networks", ctx.organizationId] })
    },
  })

  const resolveMutation = useMutation({
    mutationFn: resolveNetwork,
    onSuccess: setResolved,
    onError: () => setResolved(null),
  })

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Katalog sieci i stowarzyszeń"
        subtitle="network M-12 · kopia per tenant · nie katalog agentów"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 lg:grid lg:grid-cols-4"
        onSubmit={(event) => {
          event.preventDefault()
          if (sessionReady) createMutation.mutate()
        }}
      >
        <Input
          aria-label="Kod sieci"
          placeholder="wca"
          maxLength={32}
          value={draft.code}
          onChange={(event) => setDraft({ ...draft, code: event.target.value })}
          required
        />
        <Input
          aria-label="Nazwa sieci"
          placeholder="WCA Worldwide"
          value={draft.name}
          onChange={(event) => setDraft({ ...draft, name: event.target.value })}
          required
        />
        <Input
          aria-label="Aliasy kodu sieci"
          placeholder="wca_ww"
          value={draft.aliasesText}
          onChange={(event) => setDraft({ ...draft, aliasesText: event.target.value })}
        />
        <Input
          aria-label="Strona sieci"
          placeholder="https://…"
          value={draft.website}
          onChange={(event) => setDraft({ ...draft, website: event.target.value })}
        />
        <Input
          aria-label="Zakres regionu"
          placeholder="PL albo global"
          value={draft.regionScope}
          onChange={(event) => setDraft({ ...draft, regionScope: event.target.value })}
        />
        <label className="flex items-center gap-2 text-xs">
          <input
            type="checkbox"
            checked={draft.isGlobal}
            onChange={(event) => setDraft({ ...draft, isGlobal: event.target.checked })}
          />
          sieć globalna
        </label>
        <Button type="submit" disabled={createMutation.isPending || !sessionReady}>
          Dodaj sieć
        </Button>
      </form>
      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}
      <ResolveTokenForm
        label="Sprawdź kod sieci"
        placeholder="wca albo alias"
        pending={resolveMutation.isPending}
        resolved={resolved === null ? null : `${resolved.code} · ${resolved.name}`}
        onResolve={(token) => resolveMutation.mutate(token)}
      />
      {resolveMutation.isError ? <CatalogError error={resolveMutation.error} /> : null}
      <CatalogLoadedTable
        tableKey={BUSINESS_LISTS.networks.tableKey}
        columns={columns}
        columnLabels={COLUMN_LABELS}
        data={query.data}
        loading={query.isLoading}
        error={query.error}
        globalFilterPlaceholder="Szukaj kodu sieci…"
      />
    </div>
  )
}
