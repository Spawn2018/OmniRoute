import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createSlotGuaranteeMark,
  makeSlotGuaranteeMarkPayload,
} from "@/lib/slot-guarantee-marks-api"

const STANCES = [
  { value: "capability", label: "Capability" },
  { value: "non_guarantee", label: "Bez gwarancji" },
  { value: "other", label: "Inne" },
] as const

export function SlotGuaranteeMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("sgm_cap_01")
  const [kind, setKind] = useState("capability")
  const [ref, setRef] = useState("fixture://slot-guarantee-mark/")
  const save = useMutation({
    mutationFn: () =>
      createSlotGuaranteeMark(makeSlotGuaranteeMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("sgm_cap_01")
      setKind("capability")
      setRef("fixture://slot-guarantee-mark/")
      void qc.invalidateQueries({
        queryKey: ["slot-guarantee-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-sgm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code slot guarantee"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        stance_kind
        <select
          aria-label="stance_kind capability non_guarantee other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {STANCES.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref slot guarantee"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik stance slotu
      </Button>
    </form>
  )
}
