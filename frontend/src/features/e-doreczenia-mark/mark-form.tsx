import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createEDoreczeniaMark,
  makeEDoreczeniaMarkPayload,
} from "@/lib/e-doreczenia-marks-api"

const DELIVERY_KINDS = [
  { value: "edoreczenia", label: "e-Doręczenia" },
  { value: "receipt", label: "Receipt" },
  { value: "other", label: "Inne" },
] as const

export function EDoreczeniaMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("edm_edoreczenia_01")
  const [kind, setKind] = useState("edoreczenia")
  const [ref, setRef] = useState("fixture://e-doreczenia-mark/")
  const save = useMutation({
    mutationFn: () =>
      createEDoreczeniaMark(makeEDoreczeniaMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("edm_edoreczenia_01")
      setKind("edoreczenia")
      setRef("fixture://e-doreczenia-mark/")
      void qc.invalidateQueries({
        queryKey: ["e-doreczenia-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-violet-700/30 bg-violet-50/20 p-3 dark:bg-violet-950/10"
      data-edm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code e-doreczenia"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        delivery_kind
        <select
          aria-label="delivery_kind edoreczenia receipt"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {DELIVERY_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref e-doreczenia"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik e-Doręczenia
      </Button>
    </form>
  )
}
