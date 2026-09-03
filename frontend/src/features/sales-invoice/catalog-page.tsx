import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { createSalesInvoice, fetchSalesInvoices } from "@/lib/sales-invoices-api"
import { getTenantContext } from "@/lib/tenant"

const EMPTY_DRAFT = {
  shipmentId: "",
  invoiceKind: "issued",
  invoiceRef: "",
  sourceRef: "fixture://sales-invoice/",
}

function InvoiceDraftFields(args: {
  draft: typeof EMPTY_DRAFT
  onDraft: (next: typeof EMPTY_DRAFT) => void
}) {
  const draft = args.draft
  return (
    <>
      <Input
        aria-label="Numer faktury"
        placeholder="invoice_ref"
        value={draft.invoiceRef}
        onChange={(event) => args.onDraft({ ...draft, invoiceRef: event.target.value })}
        required
      />
      <Input
        aria-label="Identyfikator zlecenia"
        placeholder="shipment_id"
        value={draft.shipmentId}
        onChange={(event) => args.onDraft({ ...draft, shipmentId: event.target.value })}
        required
      />
      <Input
        aria-label="Rodzaj faktury"
        placeholder="issued"
        value={draft.invoiceKind}
        onChange={(event) => args.onDraft({ ...draft, invoiceKind: event.target.value })}
        required
      />
      <Input
        aria-label="Pochodzenie zapisu"
        placeholder="source_ref"
        value={draft.sourceRef}
        onChange={(event) => args.onDraft({ ...draft, sourceRef: event.target.value })}
        required
      />
    </>
  )
}

function InvoiceRecordForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_DRAFT)
  const save = useMutation({
    mutationFn: () =>
      createSalesInvoice({
        shipment_id: draft.shipmentId.trim(),
        invoice_kind: draft.invoiceKind.trim(),
        invoice_ref: draft.invoiceRef.trim(),
        source_ref: draft.sourceRef.trim(),
      }),
    onSuccess: () => {
      setDraft({ ...EMPTY_DRAFT })
      void client.invalidateQueries({ queryKey: ["sales-invoices", args.organizationId] })
    },
  })
  function submitRecord(event: FormEvent) {
    event.preventDefault()
    if (args.organizationId) save.mutate()
  }
  return (
    <form className="space-y-2 rounded-lg border bg-background p-4 md:grid md:grid-cols-2" onSubmit={submitRecord}>
      <InvoiceDraftFields draft={draft} onDraft={setDraft} />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz fakturę
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function SalesInvoicePage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const invoices = useQuery({
    queryKey: ["sales-invoices", ctx.organizationId],
    queryFn: fetchSalesInvoices,
    enabled: ready,
    retry: false,
  })

  return (
    <div className="flex flex-col gap-4" data-sales-invoice="board">
      <CatalogHeading
        title="Faktury"
        subtitle="sales_invoice M-40 · tabela na zleceniu · nie KSeF · nie druga marża"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {invoices.isError ? <CatalogError error={invoices.error} /> : null}
      <InvoiceRecordForm organizationId={ctx.organizationId} />
      {(invoices.data ?? []).map((row) => (
        <p key={row.id} className="font-mono text-xs">
          {row.invoice_kind} · {row.invoice_ref} · {row.source_ref}{" "}
          <Link className="underline" to="/shipments">
            zlecenie
          </Link>{" "}
          <Link className="underline" to="/charges">
            opłaty
          </Link>{" "}
          <Link className="underline" to="/finance">
            finance
          </Link>
        </p>
      ))}
    </div>
  )
}
