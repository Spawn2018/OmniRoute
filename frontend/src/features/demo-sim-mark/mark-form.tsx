import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createDemoSimMark,
  makeDemoSimMarkPayload,
} from "@/lib/demo-sim-marks-api"

const SIM_KINDS = [
  { value: "fleet_150", label: "Flota 150" },
  { value: "months_10", label: "10 miesięcy" },
  { value: "other", label: "Inne" },
] as const

export function DemoSimMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("dsm_fleet_150_01")
  const [kind, setKind] = useState("fleet_150")
  const [ref, setRef] = useState("fixture://demo-sim-mark/")
  const save = useMutation({
    mutationFn: () =>
      createDemoSimMark(makeDemoSimMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("dsm_fleet_150_01")
      setKind("fleet_150")
      setRef("fixture://demo-sim-mark/")
      void qc.invalidateQueries({
        queryKey: ["demo-sim-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-dsm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code demo sim"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        sim_kind
        <select
          aria-label="sim_kind fleet_150 months_10 other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {SIM_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref demo sim"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik demo sim
      </Button>
    </form>
  )
}
