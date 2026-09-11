import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { packFleetCostWrite, saveFleetCostMark } from "@/lib/fleet-cost-marks-api"

const KINDS = [
  { id: "tco", label: "TCO" },
  { id: "maintenance", label: "utrzymanie" },
  { id: "lease", label: "leasing" },
  { id: "other", label: "inny" },
] as const

export function FleetCostEntry(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("tco_01")
  const [kind, setKind] = useState("tco")
  const [ref, setRef] = useState("fixture://fleet-cost-mark/")
  const save = useMutation({
    mutationFn: () => saveFleetCostMark(packFleetCostWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("tco_01")
      setKind("tco")
      setRef("fixture://fleet-cost-mark/")
      void qc.invalidateQueries({ queryKey: ["fleet-cost-marks", props.organizationId] })
    },
  })

  function submit(event: FormEvent) {
    event.preventDefault()
    if (!props.organizationId) return
    save.mutate()
  }

  return (
    <div className="rounded-md bg-secondary/30 p-4" data-fleet="entry">
      <form className="flex flex-col gap-3 sm:max-w-md" onSubmit={submit}>
        <header>
          <h2 className="text-sm font-semibold">Koszt floty</h2>
          <p className="text-xs text-muted-foreground">
            HITL: TCO / utrzymanie / leasing. Bez TCO SQL i bez CMMS silnika (patrz cmms_mark).
          </p>
        </header>
        <label className="grid gap-1 text-xs">
          Kod
          <input
            aria-label="Kod fleet cost"
            className="h-9 rounded-md border bg-background px-2 font-mono"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="grid gap-1 text-xs">
          Rodzaj (`cost_kind`)
          <select
            aria-label="Rodzaj fleet cost"
            className="h-9 rounded-md border bg-background px-2"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {KINDS.map((row) => (
              <option key={row.id} value={row.id}>
                {row.id} — {row.label}
              </option>
            ))}
          </select>
        </label>
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="Pochodzenie fleet cost"
          value={ref}
          onChange={setRef}
        />
        {save.error ? <CatalogError error={save.error} /> : null}
        <Button disabled={!props.organizationId || save.isPending} type="submit">
          Zapisz fleet cost
        </Button>
      </form>
    </div>
  )
}
