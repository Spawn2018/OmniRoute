import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { fetchExtractionDrafts } from "@/lib/extractions-api"
import {
  EMPTY_NOTICE_DRAFT,
  createOperatorNotice,
  fetchOperatorNotices,
  operatorNoticeCreateBody,
  readOperatorNotice,
  type NoticeDraft,
  type StoredOperatorNotice,
} from "@/lib/operator-notices-api"
import { operatorNotices } from "@/lib/operator-notices"
import { fetchQuotations } from "@/lib/quotations-api"
import { getTenantContext } from "@/lib/tenant"

const EMPTY_QUOTE_FILTERS = { partyId: "", originPortId: "", destinationPortId: "" }

function PendingWorkBoard() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const drafts = useQuery({
    queryKey: ["notice-drafts", ctx.organizationId],
    queryFn: () => fetchExtractionDrafts("pending"),
    enabled: ready,
    retry: false,
  })
  const quotations = useQuery({
    queryKey: ["notice-quotations", ctx.organizationId],
    queryFn: () => fetchQuotations(EMPTY_QUOTE_FILTERS),
    enabled: ready,
    retry: false,
  })
  const notices = operatorNotices(drafts.data ?? [], quotations.data ?? [])
  const hasAiDraft = notices.some((row) => row.kind === "extraction_draft")
  return (
    <div data-operator-notice="board">
      {drafts.isError ? <CatalogError error={drafts.error} /> : null}
      {quotations.isError ? <CatalogError error={quotations.error} /> : null}
      {hasAiDraft ? (
        <p className="text-xs text-muted-foreground">system AI · recenzja człowieka (Art. 50)</p>
      ) : null}
      {notices.map((row) => (
        <p key={`${row.kind}:${row.id}`} className="text-xs">
          <Link className="underline" to={row.href}>
            {row.kind} {row.label}
          </Link>
          {row.amount !== null && row.currency !== null ? (
            <>
              {" "}
              <Money amount={row.amount} currency={row.currency} />
            </>
          ) : null}
        </p>
      ))}
    </div>
  )
}

function NoticeCreateForm({
  draft,
  onDraft,
  pending,
  sessionReady,
  onSubmit,
}: {
  draft: NoticeDraft
  onDraft: (next: NoticeDraft) => void
  pending: boolean
  sessionReady: boolean
  onSubmit: () => void
}) {
  return (
    <form
      className="grid gap-2 rounded-md border border-border bg-card p-3 lg:grid-cols-3"
      onSubmit={(event) => {
        event.preventDefault()
        if (sessionReady) onSubmit()
      }}
    >
      <Input
        aria-label="Treść powiadomienia"
        placeholder="treść"
        value={draft.body}
        onChange={(event) => onDraft({ ...draft, body: event.target.value })}
        required
      />
      <Input
        aria-label="Źródło powiadomienia"
        placeholder="fixture://operator-notice/1"
        value={draft.sourceRef}
        onChange={(event) => onDraft({ ...draft, sourceRef: event.target.value })}
        required
      />
      <Button type="submit" disabled={pending || !sessionReady}>
        Zapisz unread
      </Button>
    </form>
  )
}

function StoredNoticeList({
  rows,
  onRead,
}: {
  rows: StoredOperatorNotice[]
  onRead: (id: string) => void
}) {
  return (
    <ul className="space-y-1">
      {rows.map((row) => (
        <li key={row.id} className="flex items-center gap-2 text-xs">
          <span className="font-mono">{row.status}</span>
          <span>{row.body}</span>
          {row.status === "unread" ? (
            <Button type="button" onClick={() => onRead(row.id)}>
              Oznacz przeczytane
            </Button>
          ) : (
            "przeczytane"
          )}
        </li>
      ))}
    </ul>
  )
}

function useStoredInbox() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_NOTICE_DRAFT)
  const sessionReady = Boolean(ctx.organizationId && ctx.userId)
  const listKey = ["operator-notices", ctx.organizationId] as const
  const query = useQuery({
    queryKey: listKey,
    queryFn: fetchOperatorNotices,
    enabled: sessionReady,
    retry: false,
  })
  const createMutation = useMutation({
    mutationFn: () => createOperatorNotice(operatorNoticeCreateBody(draft)),
    onSuccess: () => {
      setDraft(EMPTY_NOTICE_DRAFT)
      void queryClient.invalidateQueries({ queryKey: listKey })
    },
  })
  const readMutation = useMutation({
    mutationFn: readOperatorNotice,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: listKey })
    },
  })
  return { draft, setDraft, sessionReady, query, createMutation, readMutation }
}

export function OperatorNoticePage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const inbox = useStoredInbox()
  return (
    <div className="flex flex-col gap-4">
      <CatalogHeading
        title="Powiadomienia"
        subtitle="operator_notice M-34 · tabela inbox + tablica pending · nie wysyłka"
      />
      {!ready ? <TenantSessionNotice /> : null}
      <NoticeCreateForm
        draft={inbox.draft}
        onDraft={inbox.setDraft}
        pending={inbox.createMutation.isPending}
        sessionReady={inbox.sessionReady}
        onSubmit={() => inbox.createMutation.mutate()}
      />
      {inbox.createMutation.isError ? <CatalogError error={inbox.createMutation.error} /> : null}
      {inbox.readMutation.isError ? <CatalogError error={inbox.readMutation.error} /> : null}
      <StoredNoticeList
        rows={inbox.query.data ?? []}
        onRead={(id) => inbox.readMutation.mutate(id)}
      />
      <PendingWorkBoard />
    </div>
  )
}
