import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/exchange-connectors"

export type ExchangeConnectorRow = {
  id: string
  organization_id: string
  connector_code: string
  system_kind: string
  source_ref: string
}

export type ExchangeConnectorWrite = {
  connector_code: string
  system_kind: string
  source_ref: string
}

export function exchangeBoardWrite(draft: {
  boardMark: string
  kindToken: string
  originHint: string
}): ExchangeConnectorWrite {
  return {
    connector_code: draft.boardMark.trim(),
    system_kind: draft.kindToken.trim(),
    source_ref: draft.originHint.trim(),
  }
}

export async function listExchangeConnectors(): Promise<ExchangeConnectorRow[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(await readApiDetail(listed, "Błąd listy konektorów giełdy"), httpErrorStatus(listed))
  }
  return (await listed.json()) as ExchangeConnectorRow[]
}

export async function persistExchangeConnector(payload: ExchangeConnectorWrite): Promise<ExchangeConnectorRow> {
  const saved = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (saved.status !== 201) {
    throw new ApiError(await readApiDetail(saved, "Błąd zapisu konektora giełdy"), httpErrorStatus(saved))
  }
  return (await saved.json()) as ExchangeConnectorRow
}
