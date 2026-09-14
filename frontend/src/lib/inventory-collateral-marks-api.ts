import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type InventoryCollateralMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  collateral_kind: string
  source_ref: string
}

export type InventoryCollateralMarkPayload = {
  mark_code: string
  collateral_kind: string
  source_ref: string
}

const PATH = "/api/v1/inventory-collateral-marks"

export function buildInventoryCollateralMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): InventoryCollateralMarkPayload {
  return {
    mark_code: args.code.trim(),
    collateral_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchInventoryCollateralMarks(): Promise<
  InventoryCollateralMarkRow[]
> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu zabezpieczenia"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as InventoryCollateralMarkRow[]
}

export async function saveInventoryCollateralMark(
  payload: InventoryCollateralMarkPayload,
): Promise<InventoryCollateralMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "inventory-collateral-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika zabezpieczenia"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as InventoryCollateralMarkRow
}
