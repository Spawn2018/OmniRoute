import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/telematics-devices"

export type TelematicsDeviceRow = {
  id: string
  organization_id: string
  device_code: string
  device_kind: string
  source_ref: string
}

export type TelematicsDeviceWrite = {
  device_code: string
  device_kind: string
  source_ref: string
}

export function buildTelematicsDeviceWrite(fields: {
  code: string
  kind: string
  origin: string
}): TelematicsDeviceWrite {
  return {
    device_code: fields.code.trim(),
    device_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchTelematicsDevices(): Promise<TelematicsDeviceRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy urządzeń telematycznych", 200)
}

export async function saveTelematicsDevice(
  body: TelematicsDeviceWrite,
): Promise<TelematicsDeviceRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu urządzenia telematycznego", 201)
}
