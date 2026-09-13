import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listTwinMarks, persistTwinMark, twinWrite } from "@/lib/twin-marks-api"

type TwinDraft = {
  kindStamp: string
  originStamp: string
}

const EMPTY_TWIN: TwinDraft = {
  kindStamp: "vehicle",
  originStamp: "fixture://twin-mark/",
}

function TwinSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_TWIN)
  const persist = useMutation({
    mutationFn: () => persistTwinMark(twinWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_TWIN })
      void cache.invalidateQueries({ queryKey: ["twin-stamps", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-twin-mark="kind-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Rodzaj ze słownika `twin_kind` (snake). To nie jest silnik fizyki i nie `plan_snapshot`.
        Marża zostaje na `/charges`.
      </p>
      <label className="text-xs">
        twin_kind
        <input
          aria-label="twin_kind open dict"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setDraft({ ...draft, kindStamp: e.target.value })}
          required
          value={draft.kindStamp}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://twin-mark/…)"
        ariaLabel="source_ref bliźniaka"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz bliźniaka
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function TwinRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["twin-stamps", args.organizationId],
    queryFn: listTwinMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  const rows = listed.data ?? []
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-twin-mark="rows" className="flex flex-col gap-1 text-xs">
        {rows.map((row) => (
          <li key={row.id} className="font-mono" data-twin-kind={row.twin_kind}>
            {row.twin_kind} · {row.source_ref}
          </li>
        ))}
      </ul>
    </>
  )
}

export function TwinPanel(args: { organizationId: string | null }) {
  return (
    <div className="flex flex-col gap-8 xl:flex-row">
      <TwinSave organizationId={args.organizationId} />
      <TwinRows organizationId={args.organizationId} />
    </div>
  )
}
