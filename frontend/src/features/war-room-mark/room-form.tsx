import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listWarRoomMarks, persistRoomMark, roomWrite } from "@/lib/war-room-marks-api"

type RoomDraft = {
  kindStamp: string
  originStamp: string
}

const EMPTY_ROOM: RoomDraft = {
  kindStamp: "weather",
  originStamp: "fixture://war-room-mark/",
}

const INCIDENTS = [
  { token: "weather", caption: "pogoda" },
  { token: "congestion", caption: "kongestia" },
  { token: "labor", caption: "strajk" },
  { token: "carrier", caption: "armator" },
  { token: "credit", caption: "kredyt" },
  { token: "other", caption: "inne" },
] as const

function RoomSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_ROOM)
  const persist = useMutation({
    mutationFn: () => persistRoomMark(roomWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_ROOM })
      void cache.invalidateQueries({ queryKey: ["incident-stamps", args.organizationId] })
    },
  })
  const blocked = !args.organizationId || persist.isPending
  return (
    <form
      className="flex max-w-lg flex-col gap-3"
      data-war-room="kind-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Sześć rodzajów incydentu. To nie jest scalanie alertów i nie drugi czat.
        Marża zostaje na `/charges`.
      </p>
      <fieldset className="flex flex-col gap-1 text-xs">
        <legend>Rodzaj incydentu (allowlista)</legend>
        {INCIDENTS.map((choice) => (
          <label key={choice.token} className="inline-flex items-center gap-2">
            <input
              type="radio"
              name="incident-kind"
              aria-label={`Incydent ${choice.caption}`}
              checked={draft.kindStamp === choice.token}
              onChange={() => setDraft({ ...draft, kindStamp: choice.token })}
              value={choice.token}
            />
            <span className="font-mono">{choice.token}</span>
            <span className="text-muted-foreground">{choice.caption}</span>
          </label>
        ))}
      </fieldset>
      <label className="flex flex-col gap-1 text-xs">
        Pochodzenie zapisu
        <input
          aria-label="source_ref sali kryzysowej"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          placeholder="tenant:manual albo fixture://war-room-mark/…"
          required
        />
      </label>
      <Button type="submit" disabled={blocked}>
        Zapisz salę kryzysową
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function RoomRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["incident-stamps", args.organizationId],
    queryFn: listWarRoomMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  const rows = listed.data ?? []
  return (
    <div>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <table data-war-room="rows" className="text-xs">
        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              <td className="font-mono pr-3" data-incident-kind={row.incident_kind}>
                {row.incident_kind}
              </td>
              <td className="font-mono text-muted-foreground">{row.source_ref}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export function RoomPanel(args: { organizationId: string | null }) {
  return (
    <div className="flex flex-col gap-8 lg:flex-row">
      <RoomSave organizationId={args.organizationId} />
      <RoomRows organizationId={args.organizationId} />
    </div>
  )
}
