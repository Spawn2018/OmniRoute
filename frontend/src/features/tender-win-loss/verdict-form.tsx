import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listVerdictMarks, persistVerdictMark, verdictWrite } from "@/lib/tender-win-losses-api"

type VerdictDraft = {
  boardStamp: string
  resultStamp: string
  whyStamp: string
  originStamp: string
}

const EMPTY_VERDICT: VerdictDraft = {
  boardStamp: "",
  resultStamp: "won",
  whyStamp: "price",
  originStamp: "fixture://tender-win-loss/",
}

function VerdictSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_VERDICT)
  const persist = useMutation({
    mutationFn: () => persistVerdictMark(verdictWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_VERDICT })
      void cache.invalidateQueries({ queryKey: ["verdict-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-tender-win-loss="verdict-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Werdykt przy nagłówku. Extract RFP i four-eyes zostają leftover. Status nagłówka nie
        zmienia się tu. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Przetarg (tender_id)
        <input
          aria-label="Identyfikator przetargu wyniku"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardStamp}
          onChange={(change) => setDraft({ ...draft, boardStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Wynik
        <select
          aria-label="Wynik win lost no_bid"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.resultStamp}
          onChange={(change) => setDraft({ ...draft, resultStamp: change.target.value })}
          required
        >
          <option value="won">won</option>
          <option value="lost">lost</option>
          <option value="no_bid">no_bid</option>
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kod powodu
        <input
          aria-label="Kod snake powodu wyniku"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.whyStamp}
          onChange={(change) => setDraft({ ...draft, whyStamp: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://tender-win-loss/…)"
        ariaLabel="Pochodzenie zapisu wyniku przetargu"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz wynik
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function VerdictRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["verdict-marks", args.organizationId],
    queryFn: listVerdictMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-win-loss="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.outcome} · {row.reason_code}
          </li>
        ))}
      </ul>
    </>
  )
}

export function VerdictPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <VerdictSave organizationId={args.organizationId} />
      <VerdictRows organizationId={args.organizationId} />
    </div>
  )
}
