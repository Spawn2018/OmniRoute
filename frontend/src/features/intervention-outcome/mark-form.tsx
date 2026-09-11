import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildInterventionOutcomeWrite,
  saveInterventionOutcome,
} from "@/lib/intervention-outcomes-api"

const KINDS = ["contained", "rerouted", "claimed", "other"] as const

export function InterventionOutcomeSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("contained_01")
  const [kind, setKind] = useState<string>("contained")
  const [origin, setOrigin] = useState("fixture://intervention-outcome/")
  const save = useMutation({
    mutationFn: () =>
      saveInterventionOutcome(buildInterventionOutcomeWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("contained_01")
      setKind("contained")
      setOrigin("fixture://intervention-outcome/")
      void cache.invalidateQueries({
        queryKey: ["intervention-outcomes", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-intervention-outcome="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Wynik interwencji jako katalog HITL. Rodzaj to dana, nie SQL saved i nie
        druga marża.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod wyniku interwencji"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj wyniku</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="intervention-result"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://intervention-outcome/…)"
        ariaLabel="Pochodzenie wyniku interwencji"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz wynik interwencji
      </Button>
    </form>
  )
}
