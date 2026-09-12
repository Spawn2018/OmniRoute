import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createHaulierRoleMark,
  makeHaulierRoleMarkPayload,
} from "@/lib/haulier-role-marks-api"

const ROLE_KINDS = [
  { value: "booked", label: "Booked" },
  { value: "actual", label: "Actual" },
  { value: "other", label: "Inne" },
] as const

export function HaulierRoleMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("hrm_booked_main")
  const [kind, setKind] = useState("booked")
  const [ref, setRef] = useState("fixture://haulier-role-mark/")
  const save = useMutation({
    mutationFn: () =>
      createHaulierRoleMark(makeHaulierRoleMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("hrm_booked_main")
      setKind("booked")
      setRef("fixture://haulier-role-mark/")
      void qc.invalidateQueries({
        queryKey: ["haulier-role-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-hrm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code haulier role"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        role_kind
        <select
          aria-label="role_kind booked actual other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {ROLE_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref haulier role"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik roli przewoznika
      </Button>
    </form>
  )
}
