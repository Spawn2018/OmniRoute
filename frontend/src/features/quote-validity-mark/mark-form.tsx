import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createQuoteValidityMark,
  makeQuoteValidityMarkPayload,
} from "@/lib/quote-validity-marks-api"

const VALIDITY_KINDS = [
  { value: "open", label: "Open" },
  { value: "revised", label: "Revised" },
  { value: "superseded", label: "Superseded" },
  { value: "other", label: "Inne" },
] as const

export function QuoteValidityMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("qvm_open_main")
  const [kind, setKind] = useState("open")
  const [ref, setRef] = useState("fixture://quote-validity-mark/")
  const save = useMutation({
    mutationFn: () =>
      createQuoteValidityMark(makeQuoteValidityMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("qvm_open_main")
      setKind("open")
      setRef("fixture://quote-validity-mark/")
      void qc.invalidateQueries({
        queryKey: ["quote-validity-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-qvm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code quote validity"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        validity_kind
        <select
          aria-label="validity_kind open revised superseded other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {VALIDITY_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref quote validity"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik quote validity
      </Button>
    </form>
  )
}
