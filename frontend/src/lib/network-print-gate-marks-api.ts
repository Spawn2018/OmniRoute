import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type NetworkPrintGateMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  gate_kind: string
  source_ref: string
}

export type NetworkPrintGateMarkWrite = {
  mark_code: string
  gate_kind: string
  source_ref: string
}

const ROOT = "/api/v1/network-print-gate-marks" as const

function authJsonHeaders(): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    "Content-Type": "application/json",
  }
}

export function buildNetworkPrintGateMarkWrite(
  code: string,
  kind: string,
  origin: string,
): NetworkPrintGateMarkWrite {
  return {
    mark_code: code.trim(),
    gate_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function decodeOk<T>(response: Response, whenFail: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
}

export async function fetchNetworkPrintGateMarks(): Promise<NetworkPrintGateMarkRow[]> {
  const response = await fetch(ROOT, { headers: requireAuthHeaders() })
  return decodeOk(response, "Błąd listy bramy wydruku sieci", 200)
}

export async function saveNetworkPrintGateMark(
  payload: NetworkPrintGateMarkWrite,
): Promise<NetworkPrintGateMarkRow> {
  const response = await fetch(ROOT, {
    method: "POST",
    headers: authJsonHeaders(),
    body: JSON.stringify(payload),
  })
  return decodeOk(response, "Błąd zapisu bramy wydruku sieci", 201)
}
