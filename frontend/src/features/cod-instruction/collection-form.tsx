import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { collectionWrite, listCodMarks, persistCodMark } from "@/lib/cod-instructions-api"

const STAGES = ["noted", "advised", "collected", "refused"] as const

type MarkDraft = {
  haulToken: string
  markerToken: string
  cashStage: string
  originStamp: string
}

const EMPTY_MARK: MarkDraft = {
  haulToken: "",
  markerToken: "",
  cashStage: "noted",
  originStamp: "fixture://cod-instruction/",
}

function MarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_MARK)
  const persist = useMutation({
    mutationFn: () => persistCodMark(collectionWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_MARK })
      void cache.invalidateQueries({ queryKey: ["cod-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-cod="mark-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik pobrania na zleceniu. `collected` to status operacyjny, nie kwota. Rozliczenie
        zostaje w Fali F na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Identyfikator zlecenia pobrania
        <input
          aria-label="Identyfikator zlecenia pobrania"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.haulToken}
          onChange={(change) => setDraft({ ...draft, haulToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kod snake instrukcji COD
        <input
          aria-label="Kod snake instrukcji COD"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.markerToken}
          onChange={(change) => setDraft({ ...draft, markerToken: change.target.value })}
          required
        />
      </label>
      <fieldset className="flex flex-col gap-1 text-xs">
        <legend>Status operacyjny pobrania</legend>
        {STAGES.map((stage) => (
          <label key={stage} className="flex items-center gap-2">
            <input
              type="radio"
              name="cashStage"
              aria-label={`Status operacyjny ${stage}`}
              checked={draft.cashStage === stage}
              onChange={() => setDraft({ ...draft, cashStage: stage })}
            />
            {stage}
          </label>
        ))}
      </fieldset>
      <label className="flex flex-col gap-1 text-xs">
        Pochodzenie zapisu pobrania
        <input
          aria-label="Pochodzenie zapisu pobrania"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz instrukcję pobrania
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function MarkRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["cod-marks", args.organizationId],
    queryFn: listCodMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-cod="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="flex flex-wrap gap-2 font-mono">
            <span>{row.instruction_code}</span>
            <span>{row.collection_status}</span>
            <Link className="underline" to="/shipments">
              zlecenie
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}

export function CollectionMarkPanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <MarkSave organizationId={args.organizationId} />
      <MarkRows organizationId={args.organizationId} />
    </>
  )
}
