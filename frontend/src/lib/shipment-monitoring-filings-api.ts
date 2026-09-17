import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/shipment-monitoring-filings"

export type ShipmentMonitoringFilingRow = {
  id: string
  organization_id: string
  filing_code: string
  status_kind: string
  source_ref: string
}

export type ShipmentMonitoringFilingWrite = {
  filing_code: string
  status_kind: string
  source_ref: string
}

export function buildShipmentMonitoringFilingWrite(fields: {
  code: string
  kind: string
  origin: string
}): ShipmentMonitoringFilingWrite {
  return {
    filing_code: fields.code.trim(),
    status_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchShipmentMonitoringFilings(): Promise<ShipmentMonitoringFilingRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Blad listy znacznikow zgloszenia SENT/BDO", 200)
}

export async function saveShipmentMonitoringFiling(
  body: ShipmentMonitoringFilingWrite,
): Promise<ShipmentMonitoringFilingRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Blad zapisu znacznika zgloszenia SENT/BDO", 201)
}
