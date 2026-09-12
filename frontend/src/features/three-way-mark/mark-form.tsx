import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createThreeWayMark,
  makeThreeWayMarkPayload,
} from "@/lib/three-way-marks-api"

const WAY_KINDS = [
  { value: "buyer", label: "Nabywca" },
  { value: "seller", label: "Sprzedawca" },
  { value: "carrier", label: "Przewoźnik" },
  { value: "other", label: "Inne" },
] as const

export function ThreeWayMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("twm_buyer_01")
  const [kind, setKind] = useState("buyer")
  const [ref, setRef] = useState("fixture://three-way-mark/")
  const save = useMutation({
    mutationFn: () =>
      createThreeWayMark(makeThreeWayMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("twm_buyer_01")
      setKind("buyer")
      setRef("fixture://three-way-mark/")
      void qc.invalidateQueries({
        queryKey: ["three-way-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-twm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code three way"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        way_kind
        <select
          aria-label="way_kind buyer seller carrier"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {WAY_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref three way"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik 3-way
      </Button>
    </form>
  )
}
