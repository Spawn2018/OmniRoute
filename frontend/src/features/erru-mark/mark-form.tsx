import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createErruMark,
  makeErruMarkPayload,
} from "@/lib/erru-marks-api"

const CHECK_KINDS = [
  { value: "to_verify", label: "TO_VERIFY" },
  { value: "clear", label: "CLEAR" },
  { value: "hit", label: "HIT" },
  { value: "other", label: "Inne" },
] as const

export function ErruMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("erm_to_verify_01")
  const [kind, setKind] = useState("to_verify")
  const [ref, setRef] = useState("fixture://erru-mark/")
  const save = useMutation({
    mutationFn: () => createErruMark(makeErruMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("erm_to_verify_01")
      setKind("to_verify")
      setRef("fixture://erru-mark/")
      void qc.invalidateQueries({ queryKey: ["erru-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-violet-700/30 bg-violet-50/20 p-3 dark:bg-violet-950/10"
      data-erm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code erru"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        check_kind
        <select
          aria-label="check_kind to_verify clear hit"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {CHECK_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref erru"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik ERRU
      </Button>
    </form>
  )
}
