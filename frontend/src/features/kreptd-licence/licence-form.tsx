import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { kreptdWrite, listKreptdMarks, persistKreptdMark } from "@/lib/kreptd-licences-api"

type KreptdDraft = {
  partyStamp: string
  licenceStamp: string
  originStamp: string
}

const EMPTY_KREPTD: KreptdDraft = {
  partyStamp: "",
  licenceStamp: "GITD-12345678",
  originStamp: "fixture://kreptd-licence/",
}

function KreptdSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_KREPTD)
  const persist = useMutation({
    mutationFn: () => persistKreptdMark(kreptdWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_KREPTD })
      void cache.invalidateQueries({ queryKey: ["kreptd-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-kreptd-licence="licence-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Numer licencji KREPTD przy kontrahencie. Citizen API i scrape zostają leftover. Marża zostaje
        na `/charges`. Nie ma tu fetcha do kreptd.gitd.gov.pl.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kontrahent (party_id)
        <input
          aria-label="Identyfikator kontrahenta licencji KREPTD"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.partyStamp}
          onChange={(change) => setDraft({ ...draft, partyStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Numer licencji KREPTD
        <input
          aria-label="Numer licencji KREPTD"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.licenceStamp}
          onChange={(change) => setDraft({ ...draft, licenceStamp: change.target.value })}
          required
        />
      </label>
      <p className="text-xs text-muted-foreground">
        source_ref: tenant:manual albo fixture://kreptd-licence/…
      </p>
      <input
        aria-label="source_ref licencji KREPTD"
        className="h-9 max-w-lg rounded-md border bg-background px-2 font-mono text-xs"
        value={draft.originStamp}
        onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
        required
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz licencję KREPTD
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function KreptdRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["kreptd-marks", args.organizationId],
    queryFn: listKreptdMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-kreptd-licence="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.licence_no}
          </li>
        ))}
      </ul>
    </>
  )
}

export function KreptdPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <KreptdSave organizationId={args.organizationId} />
      <KreptdRows organizationId={args.organizationId} />
    </div>
  )
}
