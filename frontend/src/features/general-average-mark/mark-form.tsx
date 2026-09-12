import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createGeneralAverageMark,
  makeGeneralAveragePayload,
} from "@/lib/general-average-marks-api"

const KINDS = [
  { value: "ga", note: "general average" },
  { value: "contribution", note: "contribution" },
  { value: "sacrifice", note: "sacrifice" },
  { value: "other", note: "inne" },
] as const

const CODE0 = "ga_manual_01"
const REF0 = "fixture://general-average-mark/"

export function GeneralAverageComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState(CODE0)
  const [kind, setKind] = useState("ga")
  const [ref, setRef] = useState(REF0)
  const save = useMutation({
    mutationFn: () => createGeneralAverageMark(makeGeneralAveragePayload(code, kind, ref)),
    onSuccess: () => {
      setCode(CODE0)
      setKind("ga")
      setRef(REF0)
      void qc.invalidateQueries({ queryKey: ["general-average-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 rounded border border-sky-700/20 bg-sky-50/30 p-3 dark:bg-sky-950/20"
      data-ga="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <p className="text-sm font-semibold">Wpis general average</p>
      <p className="text-[11px] text-muted-foreground">HITL only — zakaz GA live i scrape.</p>
      <label className="text-xs">
        mark_code
        <input
          aria-label="mark_code GA"
          className="mt-1 h-8 w-full rounded border px-2 font-mono text-sm"
          onChange={(event) => setCode(event.target.value)}
          required
          value={code}
        />
      </label>
      <label className="text-xs">
        average_kind
        <select
          aria-label="average_kind GA"
          className="mt-1 h-8 w-full rounded border px-2 text-sm"
          onChange={(event) => setKind(event.target.value)}
          value={kind}
        >
          {KINDS.map((row) => (
            <option key={row.value} value={row.value}>
              {row.value} — {row.note}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref GA"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit">
        Zapisz znacznik GA
      </Button>
    </form>
  )
}
