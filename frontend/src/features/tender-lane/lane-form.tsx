import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { laneWrite, listLaneMarks, persistLaneMark } from "@/lib/tender-lanes-api"

type LaneDraft = {
  lotStamp: string
  originStamp: string
  destStamp: string
  originRef: string
}

const EMPTY_LANE: LaneDraft = {
  lotStamp: "",
  originStamp: "PLGDY",
  destStamp: "DEHAM",
  originRef: "fixture://tender-lane/",
}

function LaneSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_LANE)
  const persist = useMutation({
    mutationFn: () => persistLaneMark(laneWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_LANE })
      void cache.invalidateQueries({ queryKey: ["lane-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-tender-lane="lane-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Para UN/LOCODE na partii przetargu. Runda i auto-award zostają leftover. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Partia (tender_lot_id)
        <input
          aria-label="Identyfikator partii korytarza"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.lotStamp}
          onChange={(change) => setDraft({ ...draft, lotStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Origin UN/LOCODE
        <input
          aria-label="UN/LOCODE początku korytarza"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Destination UN/LOCODE
        <input
          aria-label="UN/LOCODE końca korytarza"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.destStamp}
          onChange={(change) => setDraft({ ...draft, destStamp: change.target.value })}
          required
        />
      </label>
      <div className="flex flex-col gap-1 text-xs">
        <span>Pochodzenie zapisu korytarza</span>
        <input
          aria-label="Pochodzenie zapisu korytarza przetargu"
          autoComplete="off"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          spellCheck={false}
          value={draft.originRef}
          onChange={(change) => setDraft({ ...draft, originRef: change.target.value })}
          required
        />
      </div>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz korytarz
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function LaneRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["lane-marks", args.organizationId],
    queryFn: listLaneMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-lane="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.tender_lot_id} · {row.origin_unlocode}→{row.destination_unlocode}
          </li>
        ))}
      </ul>
    </>
  )
}

export function LanePanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <LaneSave organizationId={args.organizationId} />
      <LaneRows organizationId={args.organizationId} />
    </div>
  )
}
