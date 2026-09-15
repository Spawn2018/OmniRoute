import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildShipperRoundMarkWrite, saveShipperRoundMark } from "@/lib/shipper-round-marks-api"

const KINDS = ["first", "second", "final", "other"] as const

export function ShipperRoundMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("srm_first_01")
  const [kind, setKind] = useState<string>("first")
  const [origin, setOrigin] = useState("fixture://shipper-round-mark/")
  const save = useMutation({
    mutationFn: () => saveShipperRoundMark(buildShipperRoundMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("srm_first_01")
      setKind("first")
      setOrigin("fixture://shipper-round-mark/")
      void cache.invalidateQueries({ queryKey: ["shipper-round-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-shipper-round-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Runda przetargu załadowcy jako katalog HITL. Rodzaj to dana, nie Alpega i nie like-for-like.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod rundy przetargu załadowcy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj rundy</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="shipper-round-mark-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://shipper-round-mark/…)"
        ariaLabel="Pochodzenie rundy przetargu załadowcy"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz rundę
      </Button>
    </form>
  )
}
