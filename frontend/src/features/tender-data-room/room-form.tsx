import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listRoomMarks, ndaWrite, persistRoomMark } from "@/lib/tender-data-rooms-api"

type RoomDraft = {
  boardStamp: string
  ndaStamp: string
  originRef: string
}

const EMPTY_ROOM: RoomDraft = {
  boardStamp: "",
  ndaStamp: "signed",
  originRef: "fixture://tender-data-room/",
}

function RoomSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_ROOM)
  const persist = useMutation({
    mutationFn: () => persistRoomMark(ndaWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_ROOM })
      void cache.invalidateQueries({ queryKey: ["room-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-md flex-col gap-3"
      data-tender-data-room="room-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik NDA przy nagłówku przetargu. Extract RFP i matryca zostają leftover. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Przetarg (tender_id)
        <input
          aria-label="Identyfikator przetargu pokoju danych"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardStamp}
          onChange={(change) => setDraft({ ...draft, boardStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Znacznik NDA
        <input
          aria-label="Znacznik NDA pokoju danych"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.ndaStamp}
          onChange={(change) => setDraft({ ...draft, ndaStamp: change.target.value })}
          required
        />
      </label>
      <fieldset className="m-0 border-0 p-0">
        <legend className="mb-1 px-0 text-xs">Pochodzenie zapisu pokoju danych</legend>
        <input
          aria-label="Pochodzenie zapisu pokoju danych"
          autoComplete="off"
          className="h-9 w-full rounded-md border bg-background px-2 font-mono text-[13px]"
          name="room-source-ref"
          spellCheck={false}
          value={draft.originRef}
          onChange={(change) => setDraft({ ...draft, originRef: change.target.value })}
          required
        />
      </fieldset>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz pokój
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function RoomRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["room-marks", args.organizationId],
    queryFn: listRoomMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-data-room="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.tender_id} · NDA {row.nda_mark}
          </li>
        ))}
      </ul>
    </>
  )
}

export function RoomPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <RoomSave organizationId={args.organizationId} />
      <RoomRows organizationId={args.organizationId} />
    </div>
  )
}
