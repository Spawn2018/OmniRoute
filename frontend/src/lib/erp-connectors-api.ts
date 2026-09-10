import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/erp-connectors"

export type ErpConnectorRow = {
  id: string
  organization_id: string
  connector_code: string
  system_kind: string
  source_ref: string
}

export type ErpConnectorWrite = {
  connector_code: string
  system_kind: string
  source_ref: string
}

export function erpConnectorWrite(draft: {
  codeStamp: string
  kindStamp: string
  originStamp: string
}): ErpConnectorWrite {
  return {
    connector_code: draft.codeStamp.trim(),
    system_kind: draft.kindStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

async function parseErpConnector<T>(res: Response, fallback: string, ok: number): Promise<T> {
  if (res.status !== ok) {
    throw new ApiError(await readApiDetail(res, fallback), httpErrorStatus(res))
  }
  return (await res.json()) as T
}

export async function listErpConnectors(): Promise<ErpConnectorRow[]> {
  return parseErpConnector(
    await fetch(PATH, { headers: requireAuthHeaders() }),
    "Błąd listy konektorów Optima",
    200,
  )
}

export async function persistErpConnector(payload: ErpConnectorWrite): Promise<ErpConnectorRow> {
  return parseErpConnector(
    await fetch(PATH, {
      method: "POST",
      headers: { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),
    "Błąd zapisu konektora Optima",
    201,
  )
}
