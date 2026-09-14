import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildWmsFlowMarkWrite, saveWmsFlowMark } from "@/lib/wms-flow-marks-api"

const KINDS = ["receipt", "location", "pick", "ship", "count", "other"] as const

export function WmsFlowMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("wms_receipt_01")
  const [kind, setKind] = useState<string>("receipt")
  const [origin, setOrigin] = useState("fixture://wms-flow/")
  const save = useMutation({
    mutationFn: () => saveWmsFlowMark(buildWmsFlowMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("wms_receipt_01")
      setKind("receipt")
      setOrigin("fixture://wms-flow/")
      void cache.invalidateQueries({
        queryKey: ["wms-flow-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="grid max-w-xl gap-3"
      data-wms-flow-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Rodzaj operacji magazynowej WMS jako katalog HITL. Lokalizacja bin, RFID i live WMS nie
        wchodzą do tego wiersza.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod operacji WMS"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <div className="grid gap-2 text-xs">
        <span>Przepływ magazynowy</span>
        <div
          className="inline-flex max-w-full flex-wrap rounded-md border p-0.5"
          role="group"
          aria-label="Rodzaj przepływu WMS"
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
        label="source_ref (tenant:manual albo fixture://wms-flow/…)"
        ariaLabel="Pochodzenie operacji WMS"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz operację WMS
      </Button>
    </form>
  )
}
