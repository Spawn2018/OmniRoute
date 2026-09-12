import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createUnSegregationMark,
  makeUnSegregationMarkPayload,
} from "@/lib/un-segregation-marks-api"

const SEGREGATE_KINDS = [
  { value: "tunnel", label: "Tunel" },
  { value: "segregation", label: "Segregacja" },
  { value: "compat", label: "Kompatybilnosc" },
  { value: "other", label: "Inne" },
] as const

export function UnSegregationMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("usm_tunnel_01")
  const [kind, setKind] = useState("tunnel")
  const [ref, setRef] = useState("fixture://un-segregation-mark/")
  const save = useMutation({
    mutationFn: () =>
      createUnSegregationMark(makeUnSegregationMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("usm_tunnel_01")
      setKind("tunnel")
      setRef("fixture://un-segregation-mark/")
      void qc.invalidateQueries({
        queryKey: ["un-segregation-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-usm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code segregacji UN"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        segregate_kind
        <select
          aria-label="segregate_kind tunnel segregation compat other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {SEGREGATE_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref segregacji UN"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik segregacji UN
      </Button>
    </form>
  )
}
