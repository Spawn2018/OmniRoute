import { Link } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { getTenantContext } from "@/lib/tenant"
import { fetchMoneyCosts, recordMoneyCost } from "@/lib/money-costs-api"

type CostDraft = {
  paymentId: string
  rateId: string
  sourceRef: string
}

const START: CostDraft = {
  paymentId: "",
  rateId: "",
  sourceRef: "fixture://money-cost/",
}

function PaymentRateInputs(args: { draft: CostDraft; setDraft: (next: CostDraft) => void }) {
  const draft = args.draft
  return (
    <div className="flex flex-col gap-4 border-l-2 border-primary pl-3">
      <Input
        name="bank_payment_id"
        placeholder="bank_payment_id"
        value={draft.paymentId}
        onChange={(event) => args.setDraft({ ...draft, paymentId: event.target.value })}
        required
      />
      <Input
        name="nbp_rate_id"
        placeholder="nbp_rate_id"
        value={draft.rateId}
        onChange={(event) => args.setDraft({ ...draft, rateId: event.target.value })}
        required
      />
      <Input
        name="source_ref"
        placeholder="source_ref"
        value={draft.sourceRef}
        onChange={(event) => args.setDraft({ ...draft, sourceRef: event.target.value })}
        required
      />
    </div>
  )
}

function CostSaveBox(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [draft, setDraft] = useState(START)
  const save = useMutation({
    mutationFn: () =>
      recordMoneyCost({
        bank_payment_id: draft.paymentId.trim(),
        nbp_rate_id: draft.rateId.trim(),
        source_ref: draft.sourceRef.trim(),
      }),
    onSuccess: () => {
      setDraft({ ...START })
      void client.invalidateQueries({ queryKey: ["money-costs", args.organizationId] })
    },
  })
  return (
    <form
      className="max-w-md space-y-3 bg-card/50 p-4"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <PaymentRateInputs draft={draft} setDraft={setDraft} />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz koszt
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function MoneyCostPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const rows = useQuery({
    queryKey: ["money-costs", ctx.organizationId],
    queryFn: fetchMoneyCosts,
    enabled: ready,
    retry: false,
  })

  return (
    <section className="flex flex-col gap-3" data-money-cost="board">
      <CatalogHeading
        title="Koszt pieniądza"
        subtitle="money_cost M-43 · para płatność+kurs NBP · nie odsetki · nie mnożenie"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      <CostSaveBox organizationId={ctx.organizationId} />
      <ol className="list-decimal pl-5">
        {(rows.data ?? []).map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.bank_payment_id} · {row.nbp_rate_id} · {row.source_ref}{" "}
            <Link className="underline" to="/payments">
              płatność
            </Link>{" "}
            <Link className="underline" to="/nbp-rates">
              kurs
            </Link>
          </li>
        ))}
      </ol>
    </section>
  )
}
