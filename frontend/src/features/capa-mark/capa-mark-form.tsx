import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildCapaWrite, saveCapaMark } from "@/lib/capa-marks-api"

const KINDS = ["capa", "eight_d", "recurrence"] as const

export function CapaMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("capa_pl_01")
  const [kind, setKind] = useState<string>("capa")
  const [origin, setOrigin] = useState("fixture://capa-mark/")
  const save = useMutation({
    mutationFn: () => saveCapaMark(buildCapaWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("capa_pl_01")
      setKind("capa")
      setOrigin("fixture://capa-mark/")
      void cache.invalidateQueries({ queryKey: ["capa-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-capa-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Rodzaj QMS jako katalog HITL. Bez workflow CAPA i bez scoringu.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika CAPA"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-1 text-xs">
        <legend>Rodzaj</legend>
        <div className="flex flex-wrap gap-3">
          {KINDS.map((token) => (
            <label key={token} className="flex items-center gap-1">
              <input
                checked={kind === token}
                name="capa-kind"
                onChange={() => setKind(token)}
                type="radio"
                value={token}
              />
              {token}
            </label>
          ))}
        </div>
      </fieldset>
      <label className="grid gap-1 text-xs">
        source_ref
        <input
          aria-label="Pochodzenie znacznika CAPA"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setOrigin(change.target.value)}
          required
          value={origin}
        />
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik CAPA
      </Button>
    </form>
  )
}
