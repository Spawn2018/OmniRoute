import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildYardMarkWrite, saveYardMark } from "@/lib/yard-marks-api"

const KINDS = ["yard_slot", "weigh", "eir", "other"] as const

export function YardMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("yard_slot_01")
  const [kind, setKind] = useState<string>("yard_slot")
  const [origin, setOrigin] = useState("fixture://yard-mark/")
  const save = useMutation({
    mutationFn: () => saveYardMark(buildYardMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("yard_slot_01")
      setKind("yard_slot")
      setOrigin("fixture://yard-mark/")
      void cache.invalidateQueries({ queryKey: ["yard-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-yard-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Yard / waga / EIR jako katalog HITL. Rodzaj to dana, nie live yard i nie kg.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika yard"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj yard</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="yard-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://yard-mark/…)"
        ariaLabel="Pochodzenie znacznika yard"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz yard
      </Button>
    </form>
  )
}
