import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  createNetwork,
  createNetworkMember,
  fetchNetworkMembers,
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
  const [networkId, setNetworkId] = useState("")
  const [memberCode, setMemberCode] = useState("")
  const [memberName, setMemberName] = useState("")
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
  const members = useQuery({
    queryKey: ["network-members", ctx.organizationId, networkId],
    queryFn: () => fetchNetworkMembers(networkId),
    enabled: sessionReady && networkId !== "",
    retry: false,
  })
  const createMember = useMutation({
    mutationFn: () =>
      createNetworkMember(networkId, {
        member_code: memberCode,
        legal_name: memberName,
      }),
    onSuccess: () => {
      setMemberCode("")
      setMemberName("")
      void queryClient.invalidateQueries({
        queryKey: ["network-members", ctx.organizationId, networkId],
      })
    },
  })

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Katalog sieci i stowarzyszeń"
        subtitle="network M-12 · kopia per tenant · ręczny członek · nie portal"
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
      <section className="space-y-2" data-network-member="catalog">
        <h2 className="text-sm font-medium">Członkowie sieci</h2>
        <label className="flex flex-col gap-1 text-xs">
          sieć
          <select
            aria-label="Sieć dla członka"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={networkId}
            onChange={(event) => setNetworkId(event.target.value)}
          >
            <option value="">Wybierz sieć</option>
            {(query.data ?? []).map((row) => (
              <option key={row.id} value={row.id}>
                {row.code} {row.name}
              </option>
            ))}
          </select>
        </label>
        <form
          className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 lg:grid lg:grid-cols-3"
          onSubmit={(event) => {
            event.preventDefault()
            if (sessionReady && networkId !== "") createMember.mutate()
          }}
        >
          <Input
            aria-label="Kod członka sieci"
            placeholder="agent_a"
            maxLength={32}
            value={memberCode}
            onChange={(event) => setMemberCode(event.target.value)}
            required
          />
          <Input
            aria-label="Nazwa członka sieci"
            placeholder="Agent Alpha"
            value={memberName}
            onChange={(event) => setMemberName(event.target.value)}
            required
          />
          <Button type="submit" disabled={createMember.isPending || !sessionReady || networkId === ""}>
            Dodaj członka
          </Button>
        </form>
        {createMember.isError ? <CatalogError error={createMember.error} /> : null}
        {members.isError ? <CatalogError error={members.error} /> : null}
        <ul className="text-xs">
          {(members.data ?? []).map((row) => (
            <li key={row.id}>
              {row.member_code} · {row.legal_name}
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}
