import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { Link } from "@tanstack/react-router"
import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { quotationOfferOutcomes } from "@/features/party-scorecards/offer-outcomes"
import { fetchOperatorDecisions } from "@/lib/operator-decisions-api"
import {
  EMPTY_LANE_DRAFT,
  fetchPartyLaneScorecards,
  laneScorecardUpsertBody,
  upsertPartyLaneScorecard,
  type LaneScorecardDraft,
} from "@/lib/party-lane-scorecards-api"
import {
  EMPTY_SCORECARD_DRAFT,
  fetchPartyScorecards,
  scorecardUpsertBody,
  upsertPartyScorecard,
  type PartyScorecard,
  type ScorecardDraft,
} from "@/lib/party-scorecards-api"
import { fetchOrganizationSettings, laneScorecardWindowDays } from "@/lib/organization-settings-api"
import { fetchQuotations } from "@/lib/quotations-api"
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

const EMPTY_QUOTE_FILTERS = { partyId: "", originPortId: "", destinationPortId: "" }

function outcomeLabel(status: "accepted" | "rejected"): string {
  if (status === "accepted") {
    return "Przyjęta"
  }
  return "Odrzucona"
}

function useOfferOutcomeQueries() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const quotations = useQuery({
    queryKey: ["scorecard-quotations", ctx.organizationId],
    queryFn: () => fetchQuotations(EMPTY_QUOTE_FILTERS),
    enabled: ready,
    retry: false,
  })
  const decisions = useQuery({
    queryKey: ["scorecard-decisions", ctx.organizationId],
    queryFn: fetchOperatorDecisions,
    enabled: ready,
    retry: false,
  })
  return { quotations, decisions }
}

function OfferOutcomesSection() {
  const queries = useOfferOutcomeQueries()
  const rows = quotationOfferOutcomes(queries.quotations.data, queries.decisions.data)
  return (
    <section className="rounded-md border border-border bg-card p-3" data-scorecard="offer-outcomes">
      <h2 className="mb-2 text-sm font-medium">Decyzje oferty</h2>
      <p className="mb-2 text-xs">
        Werdykt S11 zostaje na{" "}
        <Link className="underline" to="/decisions">
          /decisions
        </Link>
        . Wycena na{" "}
        <Link className="underline" to="/quotations">
          /quotations
        </Link>
        . Karta nie zapisuje wskaźnika.
      </p>
      {queries.quotations.isError ? <CatalogError error={queries.quotations.error} /> : null}
      {queries.decisions.isError ? <CatalogError error={queries.decisions.error} /> : null}
      <ul className="list-disc pl-5 text-xs">
        {rows.map((row) => (
          <li key={`${row.quotationId}-${row.status}`}>
            {row.partyId} · {outcomeLabel(row.status)} · {row.quotationId} · {row.sourceRef}
          </li>
        ))}
      </ul>
    </section>
  )
}

function SnapshotFields(args: {
  draft: ScorecardDraft
  onDraft: (next: ScorecardDraft) => void
}) {
  return (
    <>
      <Input
        aria-label="Identyfikator kontrahenta karty"
        placeholder="party_id"
        value={args.draft.partyId}
        onChange={(event) => args.onDraft({ ...args.draft, partyId: event.target.value })}
        required
      />
      <Input
        aria-label="Wskaźnik odpowiedzi"
        placeholder="0–1"
        value={args.draft.responseRate}
        onChange={(event) => args.onDraft({ ...args.draft, responseRate: event.target.value })}
      />
      <Input
        aria-label="Mediana godzin odpowiedzi"
        placeholder="godziny"
        value={args.draft.medianHours}
        onChange={(event) => args.onDraft({ ...args.draft, medianHours: event.target.value })}
      />
      <Input
        aria-label="Pozycja cenowa"
        placeholder="0–1"
        value={args.draft.pricePosition}
        onChange={(event) => args.onDraft({ ...args.draft, pricePosition: event.target.value })}
      />
      <Input
        aria-label="Zgodność oferty z fakturą"
        placeholder="0–1"
        value={args.draft.quoteInvoiceMatch}
        onChange={(event) => args.onDraft({ ...args.draft, quoteInvoiceMatch: event.target.value })}
      />
      <Input
        aria-label="Liczba rollover"
        placeholder="rollover"
        value={args.draft.rolloverCount}
        onChange={(event) => args.onDraft({ ...args.draft, rolloverCount: event.target.value })}
      />
      <Input
        aria-label="Wielkość próby"
        placeholder="sample_size"
        value={args.draft.sampleSize}
        onChange={(event) => args.onDraft({ ...args.draft, sampleSize: event.target.value })}
        required
      />
      <Input
        aria-label="Okno dni"
        placeholder="window_days"
        value={args.draft.windowDays}
        onChange={(event) => args.onDraft({ ...args.draft, windowDays: event.target.value })}
        required
      />
    </>
  )
}

