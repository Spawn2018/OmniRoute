import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildBondedMarkWrite, saveBondedMark } from "@/lib/bonded-marks-api"

const KINDS = ["bonded", "recognized", "other"] as const

export function BondedMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("bond_01")
  const [kind, setKind] = useState<string>("bonded")
  const [origin, setOrigin] = useState("fixture://bonded-mark/")
  const save = useMutation({
    mutationFn: () => saveBondedMark(buildBondedMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("bond_01")
      setKind("bonded")
      setOrigin("fixture://bonded-mark/")
      void cache.invalidateQueries({ queryKey: ["bonded-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-bonded-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik bonded / miejsce uznane jako katalog HITL. Rodzaj to dana, nie WMS i nie procedura live.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika bonded"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj bonded</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="bonded-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://bonded-mark/…)"
        ariaLabel="Pochodzenie znacznika bonded"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik bonded
      </Button>
    </form>
  )
}
