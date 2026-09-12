import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createRailUicMark,
  makeRailUicMarkPayload,
} from "@/lib/rail-uic-marks-api"

const RAIL_KINDS = [
  { value: "uic", label: "UIC" },
  { value: "cim", label: "CIM" },
  { value: "smgs", label: "SMGS" },
  { value: "other", label: "Inne" },
] as const

export function RailUicMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("rum_uic_01")
  const [kind, setKind] = useState("uic")
  const [ref, setRef] = useState("fixture://rail-uic-mark/")
  const save = useMutation({
    mutationFn: () =>
      createRailUicMark(makeRailUicMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("rum_uic_01")
      setKind("uic")
      setRef("fixture://rail-uic-mark/")
      void qc.invalidateQueries({
        queryKey: ["rail-uic-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-violet-700/30 bg-violet-50/20 p-3 dark:bg-violet-950/10"
      data-rum="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code rail-uic"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        rail_kind
        <select
          aria-label="rail_kind uic cim smgs"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {RAIL_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref rail-uic"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik UIC/CIM/SMGS
      </Button>
    </form>
  )
}
