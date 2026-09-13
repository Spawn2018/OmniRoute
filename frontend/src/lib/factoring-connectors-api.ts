import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/factoring-connectors"

export type FactoringConnectorRow = {
  id: string
  organization_id: string
  connector_code: string
  system_kind: string
  source_ref: string
}

export type FactoringConnectorWrite = {
  connector_code: string
  system_kind: string
  source_ref: string
}

export function factoringConnectorWrite(draft: {
  codeStamp: string
  kindStamp: string
  originStamp: string
}): FactoringConnectorWrite {
  return {
    connector_code: draft.codeStamp.trim(),
    system_kind: draft.kindStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listFactoringConnectors(): Promise<FactoringConnectorRow[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(
      await readApiDetail(listed, "Błąd listy konektorów faktoringu"),
      httpErrorStatus(listed),
    )
  }
  return (await listed.json()) as FactoringConnectorRow[]
}

export async function persistFactoringConnector(
  payload: FactoringConnectorWrite,
): Promise<FactoringConnectorRow> {
  const saved = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (saved.status !== 201) {
    throw new ApiError(
      await readApiDetail(saved, "Błąd zapisu konektora faktoringu"),
      httpErrorStatus(saved),
    )
  }
  return (await saved.json()) as FactoringConnectorRow
}
