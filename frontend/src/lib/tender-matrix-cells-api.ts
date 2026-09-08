import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-matrix-cells"

export type CellMark = {
  id: string
  organization_id: string
  tender_id: string
  cell_code: string
  amount: string
  currency: string
  source_ref: string
}

export type CellMarkWrite = {
  tender_id: string
  cell_code: string
  amount: string
  currency: string
  source_ref: string
}

export function cellWrite(draft: {
  boardStamp: string
  codeStamp: string
  cashStamp: string
  ccyStamp: string
  originStamp: string
}): CellMarkWrite {
  return {
    tender_id: draft.boardStamp.trim(),
    cell_code: draft.codeStamp.trim(),
    amount: draft.cashStamp.trim(),
    currency: draft.ccyStamp.trim().toUpperCase(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listCellMarks(): Promise<CellMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(
      await readApiDetail(listed, "Błąd listy komórek matrycy"),
      httpErrorStatus(listed),
    )
  }
  const bag: unknown = await listed.json()
  return bag as CellMark[]
}

export async function persistCellMark(payload: CellMarkWrite): Promise<CellMark> {
  const envelope = JSON.stringify(payload)
  const posted = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "cell-desk",
    },
    body: envelope,
  })
  const denied = posted.status !== 201
  if (denied) {
    const reason = await readApiDetail(posted, "Błąd zapisu komórki matrycy")
    throw new ApiError(reason, httpErrorStatus(posted))
  }
  const cell: unknown = await posted.json()
  return cell as CellMark
}
