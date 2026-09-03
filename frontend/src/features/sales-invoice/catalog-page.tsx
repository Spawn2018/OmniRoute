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
import { fetchCollectiveInvoices, recordCollectiveInvoice } from "@/lib/collective-invoices-api"
import { createSalesInvoice, fetchSalesInvoices, noteKsef } from "@/lib/sales-invoices-api"
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

function InvoiceKsefForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [invoiceId, setInvoiceId] = useState("")
  const [ksefRef, setKsefRef] = useState("fixture://ksef/")
  const save = useMutation({
    mutationFn: () => noteKsef(invoiceId.trim(), ksefRef.trim()),
    onSuccess: () => {
      setInvoiceId("")
      setKsefRef("fixture://ksef/")
      void client.invalidateQueries({ queryKey: ["sales-invoices", args.organizationId] })
    },
  })
  function submitNote(event: FormEvent) {
    event.preventDefault()
    if (args.organizationId) save.mutate()
  }
  return (
    <form className="flex max-w-md flex-col gap-2" onSubmit={submitNote}>
      <Input
        aria-label="Identyfikator faktury"
        placeholder="invoice_id"
        value={invoiceId}
        onChange={(event) => setInvoiceId(event.target.value)}
        required
      />
      <Input
        aria-label="Numer sesji KSeF"
        placeholder="ksef_ref"
        value={ksefRef}
        onChange={(event) => setKsefRef(event.target.value)}
        required
      />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz numer sesji
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
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

type ExtraDraft = {
  invoiceId: string
  shipmentId: string
  sourceRef: string
}

const FRESH_EXTRA: ExtraDraft = {
  invoiceId: "",
  shipmentId: "",
  sourceRef: "fixture://collective-invoice/",
}

function ExtraShipmentFields(args: { draft: ExtraDraft; patch: (next: ExtraDraft) => void }) {
  const draft = args.draft
  return (
    <div className="inline-flex flex-wrap items-baseline gap-x-3">
      <Input
        name="sales_invoice_id"
        placeholder="sales_invoice_id"
        className="w-52"
        value={draft.invoiceId}
        onChange={(event) => args.patch({ ...draft, invoiceId: event.target.value })}
        required
      />
      <Input
        name="shipment_id"
        placeholder="shipment_id dodatkowego zlecenia"
        className="w-52"
        value={draft.shipmentId}
        onChange={(event) => args.patch({ ...draft, shipmentId: event.target.value })}
        required
      />
      <Input
        name="source_ref"
        placeholder="source_ref"
        className="w-64"
        value={draft.sourceRef}
        onChange={(event) => args.patch({ ...draft, sourceRef: event.target.value })}
        required
      />
    </div>
  )
}

function CollectiveMemberForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [draft, setDraft] = useState(FRESH_EXTRA)
  const save = useMutation({
    mutationFn: () =>
      recordCollectiveInvoice({
        sales_invoice_id: draft.invoiceId.trim(),
        shipment_id: draft.shipmentId.trim(),
        source_ref: draft.sourceRef.trim(),
      }),
    onSuccess: () => {
      setDraft({ ...FRESH_EXTRA })
      void client.invalidateQueries({ queryKey: ["collective-invoices", args.organizationId] })
    },
  })
  return (
    <form
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <ExtraShipmentFields draft={draft} patch={setDraft} />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz zbiorczą
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
  const members = useQuery({
    queryKey: ["collective-invoices", ctx.organizationId],
    queryFn: fetchCollectiveInvoices,
    enabled: ready,
    retry: false,
  })

  return (
    <div className="flex flex-col gap-4" data-sales-invoice="board">
      <CatalogHeading
        title="Faktury"
        subtitle="sales_invoice M-40 · numer sesji KSeF · nie live HTTP · nie druga marża"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {invoices.isError ? <CatalogError error={invoices.error} /> : null}
      {members.isError ? <CatalogError error={members.error} /> : null}
      <InvoiceRecordForm organizationId={ctx.organizationId} />
      <InvoiceKsefForm organizationId={ctx.organizationId} />
      <CollectiveMemberForm organizationId={ctx.organizationId} />
      {(invoices.data ?? []).map((row) => (
        <p key={row.id} className="font-mono text-xs">
          {row.invoice_kind} · {row.invoice_ref} · {row.source_ref}{" "}
          {row.ksef_ref ?? "—"}{" "}
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
      <ul className="text-xs" data-collective-invoice="members">
        {(members.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.sales_invoice_id} · {row.shipment_id} · {row.source_ref}
          </li>
        ))}
      </ul>
    </div>
  )
}
