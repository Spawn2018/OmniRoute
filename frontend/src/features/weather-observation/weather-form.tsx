import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listWeatherMarks, persistWeatherMark, weatherWrite } from "@/lib/weather-observations-api"

type WeatherDraft = {
  conditionStamp: string
  stationStamp: string
  observedStamp: string
  providerStamp: string
  originStamp: string
}

const EMPTY_WEATHER: WeatherDraft = {
  conditionStamp: "rain",
  stationStamp: "PLGDY",
  observedStamp: "2026-09-09T12:00:00+00:00",
  providerStamp: "hitl",
  originStamp: "fixture://weather-observation/",
}

const CONDITIONS = ["clear", "rain", "snow", "wind", "fog", "ice", "other"] as const

function StampField(args: {
  label: string
  aria: string
  value: string
  onValue: (next: string) => void
}) {
  return (
    <label className="flex flex-col gap-1 text-xs">
      {args.label}
      <input
        aria-label={args.aria}
        className="h-9 rounded-md border bg-background px-2 font-mono"
        value={args.value}
        onChange={(change) => args.onValue(change.target.value)}
        required
      />
    </label>
  )
}

function WeatherFields(args: {
  draft: WeatherDraft
  onChange: (next: WeatherDraft) => void
}) {
  const { draft, onChange } = args
  return (
    <>
      <label className="flex flex-col gap-1 text-xs">
        Warunek (allowlista)
        <select
          aria-label="Warunek pogody"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.conditionStamp}
          onChange={(change) => onChange({ ...draft, conditionStamp: change.target.value })}
          required
        >
          {CONDITIONS.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
      <StampField
        label="Stacja UN/LOCODE"
        aria="Stacja UN/LOCODE"
        value={draft.stationStamp}
        onValue={(stationStamp) => onChange({ ...draft, stationStamp })}
      />
      <StampField
        label="Czas obserwacji (ISO ze strefą)"
        aria="Czas obserwacji pogody"
        value={draft.observedStamp}
        onValue={(observedStamp) => onChange({ ...draft, observedStamp })}
      />
      <StampField
        label="Dostawca (tylko hitl)"
        aria="Dostawca pogody"
        value={draft.providerStamp}
        onValue={(providerStamp) => onChange({ ...draft, providerStamp })}
      />
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://weather-observation/…)"
        ariaLabel="source_ref pogody"
        value={draft.originStamp}
        onChange={(originStamp) => onChange({ ...draft, originStamp })}
      />
    </>
  )
}

function WeatherSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_WEATHER)
  const persist = useMutation({
    mutationFn: () => persistWeatherMark(weatherWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_WEATHER })
      void cache.invalidateQueries({ queryKey: ["weather-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-weather-observation="weather-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Warunek i stacja UN/LOCODE tenanta plus czas ze strefą. Open-Meteo, IMGW i GPS zostają leftover.
        Marża zostaje na `/charges`.
      </p>
      <WeatherFields draft={draft} onChange={setDraft} />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz pogodę
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function WeatherRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["weather-marks", args.organizationId],
    queryFn: listWeatherMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-weather-observation="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.condition_code} {row.station_unlocode} {row.observed_at}
          </li>
        ))}
      </ul>
    </>
  )
}

export function WeatherPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <WeatherSave organizationId={args.organizationId} />
      <WeatherRows organizationId={args.organizationId} />
    </div>
  )
}
