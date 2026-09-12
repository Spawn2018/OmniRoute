import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createChassisMark,
  makeChassisMarkPayload,
} from "@/lib/chassis-marks-api"

const CHASSIS_KINDS = [
  { value: "chassis", label: "Chassis" },
  { value: "trailer", label: "Trailer" },
  { value: "other", label: "Inne" },
] as const

export function ChassisMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("chm_chassis_01")
  const [kind, setKind] = useState("chassis")
  const [ref, setRef] = useState("fixture://chassis-mark/")
  const save = useMutation({
    mutationFn: () =>
      createChassisMark(makeChassisMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("chm_chassis_01")
      setKind("chassis")
      setRef("fixture://chassis-mark/")
      void qc.invalidateQueries({
        queryKey: ["chassis-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-chm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code chassis"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        chassis_kind
        <select
          aria-label="chassis_kind chassis trailer"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {CHASSIS_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref chassis"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik chassis/trailer
      </Button>
    </form>
  )
}
