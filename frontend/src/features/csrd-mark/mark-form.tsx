import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createCsrdMark, makeCsrdMarkPayload } from "@/lib/csrd-marks-api"

const OPTIONS = [
  { value: "csrd", label: "CSRD" },
  { value: "esrs", label: "ESRS" },
  { value: "assurance", label: "Assurance" },
  { value: "other", label: "Inne" },
] as const

const DEFAULT_CODE = "csrd_manual_01"
const DEFAULT_REF = "fixture://csrd-mark/"

export function CsrdMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState(DEFAULT_CODE)
  const [kind, setKind] = useState<string>("csrd")
  const [ref, setRef] = useState(DEFAULT_REF)
  const mutation = useMutation({
    mutationFn: () => createCsrdMark(makeCsrdMarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode(DEFAULT_CODE)
      setKind("csrd")
      setRef(DEFAULT_REF)
      void qc.invalidateQueries({ queryKey: ["csrd-marks", props.organizationId] })
    },
  })

  function onSubmit(event: FormEvent) {
    event.preventDefault()
    if (props.organizationId) mutation.mutate()
  }

  return (
    <form
      className="flex flex-col gap-3 rounded-md border border-emerald-900/20 bg-background p-3"
      data-csrd="composer"
      onSubmit={onSubmit}
    >
      <header>
        <h2 className="text-sm font-semibold">Dodaj znacznik CSRD</h2>
        <p className="text-[11px] text-muted-foreground">
          Tylko HITL — bez kalkulatora i bez filing live.
        </p>
      </header>
      <div className="flex flex-col gap-2 md:flex-row">
        <label className="flex-1 text-xs">
          mark_code
          <input
            aria-label="mark_code CSRD"
            className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="w-full text-xs md:w-48">
          report_kind
          <select
            aria-label="report_kind CSRD"
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
        ariaLabel="source_ref CSRD"
        value={ref}
        onChange={setRef}
      />
      {mutation.error ? <CatalogError error={mutation.error} /> : null}
      <Button disabled={!props.organizationId || mutation.isPending} type="submit" variant="outline">
        Zapisz CSRD
      </Button>
    </form>
  )
}
