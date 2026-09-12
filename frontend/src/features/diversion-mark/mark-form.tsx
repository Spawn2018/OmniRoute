import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createDiversionMark,
  makeDiversionMarkPayload,
} from "@/lib/diversion-marks-api"

const STANCE_KINDS = [
  { value: "diversion", label: "Diversion" },
  { value: "reroute", label: "Reroute" },
  { value: "other", label: "Inne" },
] as const

export function DiversionMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("dvm_diversion_main")
  const [kind, setKind] = useState("diversion")
  const [ref, setRef] = useState("fixture://diversion-mark/")
  const save = useMutation({
    mutationFn: () =>
      createDiversionMark(makeDiversionMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("dvm_diversion_main")
      setKind("diversion")
      setRef("fixture://diversion-mark/")
      void qc.invalidateQueries({
        queryKey: ["diversion-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-dvm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code diversion"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        stance_kind
        <select
          aria-label="stance_kind diversion reroute other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {STANCE_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref diversion"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik diversion
      </Button>
    </form>
  )
}
