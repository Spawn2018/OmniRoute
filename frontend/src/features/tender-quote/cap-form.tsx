import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { capWrite, listBidMarks, persistCapMark } from "@/lib/tender-quotes-api"

type CapDraft = {
  quoteStamp: string
  untilStamp: string
  capCount: string
  originStamp: string
}

const EMPTY_CAP: CapDraft = {
  quoteStamp: "",
  untilStamp: "2026-12-31",
  capCount: "3",
  originStamp: "fixture://tender-quote/",
}

function CapSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_CAP)
  const persist = useMutation({
    mutationFn: () => persistCapMark(capWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_CAP })
      void cache.invalidateQueries({ queryKey: ["bid-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-tender-quote="cap-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Ważność i limit zleceń z oferty jako dane. Auto-award i obiekt przetargu G2 zostają leftover.
        Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Wycena (quotation_id)
        <input
          aria-label="Identyfikator wyceny oferty przetargowej"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.quoteStamp}
          onChange={(change) => setDraft({ ...draft, quoteStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Ważna do
        <input
          aria-label="Data ważności oferty przetargowej"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          type="date"
          value={draft.untilStamp}
          onChange={(change) => setDraft({ ...draft, untilStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Limit orderów
        <input
          aria-label="Limit orderów oferty przetargowej"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.capCount}
          onChange={(change) => setDraft({ ...draft, capCount: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://tender-quote/…)"
        ariaLabel="Pochodzenie zapisu oferty przetargowej"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz ofertę przetargową
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function BidRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["bid-marks", args.organizationId],
    queryFn: listBidMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-quote="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.quotation_id} · do {row.valid_until} · limit {row.order_limit}
          </li>
        ))}
      </ul>
    </>
  )
}

export function CapPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <CapSave organizationId={args.organizationId} />
      <BidRows organizationId={args.organizationId} />
    </div>
  )
}
