import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { persistPurchaseOrder, purchaseOrderBody } from "@/lib/purchase-orders-api"

type PurchaseOrderDraft = {
  poSlug: string
  plantText: string
  originPointer: string
}

const EMPTY_HEADER: PurchaseOrderDraft = {
  poSlug: "po_gdansk_01",
  plantText: "",
  originPointer: "fixture://purchase-order/",
}

export function PurchaseOrderSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_HEADER)
  const persist = useMutation({
    mutationFn: () => persistPurchaseOrder(purchaseOrderBody(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_HEADER })
      void cache.invalidateQueries({ queryKey: ["purchase-order-headers", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-xl flex-col gap-3"
      data-purchase-order="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Nagłówek zamówienia zakupu: kod snake i opcjonalny zakład. To nie jest linia SKU, ASN
        ani zlecenie.
      </p>
      <label className="grid gap-1 text-xs">
        Kod zamówienia zakupu (snake 2–32)
        <input
          aria-label="Kod zamówienia zakupu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, poSlug: change.target.value })}
          required
          value={draft.poSlug}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Zakład (opcjonalna etykieta, nie FK)
        <input
          aria-label="Zakład zamówienia zakupu"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setDraft({ ...draft, plantText: change.target.value })}
          value={draft.plantText}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://purchase-order/…)"
        ariaLabel="Pochodzenie zamówienia zakupu"
        value={draft.originPointer}
        onChange={(originPointer) => setDraft({ ...draft, originPointer })}
      />
      <Button disabled={persist.isPending || !args.organizationId} type="submit">
        Zapisz zamówienie zakupu
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}
