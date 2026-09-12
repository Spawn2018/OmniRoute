import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const BASE = "/api/v1/e-delivery-marks"

export type EDeliveryMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  delivery_kind: string
  source_ref: string
}

export type EDeliveryWriteBody = {
  mark_code: string
  delivery_kind: string
  source_ref: string
}

export function buildEDeliveryBody(
  markCode: string,
  deliveryKind: string,
  sourceRef: string,
): EDeliveryWriteBody {
  return {
    mark_code: markCode.trim(),
    delivery_kind: deliveryKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function listEDeliveryMarks(): Promise<EDeliveryMarkRow[]> {
  const response = await fetch(BASE, { headers: requireAuthHeaders() })
  if (response.status !== 200) {
    throw new ApiError(
      await readApiDetail(response, "Nie udało się wczytać katalogu e-Doręczeń"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as EDeliveryMarkRow[]
}

export async function saveEDeliveryMark(
  payload: EDeliveryWriteBody,
): Promise<EDeliveryMarkRow> {
  const response = await fetch(BASE, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Nie udało się zapisać znacznika e-Doręczeń"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as EDeliveryMarkRow
}
