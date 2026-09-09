import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { briefWrite, listExecutiveMarks, persistBriefMark } from "@/lib/executive-marks-api"

type AskDraft = {
  askKind: string
  originRef: string
}

const BLANK_ASK: AskDraft = {
  askKind: "loss",
  originRef: "fixture://executive-mark/",
}

const ASKS = [
  { token: "loss", caption: "strata" },
  { token: "lane", caption: "korytarz" },
  { token: "risk", caption: "ryzyko" },
  { token: "cash", caption: "gotówka" },
  { token: "other", caption: "inne" },
] as const

function BriefComposer(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(BLANK_ASK)
  const persist = useMutation({
    mutationFn: () => persistBriefMark(briefWrite(draft)),
    onSuccess: () => {
      setDraft({ ...BLANK_ASK })
      void cache.invalidateQueries({ queryKey: ["board-ask-stamps", args.organizationId] })
    },
  })
  return (
    <form
      className="space-y-3 max-w-md"
      data-executive-mark="kind-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId && !persist.isPending) persist.mutate()
      }}
    >
      <p className="text-sm text-muted-foreground">
        Pięć pytań zarządu (strata, korytarz, ryzyko, gotówka, inne).
        To nie jest suma z modelu i nie zdania z agregatów. Marża zostaje na `/charges`.
      </p>
      <fieldset className="space-y-2">
        <legend className="text-sm">Rodzaj pytania (allowlista)</legend>
        {ASKS.map((ask) => (
          <label key={ask.token} className="flex items-baseline gap-2 text-sm">
            <input
              type="radio"
              name="exec-question-kind"
              aria-label={`Pytanie ${ask.caption}`}
              checked={draft.askKind === ask.token}
              onChange={() => setDraft({ ...draft, askKind: ask.token })}
              value={ask.token}
            />
            <code>{ask.token}</code>
            <em className="not-italic text-muted-foreground">{ask.caption}</em>
          </label>
        ))}
      </fieldset>
      <label className="grid gap-1 text-sm">
        Pochodzenie zapisu
        <input
          aria-label="source_ref pytania zarządu"
          className="h-9 rounded-md border bg-background px-2 font-mono text-xs"
          value={draft.originRef}
          onChange={(change) => setDraft({ ...draft, originRef: change.target.value })}
          placeholder="tenant:manual albo fixture://executive-mark/…"
          required
        />
      </label>
      <Button type="submit" disabled={!args.organizationId || persist.isPending}>
        Zapisz pytanie zarządu
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function BriefShelf(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["board-ask-stamps", args.organizationId],
    queryFn: listExecutiveMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  const rows = listed.data ?? []
  return (
    <div>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <dl data-executive-mark="rows" className="grid gap-x-4 gap-y-1 text-sm sm:grid-cols-[auto_1fr]">
        {rows.map((row) => (
          <div key={row.id} className="contents">
            <dt className="font-mono" data-question-kind={row.question_kind}>
              {row.question_kind}
            </dt>
            <dd className="font-mono text-muted-foreground">{row.source_ref}</dd>
          </div>
        ))}
      </dl>
    </div>
  )
}

export function BriefStage(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-8 md:grid-cols-2">
      <BriefComposer organizationId={args.organizationId} />
      <BriefShelf organizationId={args.organizationId} />
    </div>
  )
}
