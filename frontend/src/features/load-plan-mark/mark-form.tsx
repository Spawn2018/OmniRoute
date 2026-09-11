import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildLoadPlanMarkWrite, saveLoadPlanMark } from "@/lib/load-plan-marks-api"

const KINDS = ["axes", "tunnel", "other"] as const

export function LoadPlanMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("load_axes_01")
  const [kind, setKind] = useState<string>("axes")
  const [origin, setOrigin] = useState("fixture://load-plan-mark/")
  const save = useMutation({
    mutationFn: () => saveLoadPlanMark(buildLoadPlanMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("load_axes_01")
      setKind("axes")
      setOrigin("fixture://load-plan-mark/")
      void cache.invalidateQueries({ queryKey: ["load-plan-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-load-plan-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik planu załadunku jako katalog HITL. Rodzaj to dana, nie solver OR i nie osie Decimal.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika planu załadunku"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj postawy</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="load-plan-stance"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://load-plan-mark/…)"
        ariaLabel="Pochodzenie znacznika planu załadunku"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik planu załadunku
      </Button>
    </form>
  )
}
