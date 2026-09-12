import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createInventoryPositionMark,
  makeInventoryPositionPayload,
} from "@/lib/inventory-position-marks-api"

const STOCK_KINDS = [
  { key: "position", tip: "pozycja" },
  { key: "plant", tip: "zaklad" },
  { key: "sku", tip: "SKU" },
  { key: "other", tip: "inny" },
] as const

export function InventoryPositionComposer(props: {
  organizationId: string | null
}) {
  const client = useQueryClient()
  const [code, setCode] = useState("ip_pos_01")
  const [kind, setKind] = useState("position")
  const [ref, setRef] = useState("fixture://inventory-position-mark/")
  const save = useMutation({
    mutationFn: () =>
      createInventoryPositionMark(makeInventoryPositionPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("ip_pos_01")
      setKind("position")
      setRef("fixture://inventory-position-mark/")
      void client.invalidateQueries({
        queryKey: ["inventory-position-marks", props.organizationId],
      })
    },
  })

  return (
    <div className="border-b pb-4" data-ip="composer">
      <h2 className="text-sm font-semibold">Znacznik inventory position (HITL)</h2>
      <p className="mb-3 text-xs text-muted-foreground">
        Pozycja magazynowa HITL. Bez WMS live i bez bilansu SQL.
      </p>
      <form
        className="grid gap-2 md:grid-cols-3"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) save.mutate()
        }}
      >
        <label className="text-xs">
          mark_code
          <input
            aria-label="mark_code inventory"
            className="mt-1 h-9 w-full rounded border bg-background px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="text-xs">
          stock_kind
          <select
            aria-label="stock_kind"
            className="mt-1 h-9 w-full rounded border bg-background px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {STOCK_KINDS.map((row) => (
              <option key={row.key} value={row.key}>
                {row.key} — {row.tip}
              </option>
            ))}
          </select>
        </label>
        <div className="text-xs">
          <CatalogSourceRefField
            label="source_ref"
            ariaLabel="source_ref inventory"
            value={ref}
            onChange={setRef}
          />
        </div>
        {save.error ? (
          <div className="md:col-span-3">
            <CatalogError error={save.error} />
          </div>
        ) : null}
        <Button
          className="md:col-span-3"
          disabled={!props.organizationId || save.isPending}
          type="submit"
        >
          Zapisz znacznik inventory position
        </Button>
      </form>
    </div>
  )
}
