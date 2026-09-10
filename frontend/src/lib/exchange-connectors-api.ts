import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const BOARD_PATH = "/api/v1/exchange-connectors"

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

async function readBoardJson<T>(response: Response, fallback: string, ok: number): Promise<T> {
  const status = response.status
  if (status === ok) {
    return (await response.json()) as T
  }
  const detail = await readApiDetail(response, fallback)
  throw new ApiError(detail, httpErrorStatus(response))
}

export async function listExchangeConnectors(): Promise<ExchangeConnectorRow[]> {
  const listed = await fetch(BOARD_PATH, { headers: requireAuthHeaders() })
  return readBoardJson(listed, "Błąd listy konektorów giełdy", 200)
}

export async function persistExchangeConnector(
  payload: ExchangeConnectorWrite,
): Promise<ExchangeConnectorRow> {
  const posted = await fetch(BOARD_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  return readBoardJson(posted, "Błąd zapisu konektora giełdy", 201)
}
