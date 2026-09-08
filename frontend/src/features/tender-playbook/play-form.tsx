import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listPlayMarks, persistPlayMark, playWrite } from "@/lib/tender-playbooks-api"

type PlayDraft = {
  boardStamp: string
  thesisStamp: string
  bodyStamp: string
  originStamp: string
}

const EMPTY_PLAY: PlayDraft = {
  boardStamp: "",
  thesisStamp: "incoterm_fob",
  bodyStamp: "tylko FOB",
  originStamp: "fixture://tender-playbook/",
}

function PlaySave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_PLAY)
  const persist = useMutation({
    mutationFn: () => persistPlayMark(playWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_PLAY })
      void cache.invalidateQueries({ queryKey: ["play-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-tender-playbook="play-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Teza playbooka przy nagłówku. Extract RFP i win/loss zostają leftover. Marża zostaje na
        `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Przetarg (tender_id)
        <input
          aria-label="Identyfikator przetargu playbooka"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardStamp}
          onChange={(change) => setDraft({ ...draft, boardStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kod tezy
        <input
          aria-label="Kod snake tezy playbooka"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.thesisStamp}
          onChange={(change) => setDraft({ ...draft, thesisStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Twierdzenie
        <textarea
          aria-label="Treść twierdzenia playbooka"
          className="min-h-20 rounded-md border bg-background px-2 py-1 font-mono text-[13px]"
          value={draft.bodyStamp}
          onChange={(change) => setDraft({ ...draft, bodyStamp: change.target.value })}
          required
        />
      </label>
      <aside className="space-y-1">
        <p className="text-xs font-medium">Pochodzenie tezy playbooka</p>
        <input
          aria-label="Pochodzenie zapisu playbooka"
          autoComplete="off"
          className="h-9 w-full rounded-md border bg-background px-2 font-mono text-[13px]"
          name="playbook-origin"
          spellCheck={false}
          value={draft.originStamp}
          onChange={(event) => {
            const originStamp = event.target.value
            setDraft((current) => ({ ...current, originStamp }))
          }}
          required
        />
      </aside>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz tezę
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function PlayRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["play-marks", args.organizationId],
    queryFn: listPlayMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-playbook="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.claim_code} · {row.claim_text}
          </li>
        ))}
      </ul>
    </>
  )
}

export function PlayPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <PlaySave organizationId={args.organizationId} />
      <PlayRows organizationId={args.organizationId} />
    </div>
  )
}
