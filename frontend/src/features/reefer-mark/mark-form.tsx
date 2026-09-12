import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createReeferMark, makeReeferMarkPayload } from "@/lib/reefer-marks-api"

const OPTIONS = [
  { value: "reefer", label: "Reefer" },
  { value: "setpoint", label: "Setpoint" },
  { value: "genset", label: "Genset" },
  { value: "other", label: "Inne" },
] as const

export function ReeferMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("rf_manual_01")
  const [kind, setKind] = useState("reefer")
  const [ref, setRef] = useState("fixture://reefer-mark/")
  const mutation = useMutation({
    mutationFn: () => createReeferMark(makeReeferMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("rf_manual_01")
      setKind("reefer")
      setRef("fixture://reefer-mark/")
      void qc.invalidateQueries({ queryKey: ["reefer-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="flex flex-col gap-3 rounded-md border border-teal-900/25 bg-background p-3"
      data-rf="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) mutation.mutate()
      }}
    >
      <header>
        <p className="text-sm font-semibold">Nowy znacznik reefer</p>
        <p className="text-[11px] text-muted-foreground">HITL — bez live API i scrape.</p>
      </header>
      <div className="grid gap-2 sm:grid-cols-[1fr_11rem]">
        <label className="text-xs">
          mark_code
          <input
            aria-label="mark_code reefer"
            className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="text-xs">
          reefer_kind
          <select
            aria-label="reefer_kind reefer"
            className="mt-1 h-9 w-full rounded border px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </label>
      </div>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref reefer"
        value={ref}
        onChange={setRef}
      />
      {mutation.error ? <CatalogError error={mutation.error} /> : null}
      <Button disabled={!props.organizationId || mutation.isPending} type="submit" variant="outline">
        Zapisz reefer
      </Button>
    </form>
  )
}
