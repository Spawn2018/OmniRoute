import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { lazy, Suspense, useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { fetchMailDrafts, type StoredMailDraft } from "@/lib/mail-drafts-api"
import {
  fetchOperationalExceptions,
  type OperationalException,
} from "@/lib/operational-exceptions-api"
import { DecideStatusButtons } from "@/features/operator-decisions/decide-status-buttons"
import {
  decideOperatorDecision,
  fetchOperatorDecisions,
  type OperatorDecideStatus,
  type OperatorDecision,
} from "@/lib/operator-decisions-api"
import { getTenantContext } from "@/lib/tenant"

const WatchtowerMapPanel = lazy(() => import("@/features/watchtower/map-panel"))

function pendingRows(rows: OperatorDecision[] | undefined): OperatorDecision[] {
  return (rows ?? []).filter((row) => row.status === "pending")
}

function MapGate() {
  const [open, setOpen] = useState(false)
  if (!open) {
    return (
      <Button type="button" onClick={() => setOpen(true)}>
        Otwórz panel mapy
      </Button>
    )
  }
  return (
    <Suspense fallback={<p className="text-sm">Ładuję panel mapy</p>}>
      <WatchtowerMapPanel />
    </Suspense>
  )
}

function VerdictRow(args: {
  row: OperatorDecision
  onDecide: (id: string, status: OperatorDecideStatus, lockVersion: number) => void
}) {
  return (
    <p className="flex flex-wrap items-center gap-2 text-xs">
      <span className="font-mono">{args.row.subject_kind}</span>
      <span className="font-mono">{args.row.subject_id}</span>
      <DecideStatusButtons
        acceptLabel="Akceptuj"
        onDecide={(status) => args.onDecide(args.row.id, status, args.row.lock_version)}
      />
    </p>
  )
}

function ExceptionSection(args: { rows: OperationalException[] | undefined }) {
  return (
    <section className="rounded-md border border-border bg-card p-3">
      <h2 className="mb-2 text-sm font-medium">Wyjątki</h2>
      {(args.rows ?? []).map((row) => (
        <p key={row.id} className="text-xs">
          {row.exception_kind} {row.source_ref}
        </p>
      ))}
    </section>
  )
}

function DraftSection(args: { rows: StoredMailDraft[] | undefined }) {
  return (
    <section className="rounded-md border border-border bg-card p-3" data-watchtower="drafts">
      <h2 className="mb-2 text-sm font-medium">Szkice maila</h2>
      <ol className="list-decimal pl-5 text-xs">
        {(args.rows ?? []).map((row) => (
          <li key={row.id}>
            {row.status} · {row.subject_kind} · {row.source_ref}
          </li>
        ))}
      </ol>
    </section>
  )
}

function PendingSection(args: {
  rows: OperatorDecision[] | undefined
  onDecide: (id: string, status: OperatorDecideStatus, lockVersion: number) => void
}) {
  return (
    <section className="rounded-md border border-border bg-card p-3">
      <h2 className="mb-2 text-sm font-medium">Pending S11</h2>
      {pendingRows(args.rows).map((row) => (
        <VerdictRow key={row.id} row={row} onDecide={args.onDecide} />
      ))}
    </section>
  )
}

function useWatchtowerQueries() {
  const ctx = getTenantContext()
  const client = useQueryClient()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const exceptions = useQuery({
    queryKey: ["operational-exceptions", ctx.organizationId],
    queryFn: fetchOperationalExceptions,
    enabled: ready,
    retry: false,
  })
  const decisions = useQuery({
    queryKey: ["operator-decisions", ctx.organizationId],
    queryFn: fetchOperatorDecisions,
    enabled: ready,
    retry: false,
  })
  const drafts = useQuery({
    queryKey: ["mail-drafts", ctx.organizationId],
    queryFn: fetchMailDrafts,
    enabled: ready,
    retry: false,
  })
  const decide = useMutation({
    mutationFn: (input: { id: string; status: OperatorDecideStatus; lockVersion: number }) =>
      decideOperatorDecision(input.id, input.status, input.lockVersion),
    onSuccess: () => {
      void client.invalidateQueries({ queryKey: ["operator-decisions", ctx.organizationId] })
    },
  })
  return { ready, exceptions, decisions, drafts, decide }
}

export function WatchtowerPage() {
  const queries = useWatchtowerQueries()
  return (
    <div className="flex flex-col gap-4" data-watchtower="board">
      <CatalogHeading
        title="Wieża"
        subtitle="watchtower · wyjątki, pending S11 i szkice mail_draft · leniwy panel mapy · nie czat"
      />
      {!queries.ready ? <TenantSessionNotice /> : null}
      {queries.exceptions.isError ? <CatalogError error={queries.exceptions.error} /> : null}
      {queries.decisions.isError ? <CatalogError error={queries.decisions.error} /> : null}
      {queries.drafts.isError ? <CatalogError error={queries.drafts.error} /> : null}
      {queries.decide.isError ? <CatalogError error={queries.decide.error} /> : null}
      <p className="text-sm">
        HITL extract zostaje na{" "}
        <Link className="underline" to="/ai">
          /ai
        </Link>
      </p>
      <ExceptionSection rows={queries.exceptions.data} />
      <PendingSection
        rows={queries.decisions.data}
        onDecide={(id, status, lockVersion) =>
          queries.decide.mutate({ id, status, lockVersion })
        }
      />
      <DraftSection rows={queries.drafts.data} />
      <MapGate />
    </div>
  )
}

