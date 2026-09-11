import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { asnBody, persistAsn } from "@/lib/asns-api"

type AsnDraft = {
  purchaseOrderId: string
  asnSlug: string
  plantText: string
  carrierText: string
  shipRefText: string
  guideSlug: string
  originPointer: string
}

const EMPTY_ASN: AsnDraft = {
  purchaseOrderId: "",
  asnSlug: "asn_01",
  plantText: "",
  carrierText: "",
  shipRefText: "",
  guideSlug: "",
  originPointer: "fixture://asn/",
}

export function AsnSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_ASN)
  const persist = useMutation({
    mutationFn: () => persistAsn(asnBody(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_ASN })
      void cache.invalidateQueries({ queryKey: ["asns", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-xl flex-col gap-3"
      data-asn="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Awizo wysyłki na istniejącym zamówieniu zakupu. To nie jest live EDI 856 ani zlecenie. Przy
        egzekucji block_409 wpisz guide_code z katalogu przewodnika.
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
        Kod awiza (snake 2–32)
        <input
          aria-label="Kod awiza wysyłki"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, asnSlug: change.target.value })}
          required
          value={draft.asnSlug}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Kod przewodnika (guide_code, opcjonalnie / wymagany przy block_409)
        <input
          aria-label="Kod przewodnika routingu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, guideSlug: change.target.value })}
          value={draft.guideSlug}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Zakład (opcjonalnie)
        <input
          aria-label="Zakład awiza"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setDraft({ ...draft, plantText: change.target.value })}
          value={draft.plantText}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Przewoźnik (etykieta, nie FK)
        <input
          aria-label="Przewoźnik awiza"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setDraft({ ...draft, carrierText: change.target.value })}
          value={draft.carrierText}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Referencja wysyłki (opcjonalnie)
        <input
          aria-label="Referencja awiza"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setDraft({ ...draft, shipRefText: change.target.value })}
          value={draft.shipRefText}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Pochodzenie (source_ref)
        <input
          aria-label="Pochodzenie awiza"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, originPointer: change.target.value })}
          required
          value={draft.originPointer}
        />
      </label>
      {persist.error ? <CatalogError error={persist.error} /> : null}
      <Button disabled={!args.organizationId || persist.isPending} type="submit">
        Zapisz awizo wysyłki
      </Button>
    </form>
  )
}
