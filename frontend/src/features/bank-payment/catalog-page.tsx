import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { fetchBankPayments, recordBankPayment } from "@/lib/bank-payments-api"
import { getTenantContext } from "@/lib/tenant"

type PaymentDraft = {
  invoiceId: string
  accountId: string
  sourceRef: string
}

const BLANK: PaymentDraft = {
  invoiceId: "",
  accountId: "",
  sourceRef: "fixture://bank-payment/",
}

function InvoiceAccountFields(args: {
  draft: PaymentDraft
  onChange: (next: PaymentDraft) => void
}) {
  const draft = args.draft
  return (
    <fieldset className="grid gap-2 bg-muted/30 p-2">
      <legend className="text-xs">para faktura + rachunek</legend>
      <Input
        name="sales_invoice_id"
        placeholder="sales_invoice_id"
        value={draft.invoiceId}
        onChange={(event) => args.onChange({ ...draft, invoiceId: event.target.value })}
        required
      />
      <Input
        name="party_bank_account_id"
        placeholder="party_bank_account_id"
        value={draft.accountId}
        onChange={(event) => args.onChange({ ...draft, accountId: event.target.value })}
        required
      />
      <Input
        name="source_ref"
        placeholder="source_ref"
        value={draft.sourceRef}
        onChange={(event) => args.onChange({ ...draft, sourceRef: event.target.value })}
        required
      />
    </fieldset>
  )
}

function PaymentSaveForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [draft, setDraft] = useState(BLANK)
  const save = useMutation({
    mutationFn: () =>
      recordBankPayment({
        sales_invoice_id: draft.invoiceId.trim(),
        party_bank_account_id: draft.accountId.trim(),
        source_ref: draft.sourceRef.trim(),
      }),
    onSuccess: () => {
      setDraft({ ...BLANK })
      void client.invalidateQueries({ queryKey: ["bank-payments", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-2 border border-dashed border-border p-2"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <InvoiceAccountFields draft={draft} onChange={setDraft} />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz płatność
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function BankPaymentPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const rows = useQuery({
    queryKey: ["bank-payments", ctx.organizationId],
    queryFn: fetchBankPayments,
    enabled: ready,
    retry: false,
  })

  return (
    <section className="flex flex-col gap-3" data-bank-payment="board">
      <CatalogHeading
        title="Bank i płatności"
        subtitle="bank_payment M-42 · para faktura+rachunek · nie SEPA · nie druga marża"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      <PaymentSaveForm organizationId={ctx.organizationId} />
      <ul>
        {(rows.data ?? []).map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.sales_invoice_id} · {row.party_bank_account_id} · {row.source_ref}{" "}
            <Link className="underline" to="/invoices">
              faktura
            </Link>{" "}
            <Link className="underline" to="/parties">
              kontrahent
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
