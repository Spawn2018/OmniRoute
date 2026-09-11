import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/sap-connectors"

export type SapConnectorRow = {
  id: string
  organization_id: string
  connector_code: string
  system_kind: string
  source_ref: string
}

export type SapConnectorBody = {
  connector_code: string
  system_kind: string
  source_ref: string
}

export function sapConnectorBody(draft: {
  connectorSlug: string
  systemKind: string
  originPointer: string
}): SapConnectorBody {
  return {
    connector_code: draft.connectorSlug.trim(),
    system_kind: draft.systemKind.trim().toLowerCase(),
    source_ref: draft.originPointer.trim(),
  }
}

async function readJson<T>(response: Response, fallback: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
}

export async function listSapConnectors(): Promise<SapConnectorRow[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  return readJson(listed, "Błąd listy konektorów SAP/Oracle", 200)
}

export async function persistSapConnector(payload: SapConnectorBody): Promise<SapConnectorRow> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  return readJson(posted, "Błąd zapisu konektora SAP/Oracle", 201)
}
