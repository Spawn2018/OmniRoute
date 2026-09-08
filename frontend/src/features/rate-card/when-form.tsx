import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { listWhenMarks, persistWhenMark, whenWrite } from "@/lib/rate-cards-api"

type WhenDraft = {
  codeToken: string
  whenToken: string
  cashMark: string
  ccyMark: string
  originStamp: string
}

const EMPTY_WHEN: WhenDraft = {
  codeToken: "weekend",
  whenToken: "sobota",
  cashMark: "10.5000",
  ccyMark: "EUR",
  originStamp: "fixture://rate-card/",
}

function WhenSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_WHEN)
  const persist = useMutation({
    mutationFn: () => persistWhenMark(whenWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_WHEN })
      void cache.invalidateQueries({ queryKey: ["when-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-rate-card="when-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Warunek `applies_when` jako dana i kwota Decimal. Matching WHEN/IF zostaje leftover.
        Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kod snake karty
        <input
          aria-label="Kod snake karty"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.codeToken}
          onChange={(change) => setDraft({ ...draft, codeToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Warunek applies_when
        <input
          aria-label="Warunek applies_when"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.whenToken}
          onChange={(change) => setDraft({ ...draft, whenToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kwota karty
        <input
          aria-label="Kwota karty"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.cashMark}
          onChange={(change) => setDraft({ ...draft, cashMark: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Waluta ISO karty
        <input
          aria-label="Waluta ISO karty"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.ccyMark}
          onChange={(change) => setDraft({ ...draft, ccyMark: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Pochodzenie zapisu karty stawek
        <input
          aria-label="Pochodzenie zapisu karty stawek"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz kartę stawek
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function WhenRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["when-marks", args.organizationId],
    queryFn: listWhenMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-rate-card="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="flex flex-wrap items-baseline gap-2 font-mono">
            <span>{row.card_code}</span>
            <span>{row.applies_when}</span>
            <Money amount={row.amount} currency={row.currency} />
          </li>
        ))}
      </ul>
    </>
  )
}

export function WhenTokenPanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <WhenSave organizationId={args.organizationId} />
      <WhenRows organizationId={args.organizationId} />
    </>
  )
}
