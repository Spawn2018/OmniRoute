import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { aiProposals, fetchExtractionDrafts } from "@/lib/extractions-api"
import {
  EMPTY_MAIL_DRAFT,
  createMailDraft,
  fetchMailDrafts,
  mailDraftCreateBody,
  mailDraftDecisionBody,
  type MailDraftForm,
  type StoredMailDraft,
} from "@/lib/mail-drafts-api"
import { createOperatorDecision } from "@/lib/operator-decisions-api"
import { getTenantContext } from "@/lib/tenant"

function PendingAiBoard() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const drafts = useQuery({
    queryKey: ["ai-copilot-drafts", ctx.organizationId],
    queryFn: () => fetchExtractionDrafts("pending"),
    enabled: ready,
    retry: false,
  })
  const rows = aiProposals(drafts.data ?? [])
  return (
    <div>
      {drafts.isError ? <CatalogError error={drafts.error} /> : null}
      <ul>
        {rows.map((row) => (
          <li key={row.id} className="text-xs">
            {row.source_ref} {row.status}{" "}
            <Link className="underline" to="/extractions">
              HITL
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}

function patchDraft(
  draft: MailDraftForm,
  key: keyof MailDraftForm,
  value: string,
): MailDraftForm {
  return { ...draft, [key]: value }
}

function MailDraftCreateForm({
  draft,
  onDraft,
  pending,
  sessionReady,
  onSubmit,
}: {
  draft: MailDraftForm
  onDraft: (next: MailDraftForm) => void
  pending: boolean
  sessionReady: boolean
  onSubmit: () => void
}) {
  return (
    <form
      className="grid gap-2 rounded-md border border-border bg-card p-3 lg:grid-cols-4"
      onSubmit={(event) => {
        event.preventDefault()
        if (sessionReady) onSubmit()
      }}
    >
      <Input
        aria-label="UUID extractu"
        placeholder="extraction_draft id"
        value={draft.subjectId}
        onChange={(event) => onDraft(patchDraft(draft, "subjectId", event.target.value))}
        required
      />
      <Input
        aria-label="Treść szkicu maila"
        placeholder="treść"
        value={draft.body}
        onChange={(event) => onDraft(patchDraft(draft, "body", event.target.value))}
        required
      />
      <Input
        aria-label="Źródło szkicu maila"
        placeholder="fixture://mail-draft/1"
        value={draft.sourceRef}
        onChange={(event) => onDraft(patchDraft(draft, "sourceRef", event.target.value))}
        required
      />
      <Button type="submit" disabled={pending || !sessionReady}>
        Zapisz szkic
      </Button>
    </form>
  )
}

function StoredMailDraftList({
  rows,
  onSubmitDecision,
}: {
  rows: StoredMailDraft[]
  onSubmitDecision: (id: string) => void
}) {
  return (
    <ul className="space-y-1">
      {rows.map((row) => (
        <li key={row.id} className="flex items-center gap-2 text-xs">
          <span className="font-mono">{row.status}</span>
          <span>{row.body}</span>
          <Button type="button" onClick={() => onSubmitDecision(row.id)}>
            Zgłoś do decyzji
          </Button>
        </li>
      ))}
    </ul>
  )
}

function useMailDraftInbox() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_MAIL_DRAFT)
  const sessionReady = Boolean(ctx.organizationId && ctx.userId)
  const listKey = ["mail-drafts", ctx.organizationId] as const
  const query = useQuery({
    queryKey: listKey,
    queryFn: fetchMailDrafts,
    enabled: sessionReady,
    retry: false,
  })
  const createMutation = useMutation({
    mutationFn: () => createMailDraft(mailDraftCreateBody(draft)),
    onSuccess: () => {
      setDraft(EMPTY_MAIL_DRAFT)
      void queryClient.invalidateQueries({ queryKey: listKey })
    },
  })
  const decideMutation = useMutation({
    mutationFn: (id: string) => createOperatorDecision(mailDraftDecisionBody(id)),
  })
  return { draft, setDraft, sessionReady, query, createMutation, decideMutation }
}

export function AiCopilotPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const inbox = useMailDraftInbox()
  return (
    <section className="flex flex-col gap-4" data-ai-copilot="board">
      <CatalogHeading
        title="Propozycje AI"
        subtitle="ai_copilot M-57 · mail_draft obok extract · Art. 50 · nie czat · nie accept extractu"
      />
      {!ready ? <TenantSessionNotice /> : null}
      <PendingAiBoard />
      <MailDraftCreateForm
        draft={inbox.draft}
        onDraft={inbox.setDraft}
        pending={inbox.createMutation.isPending}
        sessionReady={inbox.sessionReady}
        onSubmit={() => inbox.createMutation.mutate()}
      />
      {inbox.createMutation.isError ? <CatalogError error={inbox.createMutation.error} /> : null}
      {inbox.decideMutation.isError ? <CatalogError error={inbox.decideMutation.error} /> : null}
      <StoredMailDraftList
        rows={inbox.query.data ?? []}
        onSubmitDecision={(id) => inbox.decideMutation.mutate(id)}
      />
      <p className="text-xs text-muted-foreground">
        Werdykt szkicu jest na <Link className="underline" to="/decisions">/decisions</Link>
        . HITL extract zostaje na /extractions.
      </p>
    </section>
  )
}
