import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { indexWrite, listIndexMarks, persistIndexMark } from "@/lib/fuel-indexes-api"

type IndexDraft = {
  kindToken: string
  dayStamp: string
  pointMark: string
  originStamp: string
}

const EMPTY_INDEX: IndexDraft = {
  kindToken: "fsc",
  dayStamp: "2026-03-01",
  pointMark: "1.2500",
  originStamp: "fixture://fuel-index/",
}

function IndexSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_INDEX)
  const persist = useMutation({
    mutationFn: () => persistIndexMark(indexWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_INDEX })
      void cache.invalidateQueries({ queryKey: ["index-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-fuel-index="index-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Indeks FSC/BAF/CAF jako dana Decimal. Przeliczenie na `/charges` zostaje leftover. Marża
        zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj indeksu
        <select
          aria-label="Rodzaj indeksu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindToken}
          onChange={(change) => setDraft({ ...draft, kindToken: change.target.value })}
        >
          <option value="fsc">fsc</option>
          <option value="baf">baf</option>
          <option value="caf">caf</option>
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Data publikacji
        <input
          aria-label="Data publikacji"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          type="date"
          value={draft.dayStamp}
          onChange={(change) => setDraft({ ...draft, dayStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Wartość indeksu
        <input
          aria-label="Wartość indeksu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.pointMark}
          onChange={(change) => setDraft({ ...draft, pointMark: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Pochodzenie zapisu indeksu paliwowego
        <input
          aria-label="Pochodzenie zapisu indeksu paliwowego"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz indeks paliwowy
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function IndexRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["index-marks", args.organizationId],
    queryFn: listIndexMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-fuel-index="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="flex flex-wrap items-baseline gap-2 font-mono">
            <span>{row.index_kind}</span>
            <span>{row.published_on}</span>
            <span>{row.index_value}</span>
          </li>
        ))}
      </ul>
    </>
  )
}

export function IndexMarkPanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <IndexSave organizationId={args.organizationId} />
      <IndexRows organizationId={args.organizationId} />
    </>
  )
}
