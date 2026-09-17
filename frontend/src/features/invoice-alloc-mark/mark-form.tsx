import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildInvoiceAllocMarkWrite,
  saveInvoiceAllocMark,
} from "@/lib/invoice-alloc-marks-api"

const KINDS = ["line", "header", "batch", "other"] as const

export function InvoiceAllocMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("alloc_01")
  const [kind, setKind] = useState<string>("line")
  const [origin, setOrigin] = useState("fixture://invoice-alloc-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveInvoiceAllocMark(buildInvoiceAllocMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("alloc_01")
      setKind("line")
      setOrigin("fixture://invoice-alloc-mark/")
      void cache.invalidateQueries({
        queryKey: ["invoice-alloc-marks", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-invoice-alloc-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stancja alokacji FV zakupu jako katalog HITL. Rodzaj to dana, nie
        allocation z kwotą i nie ranking SQL.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika alokacji FV"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj alokacji</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="invoice-alloc-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://invoice-alloc-mark/…)"
        ariaLabel="Pochodzenie znacznika alokacji FV"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz alokację FV
      </Button>
    </form>
  )
}
