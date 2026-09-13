import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createCounterfactualRun,
  makeCounterfactualRunPayload,
} from "@/lib/counterfactual-runs-api"

export function CounterfactualRunComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [runCode, setRunCode] = useState("fuel_spike")
  const [baselineLabel, setBaselineLabel] = useState("plan z wczoraj")
  const [leversLabel, setLeversLabel] = useState("paliwo w gore")
  const [resultLabel, setResultLabel] = useState("eta plus dwie godziny")
  const [ref, setRef] = useState("fixture://counterfactual-run/")
  const save = useMutation({
    mutationFn: () =>
      createCounterfactualRun(
        makeCounterfactualRunPayload({
          runCode,
          baselineLabel,
          leversLabel,
          resultLabel,
          sourceRef: ref,
        }),
      ),
    onSuccess: () => {
      setRef("fixture://counterfactual-run/")
      void qc.invalidateQueries({
        queryKey: ["counterfactual-runs", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-counterfactual-run="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        run_code
        <input
          aria-label="run_code counterfactual"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setRunCode(e.target.value)}
          required
          value={runCode}
        />
      </label>
      <label className="text-xs">
        baseline_label
        <input
          aria-label="baseline_label punkt odniesienia"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setBaselineLabel(e.target.value)}
          required
          value={baselineLabel}
        />
      </label>
      <label className="text-xs">
        levers_label
        <input
          aria-label="levers_label dzwignie"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setLeversLabel(e.target.value)}
          required
          value={leversLabel}
        />
      </label>
      <label className="text-xs">
        result_label
        <input
          aria-label="result_label wynik"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setResultLabel(e.target.value)}
          required
          value={resultLabel}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref counterfactual"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz przebieg what-if
      </Button>
    </form>
  )
}
