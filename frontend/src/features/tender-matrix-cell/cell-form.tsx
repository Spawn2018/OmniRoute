import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { cellWrite, listCellMarks, persistCellMark } from "@/lib/tender-matrix-cells-api"

type CellDraft = {
  boardStamp: string
  codeStamp: string
  cashStamp: string
  ccyStamp: string
  originStamp: string
}

const EMPTY_CELL: CellDraft = {
  boardStamp: "",
  codeStamp: "ocean_fcl",
  cashStamp: "10.5000",
  ccyStamp: "EUR",
  originStamp: "fixture://tender-matrix-cell/",
}

function CellSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_CELL)
  const persist = useMutation({
    mutationFn: () => persistCellMark(cellWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_CELL })
      void cache.invalidateQueries({ queryKey: ["cell-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-tender-matrix-cell="cell-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Kwota z P jako dana. Mapowanie kolumn Excel i extract RFP zostają leftover. Marża zostaje
        na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Przetarg (tender_id)
        <input
          aria-label="Identyfikator przetargu komórki matrycy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardStamp}
          onChange={(change) => setDraft({ ...draft, boardStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kod komórki
        <input
          aria-label="Kod snake komórki matrycy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.codeStamp}
          onChange={(change) => setDraft({ ...draft, codeStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kwota z P
        <input
          aria-label="Kwota komórki matrycy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          inputMode="decimal"
          value={draft.cashStamp}
          onChange={(change) => setDraft({ ...draft, cashStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Waluta ISO komórki
        <input
          aria-label="Waluta ISO komórki matrycy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.ccyStamp}
          onChange={(change) => setDraft({ ...draft, ccyStamp: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://tender-matrix-cell/…)"
        ariaLabel="Pochodzenie zapisu komórki matrycy"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz komórkę
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function CellRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["cell-marks", args.organizationId],
    queryFn: listCellMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-matrix-cell="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="flex flex-wrap items-baseline gap-2 font-mono">
            <span>{row.cell_code}</span>
            <Money amount={row.amount} currency={row.currency} />
          </li>
        ))}
      </ul>
    </>
  )
}

export function CellPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <CellSave organizationId={args.organizationId} />
      <CellRows organizationId={args.organizationId} />
    </div>
  )
}
