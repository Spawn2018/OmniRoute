import { Link } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  createQuoteInvoiceSettlement,
  fetchQuoteInvoiceSettlements,
} from "@/lib/quote-invoice-settlements-api"
import { getTenantContext } from "@/lib/tenant"

type Draft = { quotationId: string; invoiceId: string; sourceRef: string }

const EMPTY: Draft = {
  quotationId: "",
  invoiceId: "",
  sourceRef: "fixture://quote-invoice-settlement/",
}

function SettlementIds(args: { draft: Draft; onDraft: (next: Draft) => void }) {
  const draft = args.draft
  return (
    <div className="grid gap-3">
      <Input
        name="quotation_id"
        placeholder="quotation_id"
        value={draft.quotationId}
        onChange={(event) => args.onDraft({ ...draft, quotationId: event.target.value })}
        required
      />
      <Input
        name="sales_invoice_id"
        placeholder="sales_invoice_id"
        value={draft.invoiceId}
        onChange={(event) => args.onDraft({ ...draft, invoiceId: event.target.value })}
        required
      />
      <Input
        name="source_ref"
        placeholder="source_ref"
        value={draft.sourceRef}
        onChange={(event) => args.onDraft({ ...draft, sourceRef: event.target.value })}
        required
      />
    </div>
  )
}

function SettlementRecordForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [draft, setDraft] = useState(EMPTY)
  const save = useMutation({
    mutationFn: () =>
      createQuoteInvoiceSettlement({
        quotation_id: draft.quotationId.trim(),
        sales_invoice_id: draft.invoiceId.trim(),
        source_ref: draft.sourceRef.trim(),
      }),
    onSuccess: () => {
      setDraft({ ...EMPTY })
      void client.invalidateQueries({ queryKey: ["quote-invoice-settlements", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-xl flex-col gap-3 rounded-md border border-border p-3"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <SettlementIds draft={draft} onDraft={setDraft} />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz rozliczenie
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function QuoteInvoiceSettlementPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const rows = useQuery({
    queryKey: ["quote-invoice-settlements", ctx.organizationId],
    queryFn: fetchQuoteInvoiceSettlements,
    enabled: ready,
    retry: false,
  })

  return (
    <section className="flex flex-col gap-3" data-quote-invoice-settlement="board">
      <CatalogHeading
        title="Rozliczenie wyceny"
        subtitle="quote_invoice_settlement M-41 · para wycena+faktura · nie druga marża"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      <SettlementRecordForm organizationId={ctx.organizationId} />
      {(rows.data ?? []).map((row) => (
        <p key={row.id} className="font-mono text-xs">
          {row.quotation_id} · {row.sales_invoice_id} · {row.source_ref}{" "}
          <Link className="underline" to="/quotations">wycena</Link>{" "}
          <Link className="underline" to="/invoices">faktura</Link>
        </p>
      ))}
    </section>
  )
}
