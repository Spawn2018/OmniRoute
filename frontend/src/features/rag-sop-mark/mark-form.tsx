import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createRagSopMark,
  makeRagSopMarkPayload,
} from "@/lib/rag-sop-marks-api"

const SCOPE_KINDS = [
  { value: "sop", label: "SOP" },
  { value: "adr", label: "ADR" },
  { value: "mail", label: "Mail" },
  { value: "other", label: "Inne" },
] as const

export function RagSopMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("rsm_sop_01")
  const [kind, setKind] = useState("sop")
  const [ref, setRef] = useState("fixture://rag-sop-mark/")
  const save = useMutation({
    mutationFn: () => createRagSopMark(makeRagSopMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("rsm_sop_01")
      setKind("sop")
      setRef("fixture://rag-sop-mark/")
      void qc.invalidateQueries({ queryKey: ["rag-sop-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-violet-700/30 bg-violet-50/20 p-3 dark:bg-violet-950/10"
      data-rsm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code rag sop"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        scope_kind
        <select
          aria-label="scope_kind sop adr mail"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {SCOPE_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref rag sop"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz zakres RAG
      </Button>
    </form>
  )
}
