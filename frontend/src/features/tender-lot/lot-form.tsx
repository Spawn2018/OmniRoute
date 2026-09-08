import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listLotMarks, lotWrite, persistLotMark } from "@/lib/tender-lots-api"

type LotDraft = {
  boardStamp: string
  codeStamp: string
  originStamp: string
}

const EMPTY_LOT: LotDraft = {
  boardStamp: "",
  codeStamp: "LOT-1",
  originStamp: "fixture://tender-lot/",
}

function LotSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_LOT)
  const persist = useMutation({
    mutationFn: () => persistLotMark(lotWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_LOT })
      void cache.invalidateQueries({ queryKey: ["lot-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-tender-lot="lot-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Kod partii na nagłówku przetargu. Korytarz i auto-award zostają leftover. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Przetarg (tender_id)
        <input
          aria-label="Identyfikator przetargu partii"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardStamp}
          onChange={(change) => setDraft({ ...draft, boardStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kod partii
        <input
          aria-label="Kod partii przetargu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.codeStamp}
          onChange={(change) => setDraft({ ...draft, codeStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Pochodzenie zapisu partii
        <input
          aria-label="Pochodzenie zapisu partii przetargu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz partię
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function LotRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["lot-marks", args.organizationId],
    queryFn: listLotMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-lot="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.tender_id} · {row.lot_code}
          </li>
        ))}
      </ul>
    </>
  )
}

export function LotPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <LotSave organizationId={args.organizationId} />
      <LotRows organizationId={args.organizationId} />
    </div>
  )
}
