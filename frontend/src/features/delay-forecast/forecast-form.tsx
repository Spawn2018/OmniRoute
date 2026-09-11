import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildDelayWrite, saveDelayForecast } from "@/lib/delay-forecasts-api"

export function DelayForecastSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("late_24h_01")
  const [hours, setHours] = useState("24")
  const [chance, setChance] = useState("0.3500")
  const [origin, setOrigin] = useState("fixture://delay-forecast/")
  const save = useMutation({
    mutationFn: () => saveDelayForecast(buildDelayWrite({ code, hours, chance, origin })),
    onSuccess: () => {
      setCode("late_24h_01")
      setHours("24")
      setChance("0.3500")
      setOrigin("fixture://delay-forecast/")
      void cache.invalidateQueries({ queryKey: ["delay-forecasts", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-delay-forecast="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Prognoza opóźnienia jako katalog HITL. p_late to dana Decimal, nie wróżba i nie GPS.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod prognozy opóźnienia"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Horyzont (godziny 1–168)
        <input
          aria-label="Horyzont prognozy w godzinach"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setHours(change.target.value)}
          required
          value={hours}
        />
      </label>
      <label className="grid gap-1 text-xs">
        p_late (Decimal 0–1)
        <input
          aria-label="Prawdopodobieństwo spóźnienia"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setChance(change.target.value)}
          required
          value={chance}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://delay-forecast/…)"
        ariaLabel="Pochodzenie prognozy opóźnienia"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz prognozę opóźnienia
      </Button>
    </form>
  )
}
