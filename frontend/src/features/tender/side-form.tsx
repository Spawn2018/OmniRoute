import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listBoardMarks, persistSideMark, sideWrite } from "@/lib/tenders-api"

type SideDraft = {
  sideStamp: string
  kindStamp: string
  statusStamp: string
  buyerStamp: string
  untilStamp: string
  termStamp: string
  tradeStamp: string
  placeStamp: string
  originStamp: string
}

const EMPTY_SIDE: SideDraft = {
  sideStamp: "sell",
  kindStamp: "open",
  statusStamp: "draft",
  buyerStamp: "",
  untilStamp: "2026-12-31",
  termStamp: "FOB",
  tradeStamp: "export",
  placeStamp: "Gdynia",
  originStamp: "fixture://tender/",
}

function SideSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_SIDE)
  const persist = useMutation({
    mutationFn: () => persistSideMark(sideWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_SIDE })
      void cache.invalidateQueries({ queryKey: ["board-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-tender="side-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Nagłówek przetargu jako dane. Loty i auto-award zostają leftover. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Strona
        <input
          aria-label="Strona przetargu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.sideStamp}
          onChange={(change) => setDraft({ ...draft, sideStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj
        <input
          aria-label="Rodzaj przetargu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindStamp}
          onChange={(change) => setDraft({ ...draft, kindStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Status
        <input
          aria-label="Status przetargu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.statusStamp}
          onChange={(change) => setDraft({ ...draft, statusStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Nabywca (party_id)
        <input
          aria-label="Identyfikator nabywcy przetargu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.buyerStamp}
          onChange={(change) => setDraft({ ...draft, buyerStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Termin
        <input
          aria-label="Termin przetargu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          type="date"
          value={draft.untilStamp}
          onChange={(change) => setDraft({ ...draft, untilStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Incoterm
        <input
          aria-label="Incoterm przetargu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.termStamp}
          onChange={(change) => setDraft({ ...draft, termStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Strona handlu
        <input
          aria-label="Strona handlu przetargu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.tradeStamp}
          onChange={(change) => setDraft({ ...draft, tradeStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Miejsce
        <input
          aria-label="Miejsce nazwane przetargu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.placeStamp}
          onChange={(change) => setDraft({ ...draft, placeStamp: change.target.value })}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://tender/…)"
        ariaLabel="Pochodzenie zapisu przetargu"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz przetarg
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function BoardRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["board-marks", args.organizationId],
    queryFn: listBoardMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.side} · {row.kind} · {row.status} · do {row.deadline_at}
          </li>
        ))}
      </ul>
    </>
  )
}

export function SidePanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <SideSave organizationId={args.organizationId} />
      <BoardRows organizationId={args.organizationId} />
    </div>
  )
}
