import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildRoutePlanMarkWrite, saveRoutePlanMark } from "@/lib/route-plan-marks-api"

const KINDS = ["route", "stop", "window", "other"] as const

export function RoutePlanMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("route_gdn_osl")
  const [kind, setKind] = useState<string>("route")
  const [origin, setOrigin] = useState("fixture://route-plan-mark/")
  const save = useMutation({
    mutationFn: () => saveRoutePlanMark(buildRoutePlanMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("route_gdn_osl")
      setKind("route")
      setOrigin("fixture://route-plan-mark/")
      void cache.invalidateQueries({ queryKey: ["route-plan-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-route-plan-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik planu trasy jako katalog HITL. Rodzaj to dana, nie Valhalla i nie km.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika planu trasy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj planu</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="route-plan-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://route-plan-mark/…)"
        ariaLabel="Pochodzenie znacznika planu trasy"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik planu trasy
      </Button>
    </form>
  )
}
