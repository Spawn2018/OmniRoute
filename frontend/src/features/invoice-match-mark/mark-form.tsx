import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildInvoiceMatchMarkWrite,
  saveInvoiceMatchMark,
} from "@/lib/invoice-match-marks-api"

const KINDS = ["candidate", "rank", "allocate", "other"] as const

export function InvoiceMatchMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("match_01")
  const [kind, setKind] = useState<string>("candidate")
  const [origin, setOrigin] = useState("fixture://invoice-match-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveInvoiceMatchMark(buildInvoiceMatchMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("match_01")
      setKind("candidate")
      setOrigin("fixture://invoice-match-mark/")
      void cache.invalidateQueries({
        queryKey: ["invoice-match-marks", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-invoice-match-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stancja dopasowania FV zakupu jako katalog HITL. Rodzaj to dana, nie
        ranking SQL i nie allocation.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika match FV"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj match</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="invoice-match-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://invoice-match-mark/…)"
        ariaLabel="Pochodzenie znacznika match FV"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz match FV
      </Button>
    </form>
  )
}
