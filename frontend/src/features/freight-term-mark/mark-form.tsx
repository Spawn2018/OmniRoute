import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createFreightTermMark,
  makeFreightTermMarkPayload,
} from "@/lib/freight-term-marks-api"

const TERMS = [
  { value: "prepaid", label: "Prepaid" },
  { value: "collect", label: "Collect" },
  { value: "third_party", label: "Third party" },
  { value: "other", label: "Inne" },
] as const

export function FreightTermMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("ftm_prepaid_01")
  const [kind, setKind] = useState("prepaid")
  const [ref, setRef] = useState("fixture://freight-term-mark/")
  const save = useMutation({
    mutationFn: () =>
      createFreightTermMark(makeFreightTermMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("ftm_prepaid_01")
      setKind("prepaid")
      setRef("fixture://freight-term-mark/")
      void qc.invalidateQueries({
        queryKey: ["freight-term-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-ftm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code freight term"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        term_kind
        <select
          aria-label="term_kind prepaid collect third_party other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {TERMS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref freight term"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik warunku frachtu
      </Button>
    </form>
  )
}
