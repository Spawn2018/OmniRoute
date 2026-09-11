import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefHintField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listPartyDocMarks, partyDocWrite, persistPartyDocMark } from "@/lib/party-documents-api"

type PartyDocDraft = {
  partyStamp: string
  kindStamp: string
  originStamp: string
}

const EMPTY_PAPER: PartyDocDraft = {
  partyStamp: "",
  kindStamp: "ocp",
  originStamp: "fixture://party-document/",
}

function PartyDocSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_PAPER)
  const persist = useMutation({
    mutationFn: () => persistPartyDocMark(partyDocWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_PAPER })
      void cache.invalidateQueries({ queryKey: ["party-doc-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-party-document="paper-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Rodzaj dokumentu przy kontrahencie. Blokada 409 na zleceniu zostaje leftover. Marża zostaje
        na `/charges`. Nie ma tu extractu ani bajtów.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kontrahent (party_id)
        <input
          aria-label="Identyfikator kontrahenta dokumentu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.partyStamp}
          onChange={(change) => setDraft({ ...draft, partyStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj dokumentu (snake)
        <input
          aria-label="Rodzaj dokumentu kontrahenta"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindStamp}
          onChange={(change) => setDraft({ ...draft, kindStamp: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefHintField
        hint="source_ref: tenant:manual albo fixture://party-document/…"
        ariaLabel="source_ref dokumentu kontrahenta"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz dokument kontrahenta
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function PartyDocRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["party-doc-marks", args.organizationId],
    queryFn: listPartyDocMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-party-document="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.document_kind}
          </li>
        ))}
      </ul>
    </>
  )
}

export function PartyDocPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <PartyDocSave organizationId={args.organizationId} />
      <PartyDocRows organizationId={args.organizationId} />
    </div>
  )
}
