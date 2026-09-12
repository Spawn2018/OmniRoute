import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createTermsAiMark, makeTermsAiMarkPayload } from "@/lib/terms-ai-marks-api"

const TERMS_KINDS = [
  { value: "draft", label: "Draft" },
  { value: "clause", label: "Clause" },
  { value: "accept", label: "Accept" },
  { value: "other", label: "Inne" },
] as const

export function TermsAiMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("tai_draft_01")
  const [kind, setKind] = useState("draft")
  const [ref, setRef] = useState("fixture://terms-ai-mark/")
  const save = useMutation({
    mutationFn: () => createTermsAiMark(makeTermsAiMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("tai_draft_01")
      setKind("draft")
      setRef("fixture://terms-ai-mark/")
      void qc.invalidateQueries({ queryKey: ["terms-ai-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-stone-500/30 p-3"
      data-tai="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code terms ai"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        terms_kind
        <select
          aria-label="terms_kind draft clause accept"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {TERMS_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref terms ai"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz terms
      </Button>
    </form>
  )
}
