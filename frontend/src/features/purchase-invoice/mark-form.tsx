import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildPurchaseInvoiceWrite,
  savePurchaseInvoice,
} from "@/lib/purchase-invoices-api"

const KINDS = ["noted", "other"] as const

export function PurchaseInvoiceSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [ref, setRef] = useState("FV/2026/01")
  const [kind, setKind] = useState<string>("noted")
  const [origin, setOrigin] = useState("fixture://purchase-invoice/")
  const save = useMutation({
    mutationFn: () =>
      savePurchaseInvoice(buildPurchaseInvoiceWrite({ ref, kind, origin })),
    onSuccess: () => {
      setRef("FV/2026/01")
      setKind("noted")
      setOrigin("fixture://purchase-invoice/")
      void cache.invalidateQueries({
        queryKey: ["purchase-invoices", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-purchase-invoice="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Ingest FV zakupu jako katalog HITL. Numer i rodzaj to dane — nie ranking
        SQL i nie auto-link do charge.
      </p>
      <label className="grid gap-1 text-xs">
        Numer faktury (1–64)
        <input
          aria-label="Numer faktury zakupu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setRef(change.target.value)}
          required
          value={ref}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj faktury zakupu</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="purchase-invoice-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://purchase-invoice/…)"
        ariaLabel="Pochodzenie faktury zakupu"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz FV zakupu
      </Button>
    </form>
  )
}
