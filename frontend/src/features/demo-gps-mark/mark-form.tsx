import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createDemoGpsMark,
  makeDemoGpsMarkPayload,
} from "@/lib/demo-gps-marks-api"

const DEMO_KINDS = [
  { value: "seven_day", label: "7 dni" },
  { value: "fleet_demo", label: "Flota demo" },
  { value: "other", label: "Inne" },
] as const

export function DemoGpsMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("dgm_seven_day_01")
  const [kind, setKind] = useState("seven_day")
  const [ref, setRef] = useState("fixture://demo-gps-mark/")
  const save = useMutation({
    mutationFn: () => createDemoGpsMark(makeDemoGpsMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("dgm_seven_day_01")
      setKind("seven_day")
      setRef("fixture://demo-gps-mark/")
      void qc.invalidateQueries({ queryKey: ["demo-gps-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-violet-700/30 bg-violet-50/20 p-3 dark:bg-violet-950/10"
      data-dgm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code demo gps"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        demo_kind
        <select
          aria-label="demo_kind seven_day fleet_demo"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {DEMO_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref demo gps"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik demo GPS
      </Button>
    </form>
  )
}
