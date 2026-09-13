import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildSalesLaneWrite, saveSalesLane } from "@/lib/sales-lanes-api"

const KINDS = ["repeat", "spot", "other"] as const

export function SalesLaneSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("sln_repeat_01")
  const [kind, setKind] = useState<string>("repeat")
  const [origin, setOrigin] = useState("fixture://sales-lane/")
  const save = useMutation({
    mutationFn: () => saveSalesLane(buildSalesLaneWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("sln_repeat_01")
      setKind("repeat")
      setOrigin("fixture://sales-lane/")
      void cache.invalidateQueries({ queryKey: ["sales-lanes", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-sales-lane="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Korytarz sprzedaży jako katalog HITL. Rodzaj to dana, nie para miejsc i nie pipeline.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod korytarza sprzedażowego"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj korytarza</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="sales-lane-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://sales-lane/…)"
        ariaLabel="Pochodzenie korytarza sprzedażowego"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz korytarz
      </Button>
    </form>
  )
}
