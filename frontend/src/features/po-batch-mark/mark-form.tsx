import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createPoBatchMark,
  makePoBatchMarkPayload,
} from "@/lib/po-batch-marks-api"

const BATCH_KINDS = [
  { value: "batch", label: "Batch" },
  { value: "lot", label: "Lot" },
  { value: "serial", label: "Serial" },
  { value: "other", label: "Inne" },
] as const

export function PoBatchMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("pbm_batch_01")
  const [kind, setKind] = useState("batch")
  const [ref, setRef] = useState("fixture://po-batch-mark/")
  const save = useMutation({
    mutationFn: () =>
      createPoBatchMark(makePoBatchMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("pbm_batch_01")
      setKind("batch")
      setRef("fixture://po-batch-mark/")
      void qc.invalidateQueries({
        queryKey: ["po-batch-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-pbm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code po batch"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        batch_kind
        <select
          aria-label="batch_kind batch lot serial other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {BATCH_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref po batch"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik po batch
      </Button>
    </form>
  )
}
