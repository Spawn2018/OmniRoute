import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { laneKmWrite, persistLaneKm } from "@/lib/lane-kms-api"

type LaneKmDraft = {
  codeStamp: string
  loadedStamp: string
  emptyStamp: string
  approachStamp: string
  originStamp: string
}

const EMPTY_LANE_KM: LaneKmDraft = {
  codeStamp: "backhaul_a",
  loadedStamp: "120.5",
  emptyStamp: "40",
  approachStamp: "15.25",
  originStamp: "fixture://lane-km/",
}

export function LaneKmSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_LANE_KM)
  const persist = useMutation({
    mutationFn: () => persistLaneKm(laneKmWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_LANE_KM })
      void cache.invalidateQueries({ queryKey: ["lane-kms", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-lane-km="lane-km-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Km korytarza jako dane: kod oraz ładowny / pusty / dolot. Serwis nie liczy Haversine
        ani sumy kółek. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kod km (snake 2–32)
        <input
          aria-label="Kod km korytarza"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.codeStamp}
          onChange={(change) => setDraft({ ...draft, codeStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Km ładowny
        <input
          aria-label="Km ładowny"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.loadedStamp}
          onChange={(change) => setDraft({ ...draft, loadedStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Km pusty
        <input
          aria-label="Km pusty"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.emptyStamp}
          onChange={(change) => setDraft({ ...draft, emptyStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Km dolot
        <input
          aria-label="Km dolot"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.approachStamp}
          onChange={(change) => setDraft({ ...draft, approachStamp: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://lane-km/…)"
        ariaLabel="source_ref km korytarza"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz km korytarza
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}
