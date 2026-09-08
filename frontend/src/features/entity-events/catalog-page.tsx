import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  entityEventCreateBody,
  fetchEntityEvents,
  recordEntityEvent,
  type EntityEvent,
} from "@/lib/entity-events-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<EntityEvent>()
const columns = [
  helper.accessor("event_kind", { header: "Zdarzenie" }),
  helper.accessor("subject_kind", { header: "Podmiot" }),
  helper.accessor("subject_id", { header: "subject_id" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]
const COLUMN_LABELS = {
  event_kind: "Zdarzenie",
  subject_kind: "Podmiot",
  subject_id: "subject_id",
  source_ref: "Źródło",
}

const EMPTY_DRAFT = {
  subject_kind: "carrier_inquiry",
  subject_id: "",
  event_kind: "inquiry_queued",
  source_ref: "entity://inquiry/",
}

export function EntityEventCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const [draft, setDraft] = useState(EMPTY_DRAFT)
  const listKey = ["entity-events", ctx.organizationId] as const
  const query = useQuery({
    queryKey: listKey,
    queryFn: fetchEntityEvents,
    enabled: ready,
    retry: false,
  })
  const createMutation = useMutation({
    mutationFn: () => recordEntityEvent(entityEventCreateBody(draft)),
    onSuccess: () => {
      setDraft(EMPTY_DRAFT)
      void queryClient.invalidateQueries({ queryKey: listKey })
    },
  })
  return (
    <section className="space-y-4" data-entity-event="board">
      <CatalogHeading
        title="Zdarzenia podmiotu"
        subtitle="Dziennik inquiry / oferty. Nie outbox. Nie predykcja."
      />
      <TenantSessionNotice />
      {query.isError ? <CatalogError error={query.error} /> : null}
      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}
      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3"
        data-entity-event="record"
        onSubmit={(event) => {
          event.preventDefault()
          if (ready) createMutation.mutate()
        }}
      >
        <Input
          aria-label="Rodzaj podmiotu"
          placeholder="subject_kind"
          value={draft.subject_kind}
          onChange={(event) => setDraft({ ...draft, subject_kind: event.target.value })}
          required
        />
        <Input
          aria-label="Identyfikator podmiotu"
          placeholder="subject_id"
          value={draft.subject_id}
          onChange={(event) => setDraft({ ...draft, subject_id: event.target.value })}
          required
        />
        <Input
          aria-label="Rodzaj zdarzenia"
          placeholder="event_kind"
          value={draft.event_kind}
          onChange={(event) => setDraft({ ...draft, event_kind: event.target.value })}
          required
        />
        <Input
          aria-label="Źródło zdarzenia"
          placeholder="entity://inquiry/"
          value={draft.source_ref}
          onChange={(event) => setDraft({ ...draft, source_ref: event.target.value })}
          required
        />
        <Button type="submit" disabled={!ready || createMutation.isPending}>
          Zapisz zdarzenie
        </Button>
      </form>
      <CatalogLoadedTable
        loading={query.isLoading}
        error={query.error}
        data={query.data}
        tableKey="entity_events"
        columns={columns}
        columnLabels={COLUMN_LABELS}
        globalFilterPlaceholder="Filtruj zdarzenia"
      />
    </section>
  )
}
