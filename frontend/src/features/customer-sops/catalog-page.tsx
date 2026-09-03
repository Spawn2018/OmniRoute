import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  EMPTY_SOP_DRAFT,
  approveCustomerSop,
  createCustomerSop,
  customerSopCreateBody,
  fetchCustomerSops,
  type CustomerSop,
} from "@/lib/customer-sops-api"
import { getTenantContext } from "@/lib/tenant"
import {
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"

const helper = createColumnHelper<CustomerSop>()

function catalogColumns(onApprove: (id: string) => void) {
  return [
    helper.accessor("party_id", {
      header: "Kontrahent",
      cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
    }),
    helper.accessor("code", {
      header: "Kod",
      cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
    }),
    helper.accessor("title", { header: "Tytuł" }),
    helper.accessor("status", { header: "Status" }),
    helper.accessor("blocks_auto", {
      header: "Blokuj auto",
      cell: (info) => (info.getValue() ? "tak" : "nie"),
    }),
    helper.accessor("source_ref", { header: "Źródło" }),
    helper.display({
      id: "approve",
      header: "Zatwierdzenie",
      cell: (info) =>
        info.row.original.status === "draft" ? (
          <Button type="button" onClick={() => onApprove(info.row.original.id)}>
            Zatwierdź
          </Button>
        ) : (
          "zatwierdzona"
        ),
    }),
  ]
}

const COLUMN_LABELS = {
  party_id: "Kontrahent",
  code: "Kod",
  title: "Tytuł",
  status: "Status",
  blocks_auto: "Blokuj auto",
  source_ref: "Źródło",
  approve: "Zatwierdzenie",
}

export function CustomerSopCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_SOP_DRAFT)
  const sessionReady = Boolean(ctx.organizationId && ctx.userId)

  const query = useQuery({
    queryKey: ["customer-sops", ctx.organizationId],
    queryFn: fetchCustomerSops,
    enabled: sessionReady,
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () => createCustomerSop(customerSopCreateBody(draft)),
    onSuccess: () => {
      setDraft(EMPTY_SOP_DRAFT)
      void queryClient.invalidateQueries({ queryKey: ["customer-sops", ctx.organizationId] })
    },
  })

  const approveMutation = useMutation({
    mutationFn: (sopId: string) => approveCustomerSop(sopId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["customer-sops", ctx.organizationId] })
    },
  })

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Procedury operacyjne klienta"
        subtitle="customer_sop M-16 · katalog ręczny · nie generator zadań · nie treść z LLM"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 lg:grid-cols-2"
        onSubmit={(event) => {
          event.preventDefault()
          if (sessionReady) createMutation.mutate()
        }}
      >
        <Input
          aria-label="Identyfikator kontrahenta procedury"
          placeholder="party_id"
          value={draft.partyId}
          onChange={(event) => setDraft({ ...draft, partyId: event.target.value })}
          required
        />
        <Input
          aria-label="Kod procedury"
          placeholder="pre_alert"
          value={draft.code}
          onChange={(event) => setDraft({ ...draft, code: event.target.value })}
          required
        />
        <Input
          aria-label="Tytuł procedury"
          placeholder="tytuł"
          value={draft.title}
          onChange={(event) => setDraft({ ...draft, title: event.target.value })}
          required
        />
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={draft.blocksAuto}
            onChange={(event) => setDraft({ ...draft, blocksAuto: event.target.checked })}
          />
          Blokuj auto
        </label>
        <textarea
          aria-label="Treść procedury"
          placeholder="treść operacyjna"
          className="min-h-24 w-full rounded-md border border-input bg-card px-3 py-1.5 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          value={draft.body}
          onChange={(event) => setDraft({ ...draft, body: event.target.value })}
          required
        />
        <Button type="submit" disabled={createMutation.isPending || !sessionReady}>
          Dodaj szkic
        </Button>
      </form>
      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}
      {approveMutation.isError ? <CatalogError error={approveMutation.error} /> : null}
      <CatalogLoadedTable
        tableKey={BUSINESS_LISTS.customerSops.tableKey}
        columns={catalogColumns((sopId) => approveMutation.mutate(sopId))}
        columnLabels={COLUMN_LABELS}
        data={query.data}
        loading={query.isLoading}
        error={query.error}
        globalFilterPlaceholder="Szukaj procedury…"
      />
    </div>
  )
}
