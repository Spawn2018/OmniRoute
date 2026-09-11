import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/delay-forecasts"

export type DelayForecastRow = {
  id: string
  organization_id: string
  forecast_code: string
  horizon_hours: number
  p_late: string
  source_ref: string
}

export type DelayForecastWrite = {
  forecast_code: string
  horizon_hours: number
  p_late: string
  source_ref: string
}

export function buildDelayWrite(fields: {
  code: string
  hours: string
  chance: string
  origin: string
}): DelayForecastWrite {
  return {
    forecast_code: fields.code.trim(),
    horizon_hours: Number.parseInt(fields.hours.trim(), 10),
    p_late: fields.chance.trim(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchDelayForecasts(): Promise<DelayForecastRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy prognoz opóźnienia", 200)
}

export async function saveDelayForecast(body: DelayForecastWrite): Promise<DelayForecastRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu prognozy opóźnienia", 201)
}
