import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/network-print-requirements"

export type NetworkPrintRequirementRow = {
  id: string
  organization_id: string
  requirement_code: string
  network_label: string
  source_ref: string
}

export type NetworkPrintRequirementWrite = {
  requirement_code: string
  network_label: string
  source_ref: string
}

export function buildNetworkPrintRequirementWrite(fields: {
  code: string
  label: string
  origin: string
}): NetworkPrintRequirementWrite {
  return {
    requirement_code: fields.code.trim(),
    network_label: fields.label.trim(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchNetworkPrintRequirements(): Promise<NetworkPrintRequirementRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy wymogów wydruku sieci", 200)
}

export async function saveNetworkPrintRequirement(
  body: NetworkPrintRequirementWrite,
): Promise<NetworkPrintRequirementRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu wymogu wydruku sieci", 201)
}
