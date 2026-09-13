import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildPoFinancingMarkWrite,
  savePoFinancingMark,
} from "@/lib/po-financing-marks-api"

const KINDS = ["po", "release", "advance", "other"] as const

export function PoFinancingMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("po_trade_01")
  const [kind, setKind] = useState<string>("po")
  const [origin, setOrigin] = useState("fixture://po-financing/")
  const save = useMutation({
    mutationFn: () => savePoFinancingMark(buildPoFinancingMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("po_trade_01")
      setKind("po")
      setOrigin("fixture://po-financing/")
      void cache.invalidateQueries({
        queryKey: ["po-financing-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="grid max-w-xl gap-3"
      data-po-financing-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance finansowania zamówienia Trade-Tech jako katalog HITL. Wycena zapasu BR1.2 i live
        partner HTTP nie wchodzą do tego wiersza.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod stance PO Financing"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj finansowania</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="po-financing-mark-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://po-financing/…)"
        ariaLabel="Pochodzenie stance PO Financing"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz stance PO Financing
      </Button>
    </form>
  )
}
