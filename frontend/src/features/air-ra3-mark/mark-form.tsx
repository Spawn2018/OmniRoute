import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { createAirRa3Mark, makeAirRa3MarkPayload } from "@/lib/air-ra3-marks-api"

const OPTIONS = [
  { value: "ra3", label: "RA3" },
  { value: "lithium", label: "Lithium" },
  { value: "known_consignor", label: "Known consignor" },
  { value: "other", label: "Inne" },
] as const

const DEFAULT_CODE = "air3_manual_01"
const DEFAULT_REF = "fixture://air-ra3-mark/"

export function AirRa3MarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState(DEFAULT_CODE)
  const [kind, setKind] = useState("ra3")
  const [ref, setRef] = useState(DEFAULT_REF)
  const mutation = useMutation({
    mutationFn: () => createAirRa3Mark(makeAirRa3MarkPayload(code, kind, ref)),
    onSuccess: () => {
      setCode(DEFAULT_CODE)
      setKind("ra3")
      setRef(DEFAULT_REF)
      void qc.invalidateQueries({ queryKey: ["air-ra3-marks", props.organizationId] })
    },
  })

  function onSubmit(event: FormEvent) {
    event.preventDefault()
    if (props.organizationId) mutation.mutate()
  }

  return (
    <form
      className="flex flex-col gap-3 rounded-md border border-indigo-900/25 bg-background p-3"
      data-air3="composer"
      onSubmit={onSubmit}
    >
      <header>
        <h2 className="text-sm font-semibold">Dodaj znacznik air</h2>
        <p className="text-[11px] text-muted-foreground">
          Tylko HITL — bez IATA live i bez scrape RA3.
        </p>
      </header>
      <div className="grid gap-2 sm:grid-cols-[1fr_12rem]">
        <label className="text-xs">
          mark_code
          <input
            aria-label="mark_code air RA3"
            className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="text-xs">
          air_kind
          <select
            aria-label="air_kind air RA3"
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
        ariaLabel="source_ref air RA3"
        value={ref}
        onChange={setRef}
      />
      {mutation.error ? <CatalogError error={mutation.error} /> : null}
      <Button disabled={!props.organizationId || mutation.isPending} type="submit">
        Zapisz air RA3
      </Button>
    </form>
  )
}
