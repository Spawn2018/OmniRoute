import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listSeatMarks, persistSeatMark, seatWrite } from "@/lib/tender-consortium-members-api"

type SeatDraft = {
  boardStamp: string
  partyStamp: string
  chairStamp: string
  originStamp: string
}

const EMPTY_SEAT: SeatDraft = {
  boardStamp: "",
  partyStamp: "",
  chairStamp: "lead",
  originStamp: "fixture://tender-consortium-member/",
}

function SeatSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_SEAT)
  const persist = useMutation({
    mutationFn: () => persistSeatMark(seatWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_SEAT })
      void cache.invalidateQueries({ queryKey: ["seat-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-tender-consortium-member="seat-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Fotel przy nagłówku i kontrahencie. Extract RFP i TED zostają leftover. Marża zostaje na
        `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Przetarg (tender_id)
        <input
          aria-label="Identyfikator przetargu fotela"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardStamp}
          onChange={(change) => setDraft({ ...draft, boardStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kontrahent (party_id)
        <input
          aria-label="Identyfikator kontrahenta fotela"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.partyStamp}
          onChange={(change) => setDraft({ ...draft, partyStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Fotel
        <select
          aria-label="Fotel lead albo member"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.chairStamp}
          onChange={(change) => setDraft({ ...draft, chairStamp: change.target.value })}
          required
        >
          <option value="lead">lead</option>
          <option value="member">member</option>
        </select>
      </label>
      <fieldset className="space-y-1 border-0 p-0">
        <legend className="text-xs font-medium">Pochodzenie fotela</legend>
        <input
          aria-label="Pochodzenie zapisu fotela konsorcjum"
          autoComplete="off"
          className="h-9 w-full rounded-md border bg-background px-2 font-mono text-[13px]"
          name="consortium-origin"
          spellCheck={false}
          value={draft.originStamp}
          onChange={(event) => {
            const originStamp = event.target.value
            setDraft((current) => ({ ...current, originStamp }))
          }}
          required
        />
      </fieldset>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz fotel
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function SeatRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["seat-marks", args.organizationId],
    queryFn: listSeatMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-consortium-member="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.seat_code}
          </li>
        ))}
      </ul>
    </>
  )
}

export function SeatPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <SeatSave organizationId={args.organizationId} />
      <SeatRows organizationId={args.organizationId} />
    </div>
  )
}
