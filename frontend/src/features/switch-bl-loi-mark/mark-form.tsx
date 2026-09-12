import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createSwitchBlLoiMark,
  makeSwitchBlLoiPayload,
} from "@/lib/switch-bl-loi-marks-api"

const INSTRUMENTS = [
  { value: "bl", note: "bill of lading" },
  { value: "loi", note: "letter of indemnity" },
  { value: "switch", note: "switch BL" },
  { value: "other", note: "inne" },
] as const

const CODE0 = "sbl_manual_01"
const REF0 = "tenant:manual://switch-bl-loi/"

export function SwitchBlLoiComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState(CODE0)
  const [kind, setKind] = useState("bl")
  const [ref, setRef] = useState(REF0)
  const save = useMutation({
    mutationFn: () => createSwitchBlLoiMark(makeSwitchBlLoiPayload(code, kind, ref)),
    onSuccess: () => {
      setCode(CODE0)
      setKind("bl")
      setRef(REF0)
      void qc.invalidateQueries({ queryKey: ["switch-bl-loi-marks", props.organizationId] })
    },
  })

  return (
    <form
      className="space-y-3 border-b border-dashed border-slate-400/50 pb-4"
      data-sbl="intake"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <header className="space-y-1">
        <h2 className="text-sm font-semibold uppercase tracking-wide">Instrument BL/LOI</h2>
        <p className="text-xs text-muted-foreground">HITL only — zakaz switch BL live i LOI scrape.</p>
      </header>
      <div className="flex flex-col gap-2 sm:flex-row">
        <label className="flex-1 text-xs">
          mark_code
          <input
            aria-label="mark_code switch BL"
            className="mt-1 h-8 w-full border-b bg-transparent px-1 font-mono text-sm outline-none"
            onChange={(event) => setCode(event.target.value)}
            required
            value={code}
          />
        </label>
        <label className="flex-1 text-xs">
          instrument_kind
          <select
            aria-label="instrument_kind switch BL"
            className="mt-1 h-8 w-full border-b bg-transparent px-1 text-sm outline-none"
            onChange={(event) => setKind(event.target.value)}
            value={kind}
          >
            {INSTRUMENTS.map((row) => (
              <option key={row.value} value={row.value}>
                {row.value} — {row.note}
              </option>
            ))}
          </select>
        </label>
      </div>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref switch BL"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz instrument
      </Button>
    </form>
  )
}
