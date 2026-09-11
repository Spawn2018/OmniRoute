import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { makeFuelAnomalyBody, postFuelAnomalyMark } from "@/lib/fuel-anomaly-marks-api"

const OPTIONS = [
  ["card", "karta paliwowa"],
  ["tank", "zbiornik"],
  ["spike", "skok zużycia"],
  ["other", "inny"],
] as const

export function FuelAnomalyIntake(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [mark, setMark] = useState("card_01")
  const [kind, setKind] = useState("card")
  const [origin, setOrigin] = useState("fixture://fuel-anomaly-mark/")
  const write = useMutation({
    mutationFn: () => postFuelAnomalyMark(makeFuelAnomalyBody(mark, kind, origin)),
    onSuccess: () => {
      setMark("card_01")
      setKind("card")
      setOrigin("fixture://fuel-anomaly-mark/")
      void qc.invalidateQueries({ queryKey: ["fuel-anomaly-marks", props.organizationId] })
    },
  })

  function onSubmit(event: FormEvent) {
    event.preventDefault()
    if (props.organizationId == null) return
    write.mutate()
  }

  return (
    <form
      className="mx-auto max-w-sm space-y-3 border-l-2 border-primary/40 pl-4"
      data-fuel="intake"
      onSubmit={onSubmit}
    >
      <p className="text-sm font-medium">Karta / anomalia paliwa</p>
      <p className="text-xs text-muted-foreground">
        HITL: karta, zbiornik albo skok. Bez live fuel card i bez telemetry.
      </p>
      <label className="grid gap-1 text-xs">
        Kod znacznika
        <input
          aria-label="Kod fuel anomaly"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(e) => setMark(e.target.value)}
          required
          value={mark}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Rodzaj (`anomaly_kind`)
        <select
          aria-label="Rodzaj fuel anomaly"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(e) => setKind(e.target.value)}
          value={kind}
        >
          {OPTIONS.map(([id, pl]) => (
            <option key={id} value={id}>
              {id} — {pl}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="Pochodzenie fuel anomaly"
        value={origin}
        onChange={setOrigin}
      />
      {write.error ? <CatalogError error={write.error} /> : null}
      <Button disabled={props.organizationId == null || write.isPending} type="submit">
        Zapisz znacznik
      </Button>
    </form>
  )
}
