import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createRoleViewMark,
  makeRoleViewMarkPayload,
} from "@/lib/role-view-marks-api"

const VIEW_KINDS = [
  { value: "groupage", label: "Groupage" },
  { value: "ftl", label: "FTL" },
  { value: "ocean", label: "Ocean" },
  { value: "other", label: "Inne" },
] as const

export function RoleViewMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("rvm_groupage_01")
  const [kind, setKind] = useState("groupage")
  const [ref, setRef] = useState("fixture://role-view-mark/")
  const save = useMutation({
    mutationFn: () => createRoleViewMark(makeRoleViewMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("rvm_groupage_01")
      setKind("groupage")
      setRef("fixture://role-view-mark/")
      void qc.invalidateQueries({ queryKey: ["role-view-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-rvm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code role view"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        view_kind
        <select
          aria-label="view_kind groupage ftl ocean"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {VIEW_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref role view"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz widok roli
      </Button>
    </form>
  )
}
