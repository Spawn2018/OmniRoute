import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type BookingInstructionRow = {
  id: string
  organization_id: string
  shipment_id: string
  booking_scope: string
  target_role: string
  status: string
  source_ref: string
  superseded_by: string | null
}

export type BookingInstructionCreateBody = {
  shipment_id: string
  booking_scope: string
  target_role: string
  status: string
  source_ref: string
}

const PATH = "/api/v1/booking-instructions"

export function bookingInstructionBody(args: {
  shipmentId: string
  bookingScope: string
  targetRole: string
  status: string
}): BookingInstructionCreateBody {
  return {
    shipment_id: args.shipmentId.trim(),
    booking_scope: args.bookingScope.trim(),
    target_role: args.targetRole.trim(),
    status: args.status.trim(),
    source_ref: "tenant:manual",
  }
}

export async function fetchBookingInstructions(shipmentId: string): Promise<BookingInstructionRow[]> {
  const url = `${PATH}?shipment_id=${encodeURIComponent(shipmentId)}`
  const reply = await fetch(url, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy instrukcji bookingu"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as BookingInstructionRow[]
}

export async function saveBookingInstruction(
  payload: BookingInstructionCreateBody,
): Promise<BookingInstructionRow> {
  const auth = requireAuthHeaders()
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      Authorization: auth.Authorization,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu instrukcji bookingu"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as BookingInstructionRow
}
