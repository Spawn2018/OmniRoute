import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  carrierInquiryBatchBody,
  createCarrierInquiry,
  createCarrierInquiryBatch,
  fetchCarrierInquiries,
  fetchCarrierInquiryRanking,
  inquiryIdsForMembers,
  topRankedMemberIds,
} from "@/lib/carrier-inquiries-api"
import { createMailDraftBatch, fetchMailDrafts, mailDraftBatchBody } from "@/lib/mail-drafts-api"
import { fetchOrganizationSettings, inquiryDefaultN } from "@/lib/organization-settings-api"
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
  const [memberPartyId, setMemberPartyId] = useState("")
  const [askedMemberId, setAskedMemberId] = useState("")
  const [batchMemberIds, setBatchMemberIds] = useState<string[]>([])
  const [batchOrigin, setBatchOrigin] = useState("")
  const [batchDestination, setBatchDestination] = useState("")
  const [draftInquiryIds, setDraftInquiryIds] = useState<string[]>([])
  const [draftBody, setDraftBody] = useState("prośba o stawkę")
  const [topApplied, setTopApplied] = useState(false)
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
  const inquiries = useQuery({
    queryKey: ["carrier-inquiries", ctx.organizationId],
    queryFn: fetchCarrierInquiries,
    enabled: sessionReady,
    retry: false,
  })
  const ranking = useQuery({
    queryKey: ["carrier-inquiry-ranking", ctx.organizationId],
    queryFn: fetchCarrierInquiryRanking,
    enabled: sessionReady,
    retry: false,
  })
  const settings = useQuery({
    queryKey: ["organization-settings", ctx.organizationId],
    queryFn: fetchOrganizationSettings,
    enabled: sessionReady,
    retry: false,
  })
  const drafts = useQuery({
    queryKey: ["mail-drafts", ctx.organizationId],
    queryFn: fetchMailDrafts,
    enabled: sessionReady,
    retry: false,
  })
  const defaultN = inquiryDefaultN(settings.data ?? [])
  const askMember = useMutation({
    mutationFn: () => createCarrierInquiry(askedMemberId),
    onSuccess: () => {
      setAskedMemberId("")
      void queryClient.invalidateQueries({
        queryKey: ["carrier-inquiries", ctx.organizationId],
      })
    },
  })
  const askBatch = useMutation({
    mutationFn: () =>
      createCarrierInquiryBatch(
        carrierInquiryBatchBody({
          memberIds: batchMemberIds,
          status: "queued",
          originPortId: batchOrigin,
          destinationPortId: batchDestination,
        }),
      ),
    onSuccess: () => {
      setBatchMemberIds([])
      setBatchOrigin("")
      setBatchDestination("")
      void queryClient.invalidateQueries({
        queryKey: ["carrier-inquiries", ctx.organizationId],
      })
    },
  })
  const saveDrafts = useMutation({
    mutationFn: () =>
      createMailDraftBatch(
        mailDraftBatchBody({
          subjectIds: draftInquiryIds,
          body: draftBody,
          sourceRef: "tenant:manual:inquiry-draft",
          subjectKind: "carrier_inquiry",
        }),
      ),
    onSuccess: () => {
      setDraftInquiryIds([])
      void queryClient.invalidateQueries({ queryKey: ["mail-drafts", ctx.organizationId] })
    },
  })
  const createMember = useMutation({
    mutationFn: () =>
      createNetworkMember(networkId, {
        member_code: memberCode,
        legal_name: memberName,
        party_id: memberPartyId,
      }),
    onSuccess: () => {
      setMemberCode("")
      setMemberName("")
      setMemberPartyId("")
      void queryClient.invalidateQueries({
        queryKey: ["network-members", ctx.organizationId, networkId],
      })
    },
  })

  useEffect(() => {
    if (topApplied || ranking.data === undefined || settings.isLoading) {
      return
    }
    const members = topRankedMemberIds(ranking.data, defaultN)
    setBatchMemberIds(members)
    setDraftInquiryIds(inquiryIdsForMembers(inquiries.data ?? [], members))
    setTopApplied(true)
  }, [topApplied, ranking.data, settings.isLoading, defaultN, inquiries.data])

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
          <Input
            aria-label="Kontrahent członka"
            placeholder="party_id"
            value={memberPartyId}
            onChange={(event) => setMemberPartyId(event.target.value)}
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
              {row.member_code} · {row.legal_name} · {row.party_id ?? "—"}
            </li>
          ))}
        </ul>
      </section>
      <section className="space-y-2" data-carrier-inquiry="catalog">
        <h2 className="text-sm font-medium">Zapytania do agentów</h2>
        <form
          className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 lg:flex-row"
          onSubmit={(event) => {
            event.preventDefault()
            if (sessionReady && askedMemberId !== "") askMember.mutate()
          }}
        >
          <select
            aria-label="Członek do zapytania"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={askedMemberId}
            onChange={(event) => setAskedMemberId(event.target.value)}
          >
            <option value="">Wybierz członka</option>
            {(members.data ?? []).map((row) => (
              <option key={row.id} value={row.id}>
                {row.member_code} {row.legal_name}
              </option>
            ))}
          </select>
          <Button type="submit" disabled={askMember.isPending || !sessionReady || askedMemberId === ""}>
            Zapisz zapytanie
          </Button>
        </form>
        {askMember.isError ? <CatalogError error={askMember.error} /> : null}
        <form
          className="grid gap-2 rounded-md border border-border bg-card p-3"
          data-carrier-inquiry="batch"
          onSubmit={(event) => {
            event.preventDefault()
            if (sessionReady && batchMemberIds.length > 0) askBatch.mutate()
          }}
        >
          <p className="text-xs text-muted-foreground">
            Paczka queued: jeden, wielu albo wszyscy. Nie wysyłka.
          </p>
          <div className="flex flex-wrap gap-2 text-xs">
            {(members.data ?? []).map((row) => (
              <label key={row.id} className="flex items-center gap-1">
                <input
                  type="checkbox"
                  checked={batchMemberIds.includes(row.id)}
                  onChange={(event) => {
                    if (event.target.checked) {
                      setBatchMemberIds([...batchMemberIds, row.id])
                      return
                    }
                    setBatchMemberIds(batchMemberIds.filter((item) => item !== row.id))
                  }}
                />
                {row.member_code}
              </label>
            ))}
          </div>
          <Button
            type="button"
            onClick={() => setBatchMemberIds((members.data ?? []).map((row) => row.id))}
          >
            Wszyscy członkowie
          </Button>
          <Button
            type="button"
            onClick={() => setBatchMemberIds(topRankedMemberIds(ranking.data ?? [], defaultN))}
          >
            Zaznacz top N
          </Button>
          <Input
            aria-label="POL paczki zapytań"
            placeholder="origin_port_id"
            value={batchOrigin}
            onChange={(event) => setBatchOrigin(event.target.value)}
          />
          <Input
            aria-label="POD paczki zapytań"
            placeholder="destination_port_id"
            value={batchDestination}
            onChange={(event) => setBatchDestination(event.target.value)}
          />
          <Button type="submit" disabled={askBatch.isPending || !sessionReady || batchMemberIds.length === 0}>
            Zapisz paczkę zapytań
          </Button>
        </form>
        {askBatch.isError ? <CatalogError error={askBatch.error} /> : null}
        {ranking.isError ? <CatalogError error={ranking.error} /> : null}
        {inquiries.isError ? <CatalogError error={inquiries.error} /> : null}
        <form
          className="grid gap-2 rounded-md border border-border bg-card p-3"
          data-mail-draft="batch"
          onSubmit={(event) => {
            event.preventDefault()
            if (sessionReady && draftInquiryIds.length > 0) saveDrafts.mutate()
          }}
        >
          <p className="text-xs text-muted-foreground">
            Szkice zapytań: top {defaultN} z rankingu answered (`inquiry_default_n`). Nie wysyłka.
          </p>
          <div className="flex flex-wrap gap-2 text-xs">
            {(inquiries.data ?? []).map((row) => (
              <label key={row.id} className="flex items-center gap-1">
                <input
                  type="checkbox"
                  checked={draftInquiryIds.includes(row.id)}
                  onChange={(event) => {
                    if (event.target.checked) {
                      setDraftInquiryIds([...draftInquiryIds, row.id])
                      return
                    }
                    setDraftInquiryIds(draftInquiryIds.filter((item) => item !== row.id))
                  }}
                />
                {row.status} · {row.network_member_id}
              </label>
            ))}
          </div>
          <Button
            type="button"
            onClick={() =>
              setDraftInquiryIds(
                inquiryIdsForMembers(inquiries.data ?? [], topRankedMemberIds(ranking.data ?? [], defaultN)),
              )
            }
          >
            Top N z rankingu
          </Button>
          <Input
            aria-label="Treść szkiców zapytań"
            value={draftBody}
            onChange={(event) => setDraftBody(event.target.value)}
          />
          <Button type="submit" disabled={saveDrafts.isPending || !sessionReady || draftInquiryIds.length === 0}>
            Zapisz szkice
          </Button>
        </form>
        {saveDrafts.isError ? <CatalogError error={saveDrafts.error} /> : null}
        <ul className="text-xs">
          {(drafts.data ?? [])
            .filter((row) => row.subject_kind === "carrier_inquiry")
            .map((row) => (
              <li key={row.id}>
                {row.status} · {row.subject_id}
              </li>
            ))}
        </ul>
      </section>
    </div>
  )
}
