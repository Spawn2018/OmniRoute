import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildLcChecklistWrite, saveLcChecklist } from "@/lib/lc-checklists-api"

const KINDS = ["open", "presented", "closed", "other"] as const

export function LcChecklistSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("lc_acme_01")
  const [kind, setKind] = useState<string>("open")
  const [origin, setOrigin] = useState("fixture://lc-checklist/")
  const save = useMutation({
    mutationFn: () => saveLcChecklist(buildLcChecklistWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("lc_acme_01")
      setKind("open")
      setOrigin("fixture://lc-checklist/")
      void cache.invalidateQueries({ queryKey: ["lc-checklists", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-lc-checklist="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Checklista LC jako katalog HITL. Status to dana, nie bank live i nie termin due.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod checklisty LC"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Status checklisty</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="lc-status"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://lc-checklist/…)"
        ariaLabel="Pochodzenie checklisty LC"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz checklistę LC
      </Button>
    </form>
  )
}
