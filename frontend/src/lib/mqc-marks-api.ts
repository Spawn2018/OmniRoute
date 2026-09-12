import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type MqcMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  mqc_kind: string
  source_ref: string
}

export type MqcPayload = {
  mark_code: string
  mqc_kind: string
  source_ref: string
}

const PATH = "/api/v1/mqc-marks"

export function makeMqcPayload(
  code: string,
  kind: string,
  ref: string,
): MqcPayload {
  return {
    mark_code: code.trim(),
    mqc_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadMqcMarks(): Promise<MqcMarkRow[]> {
  const res = await fetch(PATH, { headers: requireAuthHeaders() })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Lista znacznikow MQC niedostepna"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as MqcMarkRow[]
}

export async function createMqcMark(body: MqcPayload): Promise<MqcMarkRow> {
  const res = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Zapis znacznika MQC nieudany"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as MqcMarkRow
}
