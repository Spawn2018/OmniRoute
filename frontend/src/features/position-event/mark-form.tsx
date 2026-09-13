import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildPositionEventWrite, savePositionEvent } from "@/lib/position-events-api"

const KINDS = ["gps", "manual", "other"] as const

export function PositionEventSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("pos_yard_01")
  const [kind, setKind] = useState<string>("gps")
  const [origin, setOrigin] = useState("fixture://position-event/")
  const save = useMutation({
    mutationFn: () => savePositionEvent(buildPositionEventWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("pos_yard_01")
      setKind("gps")
      setOrigin("fixture://position-event/")
      void cache.invalidateQueries({ queryKey: ["position-events", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-position-event="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Zdarzenie pozycji jako katalog HITL. Rodzaj źródła to dana, nie live poll i nie mapa.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod zdarzenia pozycji"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj źródła</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="position-event-source"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://position-event/…)"
        ariaLabel="Pochodzenie zdarzenia pozycji"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz zdarzenie pozycji
      </Button>
    </form>
  )
}
