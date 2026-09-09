import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/telematics-connectors"

export type ConnectorMark = {
  id: string
  organization_id: string
  observation_kind: string
  provider_code: string
  source_ref: string
}

export type ConnectorMarkWrite = {
  observation_kind: string
  provider_code: string
  source_ref: string
}

export function connectorWrite(draft: {
  kindStamp: string
  providerStamp: string
  originStamp: string
}): ConnectorMarkWrite {
  return {
    observation_kind: draft.kindStamp.trim(),
    provider_code: draft.providerStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

async function parseConnector<T>(res: Response, fallback: string, ok: number): Promise<T> {
  if (res.status !== ok) {
    throw new ApiError(await readApiDetail(res, fallback), httpErrorStatus(res))
  }
  return (await res.json()) as T
}

export async function listConnectorMarks(): Promise<ConnectorMark[]> {
  return parseConnector(
    await fetch(PATH, { headers: requireAuthHeaders() }),
    "Błąd listy konektorów GPS",
    200,
  )
}

export async function persistConnectorMark(payload: ConnectorMarkWrite): Promise<ConnectorMark> {
  const headers = { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" }
  return parseConnector(
    await fetch(PATH, { method: "POST", headers, body: JSON.stringify(payload) }),
    "Błąd zapisu konektora GPS",
    201,
  )
}
