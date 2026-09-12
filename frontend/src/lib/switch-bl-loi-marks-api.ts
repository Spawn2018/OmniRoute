import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type SwitchBlLoiMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  instrument_kind: string
  source_ref: string
}

export type SwitchBlLoiPayload = {
  mark_code: string
  instrument_kind: string
  source_ref: string
}

const LIST_PATH = "/api/v1/switch-bl-loi-marks"

function authJsonHeaders(): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    "Content-Type": "application/json",
  }
}

export function makeSwitchBlLoiPayload(
  markCode: string,
  instrumentKind: string,
  sourceRef: string,
): SwitchBlLoiPayload {
  const mark_code = markCode.trim()
  const instrument_kind = instrumentKind.trim().toLowerCase()
  const source_ref = sourceRef.trim()
  return { mark_code, instrument_kind, source_ref }
}

export async function loadSwitchBlLoiMarks(): Promise<SwitchBlLoiMarkRow[]> {
  const response = await fetch(LIST_PATH, { headers: requireAuthHeaders() })
  if (response.ok) {
    return (await response.json()) as SwitchBlLoiMarkRow[]
  }
  const detail = await readApiDetail(response, "Lista instrumentow BL/LOI niedostepna")
  throw new ApiError(detail, httpErrorStatus(response))
}

export async function createSwitchBlLoiMark(
  payload: SwitchBlLoiPayload,
): Promise<SwitchBlLoiMarkRow> {
  const response = await fetch(LIST_PATH, {
    method: "POST",
    headers: authJsonHeaders(),
    body: JSON.stringify(payload),
  })
  if (response.status === 201) {
    return (await response.json()) as SwitchBlLoiMarkRow
  }
  const detail = await readApiDetail(response, "Zapis instrumentu BL/LOI nieudany")
  throw new ApiError(detail, httpErrorStatus(response))
}
