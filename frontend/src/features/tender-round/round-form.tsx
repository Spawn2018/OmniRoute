import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listTurnMarks, persistRoundMark, roundWrite } from "@/lib/tender-rounds-api"

type RoundDraft = {
  boardStamp: string
  turnStamp: string
  originRef: string
}

const EMPTY_ROUND: RoundDraft = {
  boardStamp: "",
  turnStamp: "1",
  originRef: "fixture://tender-round/",
}

function RoundSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_ROUND)
  const persist = useMutation({
    mutationFn: () => persistRoundMark(roundWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_ROUND })
      void cache.invalidateQueries({ queryKey: ["turn-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-tender-round="round-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Numer rundy na nagłówku przetargu. Data room i auto-award zostają leftover. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Przetarg (tender_id)
        <input
          aria-label="Identyfikator przetargu rundy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardStamp}
          onChange={(change) => setDraft({ ...draft, boardStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Numer rundy
        <input
          aria-label="Numer rundy przetargu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          inputMode="numeric"
          value={draft.turnStamp}
          onChange={(change) => setDraft({ ...draft, turnStamp: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://tender-round/…)"
        ariaLabel="Pochodzenie zapisu rundy przetargu"
        value={draft.originRef}
        onChange={(originRef) => setDraft({ ...draft, originRef })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz rundę
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function RoundRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["turn-marks", args.organizationId],
    queryFn: listTurnMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-round="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.tender_id} · runda {row.round_no}
          </li>
        ))}
      </ul>
    </>
  )
}

export function RoundPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <RoundSave organizationId={args.organizationId} />
      <RoundRows organizationId={args.organizationId} />
    </div>
  )
}
