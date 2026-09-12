import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createProfitCenterMark,
  makeProfitCenterMarkPayload,
} from "@/lib/profit-center-marks-api"

const CENTER_KINDS = [
  { value: "profit", label: "Profit center" },
  { value: "cost", label: "Cost center" },
  { value: "project", label: "Project code" },
  { value: "other", label: "Inne" },
] as const

export function ProfitCenterMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("pcm_profit_01")
  const [kind, setKind] = useState("profit")
  const [ref, setRef] = useState("fixture://profit-center-mark/")
  const save = useMutation({
    mutationFn: () =>
      createProfitCenterMark(makeProfitCenterMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("pcm_profit_01")
      setKind("profit")
      setRef("fixture://profit-center-mark/")
      void qc.invalidateQueries({
        queryKey: ["profit-center-marks", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-pcm="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code profit center"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setCode(e.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        center_kind
        <select
          aria-label="center_kind profit cost project other"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {CENTER_KINDS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref profit center"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz znacznik centrum zysku/kosztu
      </Button>
    </form>
  )
}
