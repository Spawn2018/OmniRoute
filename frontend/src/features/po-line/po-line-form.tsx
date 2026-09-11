import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { persistPoLine, poLineBody } from "@/lib/po-lines-api"

type PoLineDraft = {
  purchaseOrderId: string
  lineSlug: string
  skuText: string
  qtyText: string
  uomText: string
  plantText: string
  batchText: string
  serialText: string
  cooText: string
  originPointer: string
}

const EMPTY_LINE: PoLineDraft = {
  purchaseOrderId: "",
  lineSlug: "line_01",
  skuText: "SKU-4401",
  qtyText: "12.5",
  uomText: "pcs",
  plantText: "",
  batchText: "",
  serialText: "",
  cooText: "",
  originPointer: "fixture://po-line/",
}

export function PoLineSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_LINE)
  const persist = useMutation({
    mutationFn: () => persistPoLine(poLineBody(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_LINE })
      void cache.invalidateQueries({ queryKey: ["po-lines", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-xl flex-col gap-3"
      data-po-line="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Linia zamówienia zakupu: SKU, ilość dziesiętna i JM. To nie jest ASN ani zlecenie.
      </p>
      <label className="grid gap-1 text-xs">
        Id nagłówka zamówienia zakupu
        <input
          aria-label="Id nagłówka zamówienia zakupu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, purchaseOrderId: change.target.value })}
          required
          value={draft.purchaseOrderId}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Kod linii (snake 2–32)
        <input
          aria-label="Kod linii zamówienia"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, lineSlug: change.target.value })}
          required
          value={draft.lineSlug}
        />
      </label>
      <label className="grid gap-1 text-xs">
        SKU
        <input
          aria-label="SKU linii zamówienia"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, skuText: change.target.value })}
          required
          value={draft.skuText}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Ilość (Decimal, nie float)
        <input
          aria-label="Ilość linii zamówienia"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, qtyText: change.target.value })}
          required
          value={draft.qtyText}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Jednostka miary
        <input
          aria-label="Jednostka miary linii zamówienia"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setDraft({ ...draft, uomText: change.target.value })}
          required
          value={draft.uomText}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Zakład (opcjonalna etykieta)
        <input
          aria-label="Zakład linii zamówienia"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setDraft({ ...draft, plantText: change.target.value })}
          value={draft.plantText}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Partia (opcjonalna etykieta)
        <input
          aria-label="Partia linii zamówienia"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setDraft({ ...draft, batchText: change.target.value })}
          value={draft.batchText}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Seria (opcjonalna etykieta)
        <input
          aria-label="Seria linii zamówienia"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setDraft({ ...draft, serialText: change.target.value })}
          value={draft.serialText}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Kraj pochodzenia (opcjonalna etykieta)
        <input
          aria-label="Kraj pochodzenia linii zamówienia"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setDraft({ ...draft, cooText: change.target.value })}
          value={draft.cooText}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://po-line/…)"
        ariaLabel="Pochodzenie linii zamówienia"
        value={draft.originPointer}
        onChange={(originPointer) => setDraft({ ...draft, originPointer })}
      />
      <Button disabled={persist.isPending || !args.organizationId} type="submit">
        Zapisz linię zamówienia
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}
