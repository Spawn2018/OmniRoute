import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { circleWrite, persistCircleSim } from "@/lib/circle-sims-api"

type CircleDraft = {
  codeStamp: string
  unloadStamp: string
  loadStamp: string
  originStamp: string
}

const EMPTY_CIRCLE: CircleDraft = {
  codeStamp: "backhaul_a",
  unloadStamp: "PLGDY",
  loadStamp: "DEHAM",
  originStamp: "fixture://circle-sim/",
}

export function CircleSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_CIRCLE)
  const persist = useMutation({
    mutationFn: () => persistCircleSim(circleWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_CIRCLE })
      void cache.invalidateQueries({ queryKey: ["circle-sims", args.organizationId] })
      void cache.invalidateQueries({ queryKey: ["circle-sim-pairs", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-circle-sim="circle-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Kółko jako dane: kod oraz para UN/LOCODE rozładunek / załadunek. Serwis nie liczy
        przecięcia ani km. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kod kółka (snake 2–32)
        <input
          aria-label="Kod kółka"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.codeStamp}
          onChange={(change) => setDraft({ ...draft, codeStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        UN/LOCODE rozładunku
        <input
          aria-label="UN/LOCODE rozładunku"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.unloadStamp}
          onChange={(change) => setDraft({ ...draft, unloadStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        UN/LOCODE załadunku
        <input
          aria-label="UN/LOCODE załadunku"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.loadStamp}
          onChange={(change) => setDraft({ ...draft, loadStamp: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://circle-sim/…)"
        ariaLabel="source_ref kółka"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz kółko
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}
