import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  EMPTY_SCORECARD_DRAFT,
  fetchPartyScorecards,
  scorecardUpsertBody,
  upsertPartyScorecard,
  type PartyScorecard,
} from "@/lib/party-scorecards-api"
import { getTenantContext } from "@/lib/tenant"
import {
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"

const helper = createColumnHelper<PartyScorecard>()
const columns = [
  helper.accessor("party_id", {
    header: "Kontrahent",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  helper.accessor("response_rate", {
    header: "Odpowiedź",
    cell: (info) => info.getValue() ?? "—",
  }),
  helper.accessor("median_response_hours", {
    header: "Mediana h",
    cell: (info) => info.getValue() ?? "—",
  }),
  helper.accessor("price_position", {
    header: "Cena",
    cell: (info) => info.getValue() ?? "—",
  }),
  helper.accessor("sample_size", { header: "Próba" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]
const COLUMN_LABELS = {
  party_id: "Kontrahent",
  response_rate: "Odpowiedź",
  median_response_hours: "Mediana h",
  price_position: "Cena",
  sample_size: "Próba",
  source_ref: "Źródło",
}

export function PartyScorecardCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_SCORECARD_DRAFT)
  const sessionReady = Boolean(ctx.organizationId && ctx.userId)

  const query = useQuery({
    queryKey: ["party-scorecards", ctx.organizationId],
    queryFn: fetchPartyScorecards,
    enabled: sessionReady,
    retry: false,
  })

  const saveMutation = useMutation({
    mutationFn: () => upsertPartyScorecard(draft.partyId.trim(), scorecardUpsertBody(draft)),
    onSuccess: () => {
      setDraft(EMPTY_SCORECARD_DRAFT)
      void queryClient.invalidateQueries({ queryKey: ["party-scorecards", ctx.organizationId] })
    },
  })

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Karty wyników kontrahenta"
        subtitle="party_scorecard M-13 · snapshot ręczny · nie scoring osoby · nie RFQ"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 lg:grid-cols-4"
        onSubmit={(event) => {
          event.preventDefault()
          if (sessionReady) saveMutation.mutate()
        }}
      >
        <Input
          aria-label="Identyfikator kontrahenta karty"
          placeholder="party_id"
          value={draft.partyId}
          onChange={(event) => setDraft({ ...draft, partyId: event.target.value })}
          required
        />
        <Input
          aria-label="Wskaźnik odpowiedzi"
          placeholder="0–1"
          value={draft.responseRate}
          onChange={(event) => setDraft({ ...draft, responseRate: event.target.value })}
        />
        <Input
          aria-label="Mediana godzin odpowiedzi"
          placeholder="godziny"
          value={draft.medianHours}
          onChange={(event) => setDraft({ ...draft, medianHours: event.target.value })}
        />
        <Input
          aria-label="Pozycja cenowa"
          placeholder="0–1"
          value={draft.pricePosition}
          onChange={(event) => setDraft({ ...draft, pricePosition: event.target.value })}
        />
        <Input
          aria-label="Zgodność oferty z fakturą"
          placeholder="0–1"
          value={draft.quoteInvoiceMatch}
          onChange={(event) => setDraft({ ...draft, quoteInvoiceMatch: event.target.value })}
        />
        <Input
          aria-label="Liczba rollover"
          placeholder="rollover"
          value={draft.rolloverCount}
          onChange={(event) => setDraft({ ...draft, rolloverCount: event.target.value })}
        />
        <Input
          aria-label="Wielkość próby"
          placeholder="sample_size"
          value={draft.sampleSize}
          onChange={(event) => setDraft({ ...draft, sampleSize: event.target.value })}
          required
        />
        <Input
          aria-label="Okno dni"
          placeholder="window_days"
          value={draft.windowDays}
          onChange={(event) => setDraft({ ...draft, windowDays: event.target.value })}
          required
        />
        <Button type="submit" disabled={saveMutation.isPending || !sessionReady}>
          Zapisz snapshot
        </Button>
      </form>
      {saveMutation.isError ? <CatalogError error={saveMutation.error} /> : null}
      <CatalogLoadedTable
        tableKey={BUSINESS_LISTS.partyScorecards.tableKey}
        columns={columns}
        columnLabels={COLUMN_LABELS}
        data={query.data}
        loading={query.isLoading}
        error={query.error}
        globalFilterPlaceholder="Szukaj karty…"
      />
    </div>
  )
}
