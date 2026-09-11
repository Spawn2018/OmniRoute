import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefHintField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listSchemeMarks, persistSchemeMark, schemeWrite } from "@/lib/monitoring-schemes-api"

type SchemeDraft = {
  codeStamp: string
  originStamp: string
}

const EMPTY_SCHEME: SchemeDraft = {
  codeStamp: "sent",
  originStamp: "fixture://monitoring-scheme/",
}

function SchemeSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_SCHEME)
  const persist = useMutation({
    mutationFn: () => persistSchemeMark(schemeWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_SCHEME })
      void cache.invalidateQueries({ queryKey: ["scheme-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-monitoring-scheme="scheme-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Kod schematu monitoringu tenanta. Zgłoszenie SENT i live PUESC zostają leftover. Marża zostaje
        na `/charges`. Nie ma tu fetcha do urzędu.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kod schematu (snake)
        <input
          aria-label="Kod schematu monitoringu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.codeStamp}
          onChange={(change) => setDraft({ ...draft, codeStamp: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefHintField
        hint="source_ref: tenant:manual albo fixture://monitoring-scheme/…"
        ariaLabel="source_ref schematu monitoringu"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz schemat monitoringu
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function SchemeRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["scheme-marks", args.organizationId],
    queryFn: listSchemeMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-monitoring-scheme="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.scheme_code}
          </li>
        ))}
      </ul>
    </>
  )
}

export function SchemePanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <SchemeSave organizationId={args.organizationId} />
      <SchemeRows organizationId={args.organizationId} />
    </div>
  )
}
