import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  EMPTY_DECISION_DRAFT,
  createOperatorDecision,
  decideOperatorDecision,
  fetchOperatorDecisions,
  operatorDecisionCreateBody,
  type OperatorDecision,
  type OperatorDecisionDraft,
} from "@/lib/operator-decisions-api"
import { getTenantContext } from "@/lib/tenant"
import {
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"

const helper = createColumnHelper<OperatorDecision>()

function catalogColumns(onDecide: (id: string, status: "accepted" | "rejected") => void) {
  return [
    helper.accessor("subject_kind", { header: "Rodzaj" }),
    helper.accessor("subject_id", {
      header: "Subject",
      cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
    }),
    helper.accessor("status", { header: "Status" }),
    helper.accessor("source_ref", { header: "Źródło" }),
    helper.display({
      id: "decide",
      header: "Werdykt",
      cell: (info) => <DecideCell row={info.row.original} onDecide={onDecide} />,
    }),
  ]
}

function DecideCell({
  row,
  onDecide,
}: {
  row: OperatorDecision
  onDecide: (id: string, status: "accepted" | "rejected") => void
}) {
  if (row.status !== "pending") {
    return row.status
  }
  return (
    <span className="flex gap-1">
      <Button type="button" onClick={() => onDecide(row.id, "accepted")}>
        Akceptuj
      </Button>
      <Button type="button" onClick={() => onDecide(row.id, "rejected")}>
        Odrzuć
      </Button>
    </span>
  )
}

const COLUMN_LABELS = {
  subject_kind: "Rodzaj",
  subject_id: "Subject",
  status: "Status",
  source_ref: "Źródło",
  decide: "Werdykt",
}

function DecisionCreateForm({
  draft,
  onDraft,
  pending,
  sessionReady,
  onSubmit,
}: {
  draft: OperatorDecisionDraft
  onDraft: (next: OperatorDecisionDraft) => void
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
        aria-label="Identyfikator wiadomości"
        placeholder="subject_id UUID"
        value={draft.subjectId}
        onChange={(event) => onDraft({ ...draft, subjectId: event.target.value })}
        required
      />
      <Input
        aria-label="Źródło decyzji"
        placeholder="fixture://operator-decision/1"
        value={draft.sourceRef}
        onChange={(event) => onDraft({ ...draft, sourceRef: event.target.value })}
        required
      />
      <Button type="submit" disabled={pending || !sessionReady}>
        Utwórz pending
      </Button>
    </form>
  )
}

function useDecisionBoard() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_DECISION_DRAFT)
  const sessionReady = Boolean(ctx.organizationId && ctx.userId)
  const listKey = ["operator-decisions", ctx.organizationId] as const
  const query = useQuery({
    queryKey: listKey,
    queryFn: fetchOperatorDecisions,
    enabled: sessionReady,
    retry: false,
  })
  const createMutation = useMutation({
    mutationFn: () => createOperatorDecision(operatorDecisionCreateBody(draft)),
    onSuccess: () => {
      setDraft(EMPTY_DECISION_DRAFT)
      void queryClient.invalidateQueries({ queryKey: listKey })
    },
  })
  const decideMutation = useMutation({
    mutationFn: ({ id, status }: { id: string; status: "accepted" | "rejected" }) =>
      decideOperatorDecision(id, status),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: listKey })
    },
  })
  return { draft, setDraft, sessionReady, query, createMutation, decideMutation }
}

export function OperatorDecisionCatalogPage() {
  const board = useDecisionBoard()
  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Szyna decyzji operatora"
        subtitle="operator_decision M-71 · pending → Akceptuj / Odrzuć · nie extract HITL"
      />
      {board.sessionReady ? null : <TenantSessionNotice />}
      <DecisionCreateForm
        draft={board.draft}
        onDraft={board.setDraft}
        pending={board.createMutation.isPending}
        sessionReady={board.sessionReady}
        onSubmit={() => board.createMutation.mutate()}
      />
      {board.createMutation.isError ? <CatalogError error={board.createMutation.error} /> : null}
      {board.decideMutation.isError ? <CatalogError error={board.decideMutation.error} /> : null}
      <CatalogLoadedTable
        tableKey={BUSINESS_LISTS.operatorDecisions.tableKey}
        columns={catalogColumns((id, status) =>
          board.decideMutation.mutate({ id, status }),
        )}
        columnLabels={COLUMN_LABELS}
        data={board.query.data}
        loading={board.query.isLoading}
        error={board.query.error}
        globalFilterPlaceholder="Szukaj decyzji…"
      />
    </div>
  )
}
