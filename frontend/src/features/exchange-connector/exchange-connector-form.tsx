import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { exchangeBoardWrite, persistExchangeConnector } from "@/lib/exchange-connectors-api"

type BoardFixtureDraft = {
  boardMark: string
  kindToken: string
  originHint: string
}

const EMPTY_BOARD: BoardFixtureDraft = {
  boardMark: "trans_eu_desk",
  kindToken: "trans_eu",
  originHint: "fixture://portal/",
}

export function ExchangeConnectorSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_BOARD)
  const persist = useMutation({
    mutationFn: () => persistExchangeConnector(exchangeBoardWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_BOARD })
      void cache.invalidateQueries({
        queryKey: ["exchange-connectors", "fixture", args.organizationId],
      })
    },
  })
  const locked = persist.isPending || args.organizationId === null
  return (
    <form
      className="grid max-w-lg gap-3"
      data-exchange-connector="fixture-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Katalog fixture giełdy: kod i kind `trans_eu`. To nie jest publiczny portal ani
        wystawienie frachtu. Serwis nie woła Trans.eu.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kod konektora giełdy (snake 2–32)
        <input
          aria-label="Kod konektora giełdy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardMark}
          onChange={(change) => setDraft({ ...draft, boardMark: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Tablica (trans_eu)
        <input
          aria-label="Kind tablicy giełdy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindToken}
          onChange={(change) => setDraft({ ...draft, kindToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        source_ref (`tenant:manual` albo `fixture://portal/…`)
        <input
          required
          aria-label="source_ref konektora giełdy"
          className="h-9 rounded-md border border-input bg-background px-3 font-mono text-sm"
          value={draft.originHint}
          onChange={(ev) => setDraft({ ...draft, originHint: ev.target.value })}
        />
      </label>
      <div>
        <Button type="submit" disabled={locked}>
          Zapisz konektor giełdy
        </Button>
      </div>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}
