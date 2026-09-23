import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildTripVarianceMarkWrite,
  saveTripVarianceMark,
} from "@/lib/trip-variance-marks-api"

const VARIANCE_OPTIONS = ["expected", "actual", "gap", "other"] as const

export function TripVarianceMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("var_expected_01")
  const [kind, setKind] = useState<string>("expected")
  const [ref, setRef] = useState("fixture://trip-variance/")
  const save = useMutation({
    mutationFn: () =>
      saveTripVarianceMark(buildTripVarianceMarkWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("var_expected_01")
      setKind("expected")
      setRef("fixture://trip-variance/")
      void cache.invalidateQueries({
        queryKey: ["trip-variance-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-3"
      data-trip-variance-mark="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance wariancji przejazdu jako dana HITL — nie SQL na charge i nie druga marża.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod wariancji przejazdu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>variance_kind</legend>
        {VARIANCE_OPTIONS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="trip-variance-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://trip-variance/…)"
        ariaLabel="Pochodzenie wariancji przejazdu"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz wariancja przekazania
      </Button>
    </form>
  )
}
