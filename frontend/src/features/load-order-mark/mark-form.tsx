import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createLoadOrderMark, makeLoadOrderMarkPayload } from "@/lib/load-order-marks-api"

const ORDER_KINDS = ["sequence", "stack", "door", "other"] as const

export function LoadOrderMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [markCode, setMarkCode] = useState("lor_seq_01")
  const [orderKind, setOrderKind] = useState<string>("sequence")
  const [sourceRef, setSourceRef] = useState("fixture://load-order-mark/")
  const persist = useMutation({
    mutationFn: () =>
      createLoadOrderMark(makeLoadOrderMarkPayload(markCode, orderKind, sourceRef)),
    onSuccess: () => {
      setMarkCode("lor_seq_01")
      setOrderKind("sequence")
      setSourceRef("fixture://load-order-mark/")
      void cache.invalidateQueries({ queryKey: ["load-order-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-load-order-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Kolejność załadunku jako katalog HITL. Rodzaj to dana, nie solver i nie osie G6.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika kolejności załadunku"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setMarkCode(change.target.value)}
          required
          value={markCode}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj kolejności</legend>
        {ORDER_KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={orderKind === token}
              name="load-order-mark-kind"
              onChange={() => setOrderKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://load-order-mark/…)"
        ariaLabel="Pochodzenie znacznika kolejności załadunku"
        value={sourceRef}
        onChange={setSourceRef}
      />
      {persist.error ? <CatalogError error={persist.error} /> : null}
      <Button disabled={!args.organizationId || persist.isPending} type="submit">
        Zapisz kolejność załadunku
      </Button>
    </form>
  )
}
