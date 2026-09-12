import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createLineImpactMark,
  makeLineImpactMarkPayload,
} from "@/lib/line-impact-marks-api"

const IMPACT_KINDS = [
  { value: "line", label: "Linia" },
  { value: "plant", label: "Zakład" },
  { value: "sku", label: "SKU" },
  { value: "other", label: "Inne" },
] as const

export function LineImpactMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("lim_line_01")
  const [kind, setKind] = useState("line")
  const [ref, setRef] = useState("fixture://line-impact-mark/")
  const save = useMutation({
    mutationFn: () =>
      createLineImpactMark(makeLineImpactMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("lim_line_01")
      setKind("line")
      setRef("fixture://line-impact-mark/")
      void qc.invalidateQueries({
        queryKey: ["line-impact-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-lim="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code line impact"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        impact_kind
        <select
          aria-label="impact_kind line plant sku"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {IMPACT_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref line impact"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik skutku linii
      </Button>
    </form>
  )
}
