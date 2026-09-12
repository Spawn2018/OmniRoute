import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type LabelParkingMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  parking_kind: string
  source_ref: string
}

export type LabelParkingMarkPayload = {
  mark_code: string
  parking_kind: string
  source_ref: string
}

const LABEL_PARKING_URL = "/api/v1/label-parking-marks"

export function makeLabelParkingMarkPayload(
  markCode: string,
  lezKind: string,
  sourceRef: string,
): LabelParkingMarkPayload {
  return {
    mark_code: markCode.trim(),
    parking_kind: lezKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadLabelParkingMarks(): Promise<LabelParkingMarkRow[]> {
  const res = await fetch(LABEL_PARKING_URL, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Katalog LABEL parking niedostepny"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as LabelParkingMarkRow[]
}

export async function createLabelParkingMark(payload: LabelParkingMarkPayload): Promise<LabelParkingMarkRow> {
  const res = await fetch(LABEL_PARKING_URL, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "label-parking-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Zapis LABEL parking odrzucony"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as LabelParkingMarkRow
}
