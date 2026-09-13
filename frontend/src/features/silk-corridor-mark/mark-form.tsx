import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildSilkCorridorMarkWrite,
  saveSilkCorridorMark,
} from "@/lib/silk-corridor-marks-api"

const KINDS = ["silk", "block_train", "transit", "other"] as const

export function SilkCorridorMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("scm_silk_01")
  const [kind, setKind] = useState<string>("silk")
  const [origin, setOrigin] = useState("fixture://silk-corridor-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveSilkCorridorMark(buildSilkCorridorMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("scm_silk_01")
      setKind("silk")
      setOrigin("fixture://silk-corridor-mark/")
      void cache.invalidateQueries({
        queryKey: ["silk-corridor-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="grid max-w-xl gap-3"
      data-silk-corridor-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance korytarza Chiny–Europa jako katalog HITL. Para UN/LOCODE, km i live CR Express
        nie wchodzą do tego wiersza.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod stance Jedwabnego Szlaku"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <div className="grid gap-2 text-xs">
        <span>Rodzaj korytarza</span>
        <div className="flex flex-wrap gap-2" role="group" aria-label="Rodzaj korytarza Chiny-Europa">
          {KINDS.map((token) => (
            <Button
              key={token}
              aria-pressed={kind === token}
              className="h-8 px-3 font-mono text-xs"
              onClick={() => setKind(token)}
              type="button"
              variant={kind === token ? "default" : "outline"}
            >
              {token}
            </Button>
          ))}
        </div>
      </div>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://silk-corridor-mark/…)"
        ariaLabel="Pochodzenie stance Jedwabnego Szlaku"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz stance Jedwabnego Szlaku
      </Button>
    </form>
  )
}
