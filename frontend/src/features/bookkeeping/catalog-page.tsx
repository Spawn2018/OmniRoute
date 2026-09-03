import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { fetchBookkeeping, recordBookkeeping } from "@/lib/bookkeeping-api"
import { getTenantContext } from "@/lib/tenant"

type EntryDraft = {
  chargeId: string
  invoiceId: string
  sourceRef: string
}

const FRESH: EntryDraft = {
  chargeId: "",
  invoiceId: "",
  sourceRef: "fixture://bookkeeping/",
}

function ChargeInvoiceWrap(args: { draft: EntryDraft; patch: (next: EntryDraft) => void }) {
  const draft = args.draft
  return (
    <div className="flex flex-wrap gap-2">
      <Input
        name="charge_id"
        placeholder="charge_id"
        className="w-56"
        value={draft.chargeId}
        onChange={(event) => args.patch({ ...draft, chargeId: event.target.value })}
        required
      />
      <Input
        name="sales_invoice_id"
        placeholder="sales_invoice_id"
        className="w-56"
        value={draft.invoiceId}
        onChange={(event) => args.patch({ ...draft, invoiceId: event.target.value })}
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

function EntrySaveStrip(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [draft, setDraft] = useState(FRESH)
  const save = useMutation({
    mutationFn: () =>
      recordBookkeeping({
        charge_id: draft.chargeId.trim(),
        sales_invoice_id: draft.invoiceId.trim(),
        source_ref: draft.sourceRef.trim(),
      }),
    onSuccess: () => {
      setDraft({ ...FRESH })
      void client.invalidateQueries({ queryKey: ["bookkeeping-rows", args.organizationId] })
    },
  })
  return (
    <form
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <ChargeInvoiceWrap draft={draft} patch={setDraft} />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz dekret
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function BookkeepingPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const rows = useQuery({
    queryKey: ["bookkeeping-rows", ctx.organizationId],
    queryFn: fetchBookkeeping,
    enabled: ready,
    retry: false,
  })

  return (
    <section className="flex flex-col gap-3" data-bookkeeping="board">
      <CatalogHeading
        title="Księgowość"
        subtitle="bookkeeping M-47 · para opłata+faktura · nie JPK · nie odejmowanie"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      <EntrySaveStrip organizationId={ctx.organizationId} />
      <ol className="list-decimal text-xs">
        {(rows.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.charge_id} · {row.sales_invoice_id} · {row.source_ref}{" "}
            <Link className="underline" to="/charges">
              opłata
            </Link>{" "}
            <Link className="underline" to="/invoices">
              faktura
            </Link>
          </li>
        ))}
      </ol>
    </section>
  )
}
