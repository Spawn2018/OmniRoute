import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listMethodMarks, methodWrite, persistMethodMark } from "@/lib/carbon-methods-api"

type MethodDraft = {
  codeStamp: string
  versionStamp: string
  originStamp: string
}

const EMPTY_METHOD: MethodDraft = {
  codeStamp: "glec",
  versionStamp: "2023",
  originStamp: "fixture://carbon-method/",
}

function MethodSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_METHOD)
  const persist = useMutation({
    mutationFn: () => persistMethodMark(methodWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_METHOD })
      void cache.invalidateQueries({ queryKey: ["method-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-carbon-method="method-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Metodyka GLEC/GHG tenanta plus wersja. Kg, CBAM i kalkulator zostają leftover. Marża zostaje
        na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kod metodyki (snake)
        <input
          aria-label="Kod metodyki CO₂"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.codeStamp}
          onChange={(change) => setDraft({ ...draft, codeStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Wersja metodyki
        <input
          aria-label="Wersja metodyki CO₂"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.versionStamp}
          onChange={(change) => setDraft({ ...draft, versionStamp: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://carbon-method/…)"
        ariaLabel="source_ref metodyki CO₂"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz metodykę CO₂
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function MethodRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["method-marks", args.organizationId],
    queryFn: listMethodMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-carbon-method="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.method_code} {row.method_version}
          </li>
        ))}
      </ul>
    </>
  )
}

export function MethodPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <MethodSave organizationId={args.organizationId} />
      <MethodRows organizationId={args.organizationId} />
    </div>
  )
}
