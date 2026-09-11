import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useId, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  packCombinedTransportWrite,
  saveCombinedTransportMark,
} from "@/lib/combined-transport-marks-api"

const REGIMES: ReadonlyArray<{ key: string; note: string }> = [
  { key: "combined", note: "transport kombinowany" },
  { key: "mobility", note: "Mobility Package" },
  { key: "piggyback", note: "Huckepack / piggyback" },
  { key: "other", note: "inny reżim" },
]

export function CombinedTransportEditor(props: { organizationId: string | null }) {
  const uid = useId()
  const qc = useQueryClient()
  const [markCode, setMarkCode] = useState("combined_01")
  const [regime, setRegime] = useState("combined")
  const [sourceRef, setSourceRef] = useState("fixture://combined-transport-mark/")
  const mutation = useMutation({
    mutationFn: () =>
      saveCombinedTransportMark(packCombinedTransportWrite(markCode, regime, sourceRef)),
    onSuccess: () => {
      setMarkCode("combined_01")
      setRegime("combined")
      setSourceRef("fixture://combined-transport-mark/")
      void qc.invalidateQueries({
        queryKey: ["combined-transport-marks", props.organizationId],
      })
    },
  })

  function onSubmit(event: FormEvent) {
    event.preventDefault()
    if (props.organizationId == null) return
    mutation.mutate()
  }

  return (
    <details className="max-w-xl open:pb-2" data-ct="editor" open>
      <summary className="cursor-pointer text-sm font-medium">
        Nowy reżim combined transport
      </summary>
      <form className="mt-3 space-y-3" id={uid} onSubmit={onSubmit}>
        <p className="text-xs text-muted-foreground">
          Etykieta reżimu (combined / mobility / piggyback). Bez silnika Mobility Package i bez
          solvera Huckepack.
        </p>
        <label className="grid gap-1 text-xs">
          Kod
          <input
            aria-label="Kod combined transport"
            className="h-9 rounded-md border bg-background px-2 font-mono"
            onChange={(e) => setMarkCode(e.target.value)}
            required
            value={markCode}
          />
        </label>
        <fieldset className="grid gap-2 text-xs">
          <legend>Reżim (`regime_kind`)</legend>
          {REGIMES.map((row) => (
            <label key={row.key} className="flex items-center gap-2">
              <input
                checked={regime === row.key}
                name={`${uid}-regime`}
                onChange={() => setRegime(row.key)}
                type="radio"
                value={row.key}
              />
              <span>
                {row.key} — {row.note}
              </span>
            </label>
          ))}
        </fieldset>
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="Pochodzenie combined transport"
          value={sourceRef}
          onChange={setSourceRef}
        />
        {mutation.error ? <CatalogError error={mutation.error} /> : null}
        <Button disabled={props.organizationId == null || mutation.isPending} type="submit">
          Zapisz reżim
        </Button>
      </form>
    </details>
  )
}
