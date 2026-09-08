import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/dock-appointments"

export type DockRow = {
  id: string
  organization_id: string
  shipment_id: string
  stop_id: string
  appointment_code: string
  appointment_status: string
  window_date: string
  window_start_local: string
  window_end_local: string
  source_ref: string
}

export type DockWrite = {
  shipment_id: string
  stop_id: string
  appointment_code: string
  appointment_status: string
  window_date: string
  window_start_local: string
  window_end_local: string
  source_ref: string
}

export function dockWrite(args: {
  orderKey: string
  haltRef: string
  slotToken: string
  stageMark: string
  dayMark: string
  openMark: string
  closeMark: string
  originNote: string
}): DockWrite {
  return {
    shipment_id: args.orderKey.trim(),
    stop_id: args.haltRef.trim(),
    appointment_code: args.slotToken.trim(),
    appointment_status: args.stageMark.trim(),
    window_date: args.dayMark.trim(),
    window_start_local: args.openMark.trim(),
    window_end_local: args.closeMark.trim(),
    source_ref: args.originNote.trim(),
  }
}

export async function listDocks(): Promise<DockRow[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy awizacji"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as DockRow[]
}

export async function persistDock(payload: DockWrite): Promise<DockRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "dock-window",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd awizacji doku"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as DockRow
}
