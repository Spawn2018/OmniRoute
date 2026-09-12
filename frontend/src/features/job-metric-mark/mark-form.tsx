import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createJobMetricMark,
  makeJobMetricMarkPayload,
} from "@/lib/job-metric-marks-api"

const METRIC_KINDS = [
  { value: "time_to_fix", label: "Time to fix" },
  { value: "touches", label: "Touches" },
  { value: "rework", label: "Rework" },
  { value: "other", label: "Inne" },
] as const

export function JobMetricMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("jmm_time_to_fix_01")
  const [kind, setKind] = useState("time_to_fix")
  const [ref, setRef] = useState("fixture://job-metric-mark/")
  const save = useMutation({
    mutationFn: () => createJobMetricMark(makeJobMetricMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("jmm_time_to_fix_01")
      setKind("time_to_fix")
      setRef("fixture://job-metric-mark/")
      void qc.invalidateQueries({ queryKey: ["job-metric-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-violet-700/30 bg-violet-50/20 p-3 dark:bg-violet-950/10"
      data-jmm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code job metric"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        metric_kind
        <select
          aria-label="metric_kind time_to_fix touches rework"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {METRIC_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref job metric"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik metryki jobu
      </Button>
    </form>
  )
}
