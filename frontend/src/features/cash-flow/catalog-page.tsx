import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { fetchCashFlows, recordCashFlow } from "@/lib/cash-flows-api"
import { getTenantContext } from "@/lib/tenant"

type FlowDraft = {
  quoteId: string
  paymentId: string
  sourceRef: string
}

const FRESH: FlowDraft = {
  quoteId: "",
  paymentId: "",
  sourceRef: "fixture://cash-flow/",
}

function QuotePaymentGrid(args: { draft: FlowDraft; patch: (next: FlowDraft) => void }) {
  const draft = args.draft
  return (
    <div className="grid grid-cols-2 gap-2">
      <Input
        name="quotation_id"
        placeholder="quotation_id"
        value={draft.quoteId}
        onChange={(event) => args.patch({ ...draft, quoteId: event.target.value })}
        required
      />
      <Input
        name="bank_payment_id"
        placeholder="bank_payment_id"
        value={draft.paymentId}
        onChange={(event) => args.patch({ ...draft, paymentId: event.target.value })}
        required
      />
      <Input
        name="source_ref"
        placeholder="source_ref"
        className="col-span-2"
        value={draft.sourceRef}
        onChange={(event) => args.patch({ ...draft, sourceRef: event.target.value })}
        required
      />
    </div>
  )
}

function FlowSaveStrip(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [draft, setDraft] = useState(FRESH)
  const save = useMutation({
    mutationFn: () =>
      recordCashFlow({
        quotation_id: draft.quoteId.trim(),
        bank_payment_id: draft.paymentId.trim(),
        source_ref: draft.sourceRef.trim(),
      }),
    onSuccess: () => {
      setDraft({ ...FRESH })
      void client.invalidateQueries({ queryKey: ["cash-flows", args.organizationId] })
    },
  })
  return (
    <form
      className="w-full space-y-2"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <QuotePaymentGrid draft={draft} patch={setDraft} />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz przepływ
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function CashFlowPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const rows = useQuery({
    queryKey: ["cash-flows", ctx.organizationId],
    queryFn: fetchCashFlows,
    enabled: ready,
    retry: false,
  })

  return (
    <section className="flex flex-col gap-3" data-cash-flow="board">
      <CatalogHeading
        title="Przepływy"
        subtitle="cash_flow M-45 · para wycena+płatność · nie księga kwot · nie odejmowanie"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      <FlowSaveStrip organizationId={ctx.organizationId} />
      <ul className="text-xs">
        {(rows.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.quotation_id} · {row.bank_payment_id} · {row.source_ref}{" "}
            <Link className="underline" to="/quotations">
              wycena
            </Link>{" "}
            <Link className="underline" to="/payments">
              płatność
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