function LaneFields(args: {
  draft: LaneScorecardDraft
  onDraft: (next: LaneScorecardDraft) => void
}) {
  return (
    <>
      <Input
        aria-label="Kontrahent karty lane"
        placeholder="party_id"
        value={args.draft.partyId}
        onChange={(event) => args.onDraft({ ...args.draft, partyId: event.target.value })}
        required
      />
      <Input
        aria-label="POL karty lane"
        placeholder="origin_port_id"
        value={args.draft.originPortId}
        onChange={(event) => args.onDraft({ ...args.draft, originPortId: event.target.value })}
        required
      />
      <Input
        aria-label="POD karty lane"
        placeholder="destination_port_id"
        value={args.draft.destinationPortId}
        onChange={(event) => args.onDraft({ ...args.draft, destinationPortId: event.target.value })}
        required
      />
      <Input
        aria-label="Okno dni karty lane"
        placeholder="lane_scorecard_window_days"
        value={args.draft.windowDays}
        onChange={(event) => args.onDraft({ ...args.draft, windowDays: event.target.value })}
        required
      />
      <Input
        aria-label="Próba karty lane"
        placeholder="sample_size"
        value={args.draft.sampleSize}
        onChange={(event) => args.onDraft({ ...args.draft, sampleSize: event.target.value })}
        required
      />
      <Input
        aria-label="Odpowiedzi na zapytania"
        placeholder="answered_inquiry_count"
        value={args.draft.answeredInquiryCount}
        onChange={(event) =>
          args.onDraft({ ...args.draft, answeredInquiryCount: event.target.value })
        }
      />
      <Input
        aria-label="Liczba zleceń na lane"
        placeholder="shipment_count"
        value={args.draft.shipmentCount}
        onChange={(event) => args.onDraft({ ...args.draft, shipmentCount: event.target.value })}
      />
      <Input
        aria-label="Ile razy najtańszy"
        placeholder="cheapest_count"
        value={args.draft.cheapestCount}
        onChange={(event) => args.onDraft({ ...args.draft, cheapestCount: event.target.value })}
      />
      <Input
        aria-label="Mediana godzin odpowiedzi lane"
        placeholder="median_response_hours"
        value={args.draft.medianHours}
        onChange={(event) => args.onDraft({ ...args.draft, medianHours: event.target.value })}
      />
    </>
  )
}

export function PartyScorecardCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_SCORECARD_DRAFT)
  const [laneDraft, setLaneDraft] = useState(EMPTY_LANE_DRAFT)
  const sessionReady = Boolean(ctx.organizationId && ctx.userId)

  const query = useQuery({
    queryKey: ["party-scorecards", ctx.organizationId],
    queryFn: fetchPartyScorecards,
    enabled: sessionReady,
    retry: false,
  })
  const settings = useQuery({
    queryKey: ["organization-settings", ctx.organizationId],
    queryFn: fetchOrganizationSettings,
    enabled: sessionReady,
    retry: false,
  })
  const lanes = useQuery({
    queryKey: ["party-lane-scorecards", ctx.organizationId],
    queryFn: fetchPartyLaneScorecards,
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
  const saveLane = useMutation({
    mutationFn: () => upsertPartyLaneScorecard(laneScorecardUpsertBody(laneDraft)),
    onSuccess: () => {
      const windowDays = String(laneScorecardWindowDays(settings.data ?? []))
      setLaneDraft({ ...EMPTY_LANE_DRAFT, windowDays })
      void queryClient.invalidateQueries({ queryKey: ["party-lane-scorecards", ctx.organizationId] })
    },
  })

  useEffect(() => {
    if (settings.data === undefined) {
      return
    }
    setLaneDraft((current) =>
      current.partyId === ""
        ? { ...current, windowDays: String(laneScorecardWindowDays(settings.data ?? [])) }
        : current,
    )
  }, [settings.data])

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Karty wyników kontrahenta"
        subtitle="party_scorecard M-13 · snapshot ręczny · nie scoring osoby · nie RFQ"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      <OfferOutcomesSection />
      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 lg:grid-cols-4"
        onSubmit={(event) => {
          event.preventDefault()
          if (sessionReady) saveMutation.mutate()
        }}
      >
        <SnapshotFields draft={draft} onDraft={setDraft} />
        <Button type="submit" disabled={saveMutation.isPending || !sessionReady}>
          Zapisz snapshot
        </Button>
      </form>
      {saveMutation.isError ? <CatalogError error={saveMutation.error} /> : null}
      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 lg:grid-cols-4"
        data-scorecard="lane"
        onSubmit={(event) => {
          event.preventDefault()
          if (sessionReady) saveLane.mutate()
        }}
      >
        <p className="text-xs text-muted-foreground lg:col-span-4">
          Karta lane: snapshot per POL/POD. `sample_size=0` zapisuje wiersz i tekst o braku historii.
          Nie scoring osoby.
        </p>
        <LaneFields draft={laneDraft} onDraft={setLaneDraft} />
        <Button type="submit" disabled={saveLane.isPending || !sessionReady}>
          Zapisz kartę lane
        </Button>
      </form>
      {saveLane.isError ? <CatalogError error={saveLane.error} /> : null}
      {lanes.isError ? <CatalogError error={lanes.error} /> : null}
      <ul className="text-xs" data-scorecard="lane-hints">
        {(lanes.data ?? []).map((row) => (
          <li key={row.id}>
            {row.hint} · {row.party_id}
          </li>
        ))}
      </ul>
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
