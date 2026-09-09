import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { clockWrite, listClockMarks, persistClockMark } from "@/lib/free-time-clocks-api"

type ClockDraft = {
  kindStamp: string
  daysStamp: string
  originStamp: string
}

const EMPTY_CLOCK: ClockDraft = {
  kindStamp: "detention",
  daysStamp: "7",
  originStamp: "fixture://free-time-clock/",
}

const KINDS = ["demurrage", "detention", "mixed", "rollover"] as const

function ClockSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_CLOCK)
  const persist = useMutation({
    mutationFn: () => persistClockMark(clockWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_CLOCK })
      void cache.invalidateQueries({ queryKey: ["clock-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-free-time-clock="clock-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Rodzaj D&amp;D albo rollover plus liczba dni wolnych. Countdown, blank sailing i szkic opłaty
        zostają leftover. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj zegara (allowlista)
        <select
          aria-label="Rodzaj zegara D&D"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindStamp}
          onChange={(change) => setDraft({ ...draft, kindStamp: change.target.value })}
          required
        >
          {KINDS.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Dni wolne (liczba całkowita, nie odliczanie)
        <input
          aria-label="Dni wolne zegara D&D"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.daysStamp}
          onChange={(change) => setDraft({ ...draft, daysStamp: change.target.value })}
          inputMode="numeric"
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        source_ref (tenant:manual albo fixture://free-time-clock/…)
        <input
          aria-label="source_ref zegara D&D"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz zegar D&amp;D
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function ClockRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["clock-marks", args.organizationId],
    queryFn: listClockMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-free-time-clock="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.clock_kind} {row.free_days}d
          </li>
        ))}
      </ul>
    </>
  )
}

export function ClockPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <ClockSave organizationId={args.organizationId} />
      <ClockRows organizationId={args.organizationId} />
    </div>
  )
}
