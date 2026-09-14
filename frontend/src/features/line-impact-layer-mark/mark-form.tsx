import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildLineImpactLayerMarkWrite,
  saveLineImpactLayerMark,
} from "@/lib/line-impact-layer-marks-api"

const KINDS = ["scored", "forecast", "actual", "other"] as const

export function LineImpactLayerMarkSave(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [markCode, setMarkCode] = useState("lil_scored_01")
  const [layer, setLayer] = useState<string>("scored")
  const [ref, setRef] = useState("fixture://line-impact-layer/")
  const write = useMutation({
    mutationFn: () =>
      saveLineImpactLayerMark(
        buildLineImpactLayerMarkWrite({ code: markCode, kind: layer, origin: ref }),
      ),
    onSuccess: () => {
      setMarkCode("lil_scored_01")
      setLayer("scored")
      setRef("fixture://line-impact-layer/")
      void qc.invalidateQueries({ queryKey: ["line-impact-layer-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-2"
      data-line-impact-layer="composer"
      onSubmit={(ev: FormEvent) => {
        ev.preventDefault()
        if (props.organizationId) write.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL trybu warstwy liczonej (scored/forecast/actual). Silnik SQL i EBITDA zostają
        poza tym katalogiem.
      </p>
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code warstwy liczonej"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setMarkCode(e.target.value)}
          required
          value={markCode}
        />
      </label>
      <div className="flex flex-col gap-1 text-xs">
        <span>layer_kind</span>
        {KINDS.map((token) => (
          <Button
            key={token}
            aria-pressed={layer === token}
            className="h-8 justify-start font-mono"
            onClick={() => setLayer(token)}
            type="button"
            variant={layer === token ? "default" : "outline"}
          >
            {token}
          </Button>
        ))}
      </div>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref warstwy liczonej"
        value={ref}
        onChange={setRef}
      />
      {write.error ? <CatalogError error={write.error} /> : null}
      <Button disabled={!props.organizationId || write.isPending} type="submit" variant="outline">
        Zapisz tryb warstwy
      </Button>
    </form>
  )
}
