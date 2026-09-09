import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listStanceMarks, persistStanceMark, stanceWrite } from "@/lib/tender-bid-stances-api"

type StanceDraft = {
  boardStamp: string
  stanceStamp: string
  originStamp: string
}

const EMPTY_STANCE: StanceDraft = {
  boardStamp: "",
  stanceStamp: "bid",
  originStamp: "fixture://tender-bid-stance/",
}

function StanceSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_STANCE)
  const persist = useMutation({
    mutationFn: () => persistStanceMark(stanceWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_STANCE })
      void cache.invalidateQueries({ queryKey: ["stance-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-tender-bid-stance="stance-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Postawa przy nagłówku. Wynik win/loss i four-eyes zostają leftover. Status nagłówka nie
        zmienia się tu. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Przetarg (tender_id)
        <input
          aria-label="Identyfikator przetargu postawy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardStamp}
          onChange={(change) => setDraft({ ...draft, boardStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Postawa
        <select
          aria-label="Postawa bid no_bid"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.stanceStamp}
          onChange={(change) => setDraft({ ...draft, stanceStamp: change.target.value })}
          required
        >
          <option value="bid">bid</option>
          <option value="no_bid">no_bid</option>
        </select>
      </label>
      <p className="text-xs text-muted-foreground">source_ref: tenant:manual albo fixture://tender-bid-stance/…</p>
      <input
        aria-label="source_ref postawy udziału"
        className="h-9 max-w-lg rounded-md border bg-background px-2 font-mono text-xs"
        value={draft.originStamp}
        onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
        required
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz udział
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function StanceRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["stance-marks", args.organizationId],
    queryFn: listStanceMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-bid-stance="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.stance_code}
          </li>
        ))}
      </ul>
    </>
  )
}

export function StancePanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <StanceSave organizationId={args.organizationId} />
      <StanceRows organizationId={args.organizationId} />
    </div>
  )
}
