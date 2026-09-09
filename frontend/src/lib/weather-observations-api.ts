import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/weather-observations"

export type WeatherMark = {
  id: string
  organization_id: string
  condition_code: string
  station_unlocode: string
  observed_at: string
  provider_code: string
  source_ref: string
}

export type WeatherMarkWrite = {
  condition_code: string
  station_unlocode: string
  observed_at: string
  provider_code: string
  source_ref: string
}

export function weatherWrite(draft: {
  conditionStamp: string
  stationStamp: string
  observedStamp: string
  providerStamp: string
  originStamp: string
}): WeatherMarkWrite {
  return {
    condition_code: draft.conditionStamp.trim(),
    station_unlocode: draft.stationStamp.trim().toUpperCase(),
    observed_at: draft.observedStamp.trim(),
    provider_code: draft.providerStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

async function parseWeather<T>(res: Response, fallback: string, ok: number): Promise<T> {
  if (res.status !== ok) {
    throw new ApiError(await readApiDetail(res, fallback), httpErrorStatus(res))
  }
  return (await res.json()) as T
}

export async function listWeatherMarks(): Promise<WeatherMark[]> {
  return parseWeather(await fetch(PATH, { headers: requireAuthHeaders() }), "Błąd listy pogody", 200)
}

export async function persistWeatherMark(payload: WeatherMarkWrite): Promise<WeatherMark> {
  const headers = { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" }
  return parseWeather(
    await fetch(PATH, { method: "POST", headers, body: JSON.stringify(payload) }),
    "Błąd zapisu pogody",
    201,
  )
}
