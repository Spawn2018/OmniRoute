import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildInventoryFinanceMarkWrite,
  saveInventoryFinanceMark,
} from "@/lib/inventory-finance-marks-api"

const KINDS = ["valuation", "aging", "release", "other"] as const

export function InventoryFinanceMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("inv_release_01")
  const [kind, setKind] = useState<string>("release")
  const [origin, setOrigin] = useState("fixture://inventory-finance/")
  const save = useMutation({
    mutationFn: () =>
      saveInventoryFinanceMark(buildInventoryFinanceMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("inv_release_01")
      setKind("release")
      setOrigin("fixture://inventory-finance/")
      void cache.invalidateQueries({
        queryKey: ["inventory-finance-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="grid max-w-xl gap-3"
      data-inventory-finance-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Wycena, wiekowanie lub Inventory Release jako katalog HITL. Silnik wyceny SQL,
        wartość Decimal i live zastaw nie wchodzą do tego wiersza.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika zapasu finansowego"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <div className="grid gap-2 text-xs">
        <span>Rodzaj finansowy</span>
        <div
          className="inline-flex max-w-full flex-wrap rounded-md border p-0.5"
          role="group"
          aria-label="Rodzaj znacznika zapasu finansowego"
        >
          {KINDS.map((token) => (
            <Button
              key={token}
              aria-pressed={kind === token}
              className="h-8 flex-1 min-w-[4.5rem] px-2 font-mono text-xs"
              onClick={() => setKind(token)}
              type="button"
              variant={kind === token ? "default" : "ghost"}
            >
              {token}
            </Button>
          ))}
        </div>
      </div>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://inventory-finance/…)"
        ariaLabel="Pochodzenie znacznika zapasu finansowego"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik zapasu
      </Button>
    </form>
  )
}
