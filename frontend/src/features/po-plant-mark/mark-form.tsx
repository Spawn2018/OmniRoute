import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createPoPlantMark,
  makePoPlantMarkPayload,
} from "@/lib/po-plant-marks-api"

const PLANT_KINDS = [
  { value: "plant", label: "Plant" },
  { value: "batch", label: "Batch" },
  { value: "sku", label: "SKU" },
  { value: "other", label: "Inne" },
] as const

export function PoPlantMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("ppm_plant_01")
  const [kind, setKind] = useState("plant")
  const [ref, setRef] = useState("fixture://po-plant-mark/")
  const save = useMutation({
    mutationFn: () =>
      createPoPlantMark(makePoPlantMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("ppm_plant_01")
      setKind("plant")
      setRef("fixture://po-plant-mark/")
      void qc.invalidateQueries({
        queryKey: ["po-plant-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-ppm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code po plant"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        plant_kind
        <select
          aria-label="plant_kind plant batch sku other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {PLANT_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref po plant"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik po plant
      </Button>
    </form>
  )
}
