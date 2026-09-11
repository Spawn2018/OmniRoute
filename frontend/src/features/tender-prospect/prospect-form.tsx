import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  listProspectMarks,
  persistProspectMark,
  prospectWrite,
} from "@/lib/tender-prospects-api"

type ProspectDraft = {
  boardStamp: string
  partyStamp: string
  outreachStamp: string
  originStamp: string
}

const EMPTY_PROSPECT: ProspectDraft = {
  boardStamp: "",
  partyStamp: "",
  outreachStamp: "called",
  originStamp: "fixture://tender-prospect/",
}

function ProspectSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_PROSPECT)
  const persist = useMutation({
    mutationFn: () => persistProspectMark(prospectWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_PROSPECT })
      void cache.invalidateQueries({ queryKey: ["prospect-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-tender-prospect="prospect-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Ślad outreach przy nagłówku i kontrahencie. Scrape, TED i bid/no-bid zostają leftover. Marża
        zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Przetarg (tender_id)
        <input
          aria-label="Identyfikator przetargu prospektu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.boardStamp}
          onChange={(change) => setDraft({ ...draft, boardStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kontrahent (party_id)
        <input
          aria-label="Identyfikator kontrahenta prospektu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.partyStamp}
          onChange={(change) => setDraft({ ...draft, partyStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Outreach (snake)
        <input
          aria-label="Kod outreach prospektu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.outreachStamp}
          onChange={(change) => setDraft({ ...draft, outreachStamp: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://tender-prospect/…)"
        ariaLabel="Pochodzenie zapisu prospektu przetargu"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz prospekt
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function ProspectRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["prospect-marks", args.organizationId],
    queryFn: listProspectMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tender-prospect="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.outreach_code}
          </li>
        ))}
      </ul>
    </>
  )
}

export function ProspectPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <ProspectSave organizationId={args.organizationId} />
      <ProspectRows organizationId={args.organizationId} />
    </div>
  )
}
