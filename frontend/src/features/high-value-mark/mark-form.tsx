import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createHighValueMark,
  makeHighValueMarkPayload,
} from "@/lib/high-value-marks-api"

const PROTOCOL_KINDS = [
  { value: "high_value", label: "High value" },
  { value: "protocol", label: "Protocol" },
  { value: "other", label: "Inne" },
] as const

export function HighValueMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("hvm_high_value_01")
  const [kind, setKind] = useState("high_value")
  const [ref, setRef] = useState("fixture://high-value-mark/")
  const save = useMutation({
    mutationFn: () =>
      createHighValueMark(makeHighValueMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("hvm_high_value_01")
      setKind("high_value")
      setRef("fixture://high-value-mark/")
      void qc.invalidateQueries({
        queryKey: ["high-value-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-hvm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code high value"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        protocol_kind
        <select
          aria-label="protocol_kind high_value protocol other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {PROTOCOL_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref high value"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik protokolu high-value
      </Button>
    </form>
  )
}
