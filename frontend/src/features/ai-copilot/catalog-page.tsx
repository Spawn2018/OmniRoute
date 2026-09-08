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
import { fetchCustomerSops, type CustomerSop } from "@/lib/customer-sops-api"
import { aiProposals, fetchExtractionDrafts } from "@/lib/extractions-api"
import {
  EMPTY_MAIL_DRAFT,
  createMailDraft,
  dispatchMailtoMailDraft,
  fetchMailDrafts,
  mailDraftCreateBody,
  mailDraftDecisionBody,
  type MailDraftDispatch,
  type MailDraftForm,
  type StoredMailDraft,
} from "@/lib/mail-drafts-api"
import { createOperatorDecision } from "@/lib/operator-decisions-api"
import { getTenantContext } from "@/lib/tenant"

function sopAutoLabel(blocksAuto: boolean): string {
  if (blocksAuto) {
    return "blokuje auto"
  }
  return "auto nieblokowane"
}

function SopAutoFacts() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const sops = useQuery({
    queryKey: ["customer-sops", ctx.organizationId],
    queryFn: fetchCustomerSops,
    enabled: ready,
    retry: false,
  })
  return (
    <section className="rounded-md border border-border bg-card p-3" data-ai-copilot="sop">
      <h2 className="mb-2 text-sm font-medium">SOP przy szkicu</h2>
      <p className="mb-2 text-xs">
        Zapis procedury zostaje na{" "}
        <Link className="underline" to="/customer-sops">
          /customer-sops
        </Link>
        . Flaga nie wysyła maila sama.
      </p>
      {sops.isError ? <CatalogError error={sops.error} /> : null}
      <ol className="list-decimal pl-5 text-xs">
        {(sops.data ?? []).map((row: CustomerSop) => (
          <li key={row.id}>
            {row.code} · {row.status} · {sopAutoLabel(row.blocks_auto)}
          </li>
        ))}
      </ol>
    </section>
  )
}

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
            {row.source_ref} {row.status} {row.draft_kind}{" "}
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
  onDispatch,
  dispatchHref,
  toAddress,
  onToAddress,
}: {
  rows: StoredMailDraft[]
  onSubmitDecision: (id: string) => void
  onDispatch: (id: string) => void
  dispatchHref: string
  toAddress: string
  onToAddress: (value: string) => void
}) {
  return (
    <ul className="space-y-1">
      {rows.map((row) => (
        <li key={row.id} className="flex flex-wrap items-center gap-2 text-xs">
          <span className="font-mono">{row.status}</span>
          <span>{row.body}</span>
          <Button type="button" onClick={() => onSubmitDecision(row.id)}>
            Zgłoś do decyzji
          </Button>
          <form
            className="flex flex-wrap items-center gap-2"
            data-mail-client="dispatch-mailto"
            onSubmit={(event) => {
              event.preventDefault()
              onDispatch(row.id)
            }}
          >
            <Input
              aria-label={`Adres wysyłki ${row.id}`}
              placeholder="ops@carrier.example"
              value={toAddress}
              onChange={(event) => onToAddress(event.target.value)}
              required
            />
            <Button type="submit">Wyślij w kliencie</Button>
          </form>
        </li>
      ))}
      {dispatchHref === "" ? null : (
        <li>
          <a className="underline" href={dispatchHref}>
            Otwórz klienta
          </a>
        </li>
      )}
    </ul>
  )
}

function useMailDraftInbox() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_MAIL_DRAFT)
  const [toAddress, setToAddress] = useState("")
  const [dispatchHref, setDispatchHref] = useState("")
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
  const dispatchMutation = useMutation({
    mutationFn: (id: string) => dispatchMailtoMailDraft(id, toAddress),
    onSuccess: (sent: MailDraftDispatch) => {
      setDispatchHref(sent.mailto)
      void queryClient.invalidateQueries({ queryKey: listKey })
    },
  })
  return {
    draft,
    setDraft,
    toAddress,
    setToAddress,
    dispatchHref,
    sessionReady,
    query,
    createMutation,
    decideMutation,
    dispatchMutation,
  }
}

export function AiCopilotPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const inbox = useMailDraftInbox()
  return (
    <section className="flex flex-col gap-4" data-ai-copilot="board">
      <CatalogHeading
        title="Propozycje AI"
        subtitle="ai_copilot M-57 · mail_draft obok extract i SOP · Art. 50 · nie czat · nie auto-send"
      />
      {!ready ? <TenantSessionNotice /> : null}
      <PendingAiBoard />
      <SopAutoFacts />
      <MailDraftCreateForm
        draft={inbox.draft}
        onDraft={inbox.setDraft}
        pending={inbox.createMutation.isPending}
        sessionReady={inbox.sessionReady}
        onSubmit={() => inbox.createMutation.mutate()}
      />
      {inbox.createMutation.isError ? <CatalogError error={inbox.createMutation.error} /> : null}
      {inbox.decideMutation.isError ? <CatalogError error={inbox.decideMutation.error} /> : null}
      {inbox.dispatchMutation.isError ? (
        <CatalogError error={inbox.dispatchMutation.error} />
      ) : null}
      <StoredMailDraftList
        rows={inbox.query.data ?? []}
        onSubmitDecision={(id) => inbox.decideMutation.mutate(id)}
        onDispatch={(id) => inbox.dispatchMutation.mutate(id)}
        dispatchHref={inbox.dispatchHref}
        toAddress={inbox.toAddress}
        onToAddress={inbox.setToAddress}
      />
      <p className="text-xs text-muted-foreground">
        Werdykt szkicu jest na <Link className="underline" to="/decisions">/decisions</Link>
        . HITL extract zostaje na /extractions.
      </p>
    </section>
  )
}
