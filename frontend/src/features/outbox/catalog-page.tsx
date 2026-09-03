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
  fetchOutboxEvents,
  outboxEventCreateBody,
  recordOutboxEvent,
  type OutboxEvent,
} from "@/lib/outbox-events-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<OutboxEvent>()
const columns = [
  helper.accessor("event_kind", { header: "Zdarzenie" }),
  helper.accessor("subject_id", { header: "subject_id" }),
  helper.accessor("status", { header: "Status" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]
const COLUMN_LABELS = {
  event_kind: "Zdarzenie",
  subject_id: "subject_id",
  status: "Status",
  source_ref: "Źródło",
}

const EMPTY_DRAFT = {
  subject_id: "",
  source_ref: "outbox://inbound-message/",
}

export function OutboxCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const [draft, setDraft] = useState(EMPTY_DRAFT)
  const listKey = ["outbox-events", ctx.organizationId] as const
  const query = useQuery({
    queryKey: listKey,
    queryFn: fetchOutboxEvents,
    enabled: ready,
    retry: false,
  })
  const createMutation = useMutation({
    mutationFn: () => recordOutboxEvent(outboxEventCreateBody(draft)),
    onSuccess: () => {
      setDraft(EMPTY_DRAFT)
      void queryClient.invalidateQueries({ queryKey: listKey })
    },
  })
  return (
    <section className="space-y-4" data-outbox="board">
      <CatalogHeading title="Outbox" subtitle="Zdarzenie po zapisie wiadomości. Nie dispatch." />
      <TenantSessionNotice />
      {query.isError ? <CatalogError error={query.error} /> : null}
      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}
      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3"
        data-outbox="record"
        onSubmit={(event) => {
          event.preventDefault()
          if (ready) createMutation.mutate()
        }}
      >
        <Input
          aria-label="Identyfikator wiadomości"
          placeholder="subject_id"
          value={draft.subject_id}
          onChange={(event) => setDraft({ ...draft, subject_id: event.target.value })}
          required
        />
        <Input
          aria-label="Źródło outbox"
          placeholder="outbox://inbound-message/"
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
        tableKey="outbox_events"
        columns={columns}
        columnLabels={COLUMN_LABELS}
        globalFilterPlaceholder="Filtruj zdarzenia"
      />
    </section>
  )
}
