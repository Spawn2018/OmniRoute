import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type InventoryFinanceMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  finance_kind: string
  source_ref: string
}

export type InventoryFinanceMarkPayload = {
  mark_code: string
  finance_kind: string
  source_ref: string
}

const PATH = "/api/v1/inventory-finance-marks"

export function buildInventoryFinanceMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): InventoryFinanceMarkPayload {
  return {
    mark_code: args.code.trim(),
    finance_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchInventoryFinanceMarks(): Promise<InventoryFinanceMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu zapasu finansowego"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as InventoryFinanceMarkRow[]
}

export async function saveInventoryFinanceMark(
  payload: InventoryFinanceMarkPayload,
): Promise<InventoryFinanceMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "inventory-finance-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika zapasu finansowego"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as InventoryFinanceMarkRow
}
