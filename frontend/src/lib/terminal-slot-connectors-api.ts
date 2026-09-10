import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const SLOT_PATH = "/api/v1/terminal-slot-connectors"

export type SlotConnectorRecord = {
  id: string
  organization_id: string
  connector_code: string
  terminal_code: string
  mode: string
  opens_local: string
  closes_local: string
  cutoff_local: string
  source_ref: string
}

export type SlotConnectorPayload = {
  connector_code: string
  terminal_code: string
  mode: string
  opens_local: string
  closes_local: string
  cutoff_local: string
  source_ref: string
}

export function toSlotWrite(draft: {
  slotKey: string
  gateToken: string
  regime: string
  openStamp: string
  closeStamp: string
  cutStamp: string
  originHint: string
}): SlotConnectorPayload {
  return {
    connector_code: draft.slotKey.trim(),
    terminal_code: draft.gateToken.trim(),
    mode: draft.regime.trim(),
    opens_local: draft.openStamp.trim(),
    closes_local: draft.closeStamp.trim(),
    cutoff_local: draft.cutStamp.trim(),
    source_ref: draft.originHint.trim(),
  }
}

export async function loadSlotConnectors(): Promise<SlotConnectorRecord[]> {
  const listed = await fetch(SLOT_PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(
      await readApiDetail(listed, "Błąd listy konektorów slotu"),
      httpErrorStatus(listed),
    )
  }
  return (await listed.json()) as SlotConnectorRecord[]
}

export async function persistTerminalSlotConnector(
  payload: SlotConnectorPayload,
): Promise<SlotConnectorRecord> {
  const saved = await fetch(SLOT_PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (saved.status !== 201) {
    throw new ApiError(
      await readApiDetail(saved, "Błąd zapisu konektora slotu"),
      httpErrorStatus(saved),
    )
  }
  return (await saved.json()) as SlotConnectorRecord
}
