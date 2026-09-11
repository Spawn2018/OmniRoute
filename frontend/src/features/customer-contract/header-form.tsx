import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { pactHeaderWrite, persistCustomerContract } from "@/lib/customer-contracts-api"

type PactHeaderDraft = {
  pactMark: string
  loaderHint: string
  buyerHint: string
  originHint: string
  attachOpaque: boolean
}

const EMPTY_PACT: PactHeaderDraft = {
  pactMark: "acme_pl_2026",
  loaderHint: "Acme Logistics",
  buyerHint: "Bayer PL",
  originHint: "fixture://contract/",
  attachOpaque: false,
}

export function CustomerContractSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_PACT)
  const persist = useMutation({
    mutationFn: () => persistCustomerContract(pactHeaderWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_PACT })
      void cache.invalidateQueries({ queryKey: ["pact-headers", args.organizationId] })
    },
  })
  const locked = persist.isPending || !args.organizationId
  return (
    <form
      className="flex max-w-xl flex-col gap-2"
      data-customer-contract="header-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Nagłówek umowy: kod snake oraz etykiety załadowcy i odbiorcy. Opcjonalny fixture blob
        zapisuje tylko obecność opakowania — lista nie pokazuje bajtów. To nie jest szyfr.
      </p>
      <label className="text-xs">
        Kod umowy (snake 2–32)
        <input
          aria-label="Kod umowy klienta"
          className="mt-1 h-9 w-full rounded-md border bg-background px-2 font-mono"
          value={draft.pactMark}
          onChange={(change) => setDraft({ ...draft, pactMark: change.target.value })}
          required
        />
      </label>
      <label className="text-xs">
        Załadowca (etykieta, nie FK)
        <input
          aria-label="Etykieta załadowcy umowy"
          className="mt-1 h-9 w-full rounded-md border bg-background px-2"
          value={draft.loaderHint}
          onChange={(change) => setDraft({ ...draft, loaderHint: change.target.value })}
          required
        />
      </label>
      <label className="text-xs">
        Odbiorca (etykieta, nie FK)
        <input
          aria-label="Etykieta odbiorcy umowy"
          className="mt-1 h-9 w-full rounded-md border bg-background px-2"
          value={draft.buyerHint}
          onChange={(change) => setDraft({ ...draft, buyerHint: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (`tenant:manual` albo `fixture://contract/…`)"
        ariaLabel="source_ref nagłówka umowy"
        value={draft.originHint}
        onChange={(originHint) => setDraft({ ...draft, originHint })}
      />
      <label className="flex items-center gap-2 text-xs">
        <input
          type="checkbox"
          aria-label="dołącz fixture blob"
          checked={draft.attachOpaque}
          onChange={(change) => setDraft({ ...draft, attachOpaque: change.target.checked })}
        />
        dołącz fixture blob (obecność, nie podgląd)
      </label>
      <div>
        <Button type="submit" disabled={locked}>
          Zapisz nagłówek umowy
        </Button>
      </div>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}
