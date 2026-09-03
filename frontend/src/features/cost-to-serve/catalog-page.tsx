import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { fetchCostToServeRows, recordCostToServe } from "@/lib/cost-to-serve-api"
import { getTenantContext } from "@/lib/tenant"

type ServeDraft = {
  sopId: string
  quoteId: string
  sourceRef: string
}

const FRESH: ServeDraft = {
  sopId: "",
  quoteId: "",
  sourceRef: "fixture://cost-to-serve/",
}

function SopQuoteStack(args: { draft: ServeDraft; patch: (next: ServeDraft) => void }) {
  const draft = args.draft
  return (
    <div className="flex flex-col gap-1">
      <label className="text-xs" htmlFor="customer_sop_id">
        SOP
        <Input
          id="customer_sop_id"
          name="customer_sop_id"
          placeholder="customer_sop_id"
          value={draft.sopId}
          onChange={(event) => args.patch({ ...draft, sopId: event.target.value })}
          required
        />
      </label>
      <label className="text-xs" htmlFor="quotation_id">
        Wycena
        <Input
          id="quotation_id"
          name="quotation_id"
          placeholder="quotation_id"
          value={draft.quoteId}
          onChange={(event) => args.patch({ ...draft, quoteId: event.target.value })}
          required
        />
      </label>
      <label className="text-xs" htmlFor="source_ref">
        Źródło
        <Input
          id="source_ref"
          name="source_ref"
          placeholder="source_ref"
          value={draft.sourceRef}
          onChange={(event) => args.patch({ ...draft, sourceRef: event.target.value })}
          required
        />
      </label>
    </div>
  )
}

function ServeSaveStrip(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [draft, setDraft] = useState(FRESH)
  const save = useMutation({
    mutationFn: () =>
      recordCostToServe({
        customer_sop_id: draft.sopId.trim(),
        quotation_id: draft.quoteId.trim(),
        source_ref: draft.sourceRef.trim(),
      }),
    onSuccess: () => {
      setDraft({ ...FRESH })
      void client.invalidateQueries({ queryKey: ["cost-to-serve-rows", args.organizationId] })
    },
  })
  return (
    <form
      className="w-full"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <SopQuoteStack draft={draft} patch={setDraft} />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz koszt obsługi
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function CostToServePage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const rows = useQuery({
    queryKey: ["cost-to-serve-rows", ctx.organizationId],
    queryFn: fetchCostToServeRows,
    enabled: ready,
    retry: false,
  })

  return (
    <section className="flex flex-col gap-3" data-cost-to-serve="board">
      <CatalogHeading
        title="Koszt obsługi klienta"
        subtitle="cost_to_serve M-46 · para SOP+wycena · nie ABC · nie suma"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      <ServeSaveStrip organizationId={ctx.organizationId} />
      <dl className="text-xs">
        {(rows.data ?? []).map((row) => (
          <div key={row.id} className="font-mono">
            <dt className="inline">{row.customer_sop_id}</dt>
            {" · "}
            <dd className="inline">{row.quotation_id}</dd>
            {" · "}
            <dd className="inline">{row.source_ref}</dd>{" "}
            <Link className="underline" to="/customer-sops">
              SOP
            </Link>{" "}
            <Link className="underline" to="/quotations">
              wycena
            </Link>
          </div>
        ))}
      </dl>
    </section>
  )
}
