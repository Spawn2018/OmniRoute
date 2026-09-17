import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildInvoiceMatchCandidateWrite,
  saveInvoiceMatchCandidate,
} from "@/lib/invoice-match-candidates-api"

const KINDS = ["proposed", "held", "rejected", "other"] as const

export function InvoiceMatchCandidateSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("cand_01")
  const [kind, setKind] = useState<string>("proposed")
  const [origin, setOrigin] = useState("fixture://invoice-match-candidate/")
  const save = useMutation({
    mutationFn: () =>
      saveInvoiceMatchCandidate(buildInvoiceMatchCandidateWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("cand_01")
      setKind("proposed")
      setOrigin("fixture://invoice-match-candidate/")
      void cache.invalidateQueries({
        queryKey: ["invoice-match-candidates", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-invoice-match-candidate="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stancja kandydata dopasowania FV (domestic/international/waste) jako katalog HITL. Rodzaj to dana, nie
        ranking SQL i nie auto-link.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika kandydata dopasowania FV"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj kandydata</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="relation-document-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://invoice-match-candidate/…)"
        ariaLabel="Pochodzenie znacznika kandydata dopasowania FV"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz kandydata
      </Button>
    </form>
  )
}
