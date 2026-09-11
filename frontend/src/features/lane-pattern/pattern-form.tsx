import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefHintField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listCorridorPatterns, patternWrite, persistPatternMark } from "@/lib/lane-patterns-api"

type PatternDraft = {
  startStamp: string
  endStamp: string
  originStamp: string
}

const EMPTY_PATTERN: PatternDraft = {
  startStamp: "PLGDY",
  endStamp: "DEHAM",
  originStamp: "fixture://lane-pattern/",
}

function PatternSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_PATTERN)
  const persist = useMutation({
    mutationFn: () => persistPatternMark(patternWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_PATTERN })
      void cache.invalidateQueries({ queryKey: ["corridor-patterns", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-lane-pattern="pattern-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Para UN/LOCODE bez partii przetargu. Kilometry i circle_sim zostają leftover. Marża zostaje na
        `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Origin UN/LOCODE
        <input
          aria-label="UN/LOCODE początku wzorca"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.startStamp}
          onChange={(change) => setDraft({ ...draft, startStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Destination UN/LOCODE
        <input
          aria-label="UN/LOCODE końca wzorca"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.endStamp}
          onChange={(change) => setDraft({ ...draft, endStamp: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefHintField
        hint="source_ref: tenant:manual albo fixture://lane-pattern/…"
        ariaLabel="source_ref wzorca korytarza"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz wzorzec korytarza
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function PatternRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["corridor-patterns", args.organizationId],
    queryFn: listCorridorPatterns,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-lane-pattern="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.origin_unlocode}→{row.destination_unlocode}
          </li>
        ))}
      </ul>
    </>
  )
}

export function PatternPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <PatternSave organizationId={args.organizationId} />
      <PatternRows organizationId={args.organizationId} />
    </div>
  )
}
