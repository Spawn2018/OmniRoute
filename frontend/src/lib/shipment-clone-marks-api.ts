import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ShipmentCloneMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  clone_kind: string
  source_ref: string
}

export type ShipmentCloneMarkPayload = {
  mark_code: string
  clone_kind: string
  source_ref: string
}

const PATH = "/api/v1/shipment-clone-marks"

export function buildShipmentCloneMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): ShipmentCloneMarkPayload {
  return {
    mark_code: args.code.trim(),
    clone_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchShipmentCloneMarks(): Promise<ShipmentCloneMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu intencji klonu"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as ShipmentCloneMarkRow[]
}

export async function saveShipmentCloneMark(
  payload: ShipmentCloneMarkPayload,
): Promise<ShipmentCloneMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "shipment-clone-mark-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika intencji klonu"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as ShipmentCloneMarkRow
}
