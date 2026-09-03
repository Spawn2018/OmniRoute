import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { fetchFxDifferences, recordFxDifference } from "@/lib/fx-differences-api"
import { getTenantContext } from "@/lib/tenant"

type FxDraft = {
  quoteId: string
  rateId: string
  sourceRef: string
}

const FRESH: FxDraft = {
  quoteId: "",
  rateId: "",
  sourceRef: "fixture://fx-difference/",
}

function QuoteRatePair(args: { draft: FxDraft; patch: (next: FxDraft) => void }) {
  const draft = args.draft
  return (
    <div className="divide-y divide-border rounded-sm border border-input">
      <Input
        name="quotation_id"
        placeholder="quotation_id"
        className="rounded-none border-0"
        value={draft.quoteId}
        onChange={(event) => args.patch({ ...draft, quoteId: event.target.value })}
        required
      />
      <Input
        name="nbp_rate_id"
        placeholder="nbp_rate_id"
        className="rounded-none border-0"
        value={draft.rateId}
        onChange={(event) => args.patch({ ...draft, rateId: event.target.value })}
        required
      />
      <Input
        name="source_ref"
        placeholder="source_ref"
        className="rounded-none border-0"
        value={draft.sourceRef}
        onChange={(event) => args.patch({ ...draft, sourceRef: event.target.value })}
        required
      />
    </div>
  )
}

function FxSaveStrip(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [draft, setDraft] = useState(FRESH)
  const save = useMutation({
    mutationFn: () =>
      recordFxDifference({
        quotation_id: draft.quoteId.trim(),
        nbp_rate_id: draft.rateId.trim(),
        source_ref: draft.sourceRef.trim(),
      }),
    onSuccess: () => {
      setDraft({ ...FRESH })
      void client.invalidateQueries({ queryKey: ["fx-differences", args.organizationId] })
    },
  })
  return (
    <form
      className="w-full max-w-2xl space-y-2"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <QuoteRatePair draft={draft} patch={setDraft} />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz różnicę
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function FxDifferencePage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const rows = useQuery({
    queryKey: ["fx-differences", ctx.organizationId],
    queryFn: fetchFxDifferences,
    enabled: ready,
    retry: false,
  })

  return (
    <section className="flex flex-col gap-3" data-fx-difference="board">
      <CatalogHeading
        title="Różnice kursowe"
        subtitle="fx_difference M-44 · para wycena+kurs NBP · nie przeliczenie"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      <FxSaveStrip organizationId={ctx.organizationId} />
      <table className="w-full text-left text-xs">
        <tbody>
          {(rows.data ?? []).map((row) => (
            <tr key={row.id} className="font-mono">
              <td>{row.quotation_id}</td>
              <td>{row.nbp_rate_id}</td>
              <td>{row.source_ref}</td>
              <td>
                <Link className="underline" to="/quotations">
                  wycena
                </Link>{" "}
                <Link className="underline" to="/nbp-rates">
                  NBP
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  )
}
