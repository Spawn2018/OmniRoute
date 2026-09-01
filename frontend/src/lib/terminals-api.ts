import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type Terminal = {
  id: string
  organization_id: string
  port_id: string
  name: string
  isps_code: string | null
  operator_name: string | null
  operator_party_id: string | null
  lat: string | null
  lng: string | null
  source_ref: string
}

export type TerminalCreateBody = {
  port_id: string
  name: string
  isps_code: string | null
  operator_name: string | null
  operator_party_id: string | null
}

export function terminalCreateBody(args: {
  portId: string
  name: string
  ispsCode: string
  operatorName: string
  operatorPartyId?: string
}): TerminalCreateBody {
  const isps = args.ispsCode.trim().toUpperCase()
  const operator = args.operatorName.trim()
  const partyId = (args.operatorPartyId ?? "").trim()
  return {
    port_id: args.portId,
    name: args.name.trim(),
    isps_code: isps === "" ? null : isps,
    operator_name: operator === "" ? null : operator,
    operator_party_id: partyId === "" ? null : partyId,
  }
}

async function readTerminal(response: Response, fallback: string): Promise<Terminal> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as Terminal
}

export async function fetchTerminals(portId: string): Promise<Terminal[]> {
  const trimmed = portId.trim()
  const query =
    trimmed === "" ? "" : `?${new URLSearchParams({ port_id: trimmed }).toString()}`
  const response = await fetch(`/api/v1/terminals${query}`, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy terminali"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as Terminal[]
}

export async function createTerminal(body: TerminalCreateBody): Promise<Terminal> {
  const response = await fetch("/api/v1/terminals", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readTerminal(response, "Błąd zapisu terminalu")
}

export async function resolveTerminal(ispsCode: string): Promise<Terminal> {
  const params = new URLSearchParams({ isps_code: ispsCode })
  const response = await fetch(`/api/v1/terminals/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return readTerminal(response, "Nieznany terminal")
}
