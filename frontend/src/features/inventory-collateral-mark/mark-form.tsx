import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildInventoryCollateralMarkWrite,
  saveInventoryCollateralMark,
} from "@/lib/inventory-collateral-marks-api"

const KINDS = ["pledge", "lien", "hold", "other"] as const

export function InventoryCollateralMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("col_pledge_01")
  const [kind, setKind] = useState<string>("pledge")
  const [origin, setOrigin] = useState("fixture://inventory-collateral/")
  const save = useMutation({
    mutationFn: () =>
      saveInventoryCollateralMark(
        buildInventoryCollateralMarkWrite({ code, kind, origin }),
      ),
    onSuccess: () => {
      setCode("col_pledge_01")
      setKind("pledge")
      setOrigin("fixture://inventory-collateral/")
      void cache.invalidateQueries({
        queryKey: ["inventory-collateral-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="grid max-w-xl gap-3"
      data-inventory-collateral-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Zastaw, lien lub hold na towarze jako katalog HITL. Klej do pozycji magazynowej
        i live zastaw nie wchodzą do tego wiersza.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika zabezpieczenia"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj zabezpieczenia</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2 font-mono">
            <input
              checked={kind === token}
              name="inventory-collateral-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://inventory-collateral/…)"
        ariaLabel="Pochodzenie znacznika zabezpieczenia"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik zabezpieczenia
      </Button>
    </form>
  )
}
