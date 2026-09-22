import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildPalletSynchroMarkWrite,
  savePalletSynchroMark,
} from "@/lib/pallet-synchro-marks-api"

const SYNCHRO_OPTIONS = ["aligned", "drift", "held", "other"] as const

export function PalletSynchroMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("synchro_aligned_01")
  const [kind, setKind] = useState<string>("aligned")
  const [ref, setRef] = useState("fixture://pallet-synchro/")
  const save = useMutation({
    mutationFn: () => savePalletSynchroMark(buildPalletSynchroMarkWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("synchro_aligned_01")
      setKind("aligned")
      setRef("fixture://pallet-synchro/")
      void cache.invalidateQueries({ queryKey: ["pallet-synchro-marks", args.organizationId] })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-3"
      data-pallet-synchro-mark="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance zgodności salda z ledgerem jako dana HITL — nie auto-UPDATE i nie giełda.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod synchro palet"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>synchro_kind</legend>
        {SYNCHRO_OPTIONS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="pallet-synchro-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://pallet-synchro/…)"
        ariaLabel="Pochodzenie synchro palet"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz synchro palet
      </Button>
    </form>
  )
}
