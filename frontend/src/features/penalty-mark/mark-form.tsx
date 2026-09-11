import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildPenaltyMarkWrite, savePenaltyMark } from "@/lib/penalty-marks-api"

const KINDS = ["otif", "delay", "damage", "other"] as const

export function PenaltyMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("otif_breach_01")
  const [kind, setKind] = useState<string>("otif")
  const [origin, setOrigin] = useState("fixture://penalty-mark/")
  const save = useMutation({
    mutationFn: () => savePenaltyMark(buildPenaltyMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("otif_breach_01")
      setKind("otif")
      setOrigin("fixture://penalty-mark/")
      void cache.invalidateQueries({ queryKey: ["penalty-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-penalty-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik naruszenia kary jako katalog HITL. Rodzaj to dana, nie kara SQL i nie
        druga marża.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika kary"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj naruszenia</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="penalty-breach"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://penalty-mark/…)"
        ariaLabel="Pochodzenie znacznika kary"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik kary
      </Button>
    </form>
  )
}
