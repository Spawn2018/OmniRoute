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

export async function listErpConnectors(): Promise<ErpConnectorRow[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(await readApiDetail(listed, "Błąd listy konektorów Optima"), httpErrorStatus(listed))
  }
  return (await listed.json()) as ErpConnectorRow[]
}

export async function persistErpConnector(payload: ErpConnectorWrite): Promise<ErpConnectorRow> {
  const saved = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (saved.status !== 201) {
    throw new ApiError(await readApiDetail(saved, "Błąd zapisu konektora Optima"), httpErrorStatus(saved))
  }
  return (await saved.json()) as ErpConnectorRow
}
