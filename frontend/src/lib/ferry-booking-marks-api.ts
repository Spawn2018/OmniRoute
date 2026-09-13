import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type FerryBookingMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  booking_kind: string
  source_ref: string
}

export type FerryBookingMarkPayload = {
  mark_code: string
  booking_kind: string
  source_ref: string
}

const DESK = "/api/v1/ferry-booking-marks"

export function makeFerryBookingMarkPayload(
  markCode: string,
  bookingKind: string,
  sourceRef: string,
): FerryBookingMarkPayload {
  return {
    mark_code: markCode.trim(),
    booking_kind: bookingKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadFerryBookingMarks(): Promise<FerryBookingMarkRow[]> {
  const response = await fetch(DESK, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Nie udało się wczytać katalogu rezerwacji promu"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as FerryBookingMarkRow[]
}

export async function createFerryBookingMark(
  payload: FerryBookingMarkPayload,
): Promise<FerryBookingMarkRow> {
  const response = await fetch(DESK, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "ferry-booking-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Nie udało się zapisać znacznika rezerwacji promu"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as FerryBookingMarkRow
}
