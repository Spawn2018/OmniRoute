import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildShipperTenderMarkWrite, saveShipperTenderMark } from "@/lib/shipper-tender-marks-api"

const KINDS = ["round", "bench", "spot", "other"] as const

export function ShipperTenderMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("stm_round_01")
  const [kind, setKind] = useState<string>("round")
  const [origin, setOrigin] = useState("fixture://shipper-tender-mark/")
  const save = useMutation({
    mutationFn: () => saveShipperTenderMark(buildShipperTenderMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("stm_round_01")
      setKind("round")
      setOrigin("fixture://shipper-tender-mark/")
      void cache.invalidateQueries({ queryKey: ["shipper-tender-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-shipper-tender-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Tryb przetargu załadowcy jako katalog HITL. Rodzaj to dana, nie druga tabela tender i nie auto-award.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod trybu przetargu załadowcy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj trybu</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="shipper-tender-mark-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://shipper-tender-mark/…)"
        ariaLabel="Pochodzenie trybu przetargu załadowcy"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz tryb
      </Button>
    </form>
  )
}
