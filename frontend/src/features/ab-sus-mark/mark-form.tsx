import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createAbSusMark, makeAbSusMarkPayload } from "@/lib/ab-sus-marks-api"

const TRIAL_KINDS = [
  { value: "ab", label: "A/B" },
  { value: "sus", label: "SUS" },
  { value: "cohort", label: "Cohort" },
  { value: "other", label: "Inne" },
] as const

export function AbSusMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("abs_ab_01")
  const [kind, setKind] = useState("ab")
  const [ref, setRef] = useState("fixture://ab-sus-mark/")
  const save = useMutation({
    mutationFn: () => createAbSusMark(makeAbSusMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("abs_ab_01")
      setKind("ab")
      setRef("fixture://ab-sus-mark/")
      void qc.invalidateQueries({ queryKey: ["ab-sus-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex flex-wrap items-end gap-3 rounded-sm border border-slate-500/40 bg-background p-3"
      data-abs="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code ab sus"
          className="mt-1 block h-9 w-44 rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        trial_kind
        <select
          aria-label="trial_kind ab sus cohort"
          className="mt-1 block h-9 w-36 rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {TRIAL_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <div className="min-w-[16rem] flex-1">
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref ab sus"
          value={ref}
          onChange={setRef}
        />
      </div>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz probe
      </Button>
    </form>
  )
}
