import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createFunnelMark, makeFunnelMarkPayload } from "@/lib/funnel-marks-api"

const FUNNEL_KINDS = [
  { value: "lead", label: "Lead" },
  { value: "quote", label: "Quote" },
  { value: "win", label: "Win" },
  { value: "other", label: "Inne" },
] as const

export function FunnelMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("fn_lead_01")
  const [kind, setKind] = useState("lead")
  const [ref, setRef] = useState("fixture://funnel-mark/")
  const save = useMutation({
    mutationFn: () => createFunnelMark(makeFunnelMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("fn_lead_01")
      setKind("lead")
      setRef("fixture://funnel-mark/")
      void qc.invalidateQueries({ queryKey: ["funnel-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="grid gap-2 sm:grid-cols-2"
      data-fn="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code funnel"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        funnel_kind
        <select
          aria-label="funnel_kind lead quote win"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {FUNNEL_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <div className="sm:col-span-2">
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref funnel"
          value={ref}
          onChange={setRef}
        />
      </div>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button
        className="sm:col-span-2 sm:justify-self-start"
        disabled={!props.organizationId || save.isPending}
        type="submit"
        variant="ghost"
      >
        Zapisz lejek
      </Button>
    </form>
  )
}
