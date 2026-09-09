import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { carbonWrite, listCarbonMarks, persistCarbonMark } from "@/lib/tender-carbon-marks-api"

type CarbonDraft = {
  boardStamp: string
  markStamp: string
  originStamp: string
}

const EMPTY_CARBON: CarbonDraft = {
  boardStamp: "",
  markStamp: "declared",
  originStamp: "fixture://tender-carbon-mark/",
}

function CarbonSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_CARBON)
  const persist = useMutation({
    mutationFn: () => persistCarbonMark(carbonWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_CARBON })
      void cache.invalidateQueries({ queryKey: ["carbon-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-tender-carbon-mark="mark-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik declared/exempt przy nagłówku. Kilogramy i CBAM zostają leftover. Status nagłówka nie
        zmienia się tu. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Przetarg (tender_id)
        <input
          aria-label="Identyfikator przetargu znacznika śladu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardStamp}
          onChange={(change) => setDraft({ ...draft, boardStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Znacznik śladu
        <select
          aria-label="Znacznik declared exempt"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.markStamp}
          onChange={(change) => setDraft({ ...draft, markStamp: change.target.value })}
          required
        >
          <option value="declared">declared</option>
          <option value="exempt">exempt</option>
        </select>
      </label>
      <p className="text-xs text-muted-foreground">source_ref: tenant:manual albo fixture://tender-carbon-mark/…</p>
      <input
        aria-label="source_ref znacznika śladu"
        className="h-9 max-w-lg rounded-md border bg-background px-2 font-mono text-xs"
        value={draft.originStamp}
        onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
        required
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz znacznik śladu
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function CarbonRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["carbon-marks", args.organizationId],
    queryFn: listCarbonMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-carbon-mark="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.mark_code}
          </li>
        ))}
      </ul>
    </>
  )
}

export function CarbonPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <CarbonSave organizationId={args.organizationId} />
      <CarbonRows organizationId={args.organizationId} />
    </div>
  )
}
