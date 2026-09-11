import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { draftWhatIfMark, postWhatIfMark } from "@/lib/what-if-marks-api"

const SCENARIOS: ReadonlyArray<{ value: string; pl: string }> = [
  { value: "fuel", pl: "paliwo" },
  { value: "port", pl: "port" },
  { value: "bankruptcy", pl: "bankructwo" },
  { value: "other", pl: "inny" },
]

const DEFAULT_REF = "fixture://what-if-mark/"

export function WhatIfMarkComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [code, setCode] = useState("fuel_spike_01")
  const [scenario, setScenario] = useState("fuel")
  const [origin, setOrigin] = useState(DEFAULT_REF)
  const save = useMutation({
    mutationFn: async () =>
      postWhatIfMark(draftWhatIfMark({ mark: code, scenario, ref: origin })),
    onSuccess: () => {
      setCode("fuel_spike_01")
      setScenario("fuel")
      setOrigin(DEFAULT_REF)
      void qc.invalidateQueries({ queryKey: ["what-if-marks", props.organizationId] })
    },
  })

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (props.organizationId == null) return
    save.mutate()
  }

  return (
    <fieldset className="max-w-lg space-y-3 rounded-md border border-dashed p-3" data-wif="composer">
      <legend className="px-1 text-sm font-medium">Nowy scenariusz HITL</legend>
      <p className="text-xs text-muted-foreground">
        Etykieta scenariusza what-if (paliwo / port / bankructwo). Bez silnika i bez mutacji
        plan_snapshot.
      </p>
      <form className="grid gap-3 sm:grid-cols-2" onSubmit={submit}>
        <label className="grid gap-1 text-xs sm:col-span-1">
          Kod
          <input
            aria-label="Kod znacznika what-if"
            className="h-9 rounded-md border bg-background px-2 font-mono"
            onChange={(event) => setCode(event.target.value)}
            required
            value={code}
          />
        </label>
        <label className="grid gap-1 text-xs sm:col-span-1">
          Scenariusz (`scenario_kind`)
          <select
            aria-label="Rodzaj scenariusza what-if"
            className="h-9 rounded-md border bg-background px-2"
            onChange={(event) => setScenario(event.target.value)}
            value={scenario}
          >
            {SCENARIOS.map((row) => (
              <option key={row.value} value={row.value}>
                {row.value} — {row.pl}
              </option>
            ))}
          </select>
        </label>
        <div className="sm:col-span-2">
          <CatalogSourceRefField
            label="source_ref"
            ariaLabel="Pochodzenie what-if"
            value={origin}
            onChange={setOrigin}
          />
        </div>
        {save.error ? <CatalogError error={save.error} /> : null}
        <div className="sm:col-span-2">
          <Button disabled={props.organizationId == null || save.isPending} type="submit">
            Zapisz scenariusz
          </Button>
        </div>
      </form>
    </fieldset>
  )
}
