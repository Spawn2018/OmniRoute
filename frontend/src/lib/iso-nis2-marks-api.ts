import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type IsoNis2MarkRow = {
  id: string
  organization_id: string
  mark_code: string
  ops_kind: string
  source_ref: string
}

export type IsoNis2Payload = {
  mark_code: string
  ops_kind: string
  source_ref: string
}

const ROUTE = "/api/v1/iso-nis2-marks"

export function makeIsoNis2Payload(
  code: string,
  kind: string,
  ref: string,
): IsoNis2Payload {
  return {
    mark_code: code.trim(),
    ops_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadIsoNis2Marks(): Promise<IsoNis2MarkRow[]> {
  const bag = await fetch(ROUTE, { headers: requireAuthHeaders() })
  if (bag.ok) {
    return (await bag.json()) as IsoNis2MarkRow[]
  }
  throw new ApiError(
    await readApiDetail(bag, "Lista znacznikow ISO/NIS2 niedostepna"),
    httpErrorStatus(bag),
  )
}

export async function createIsoNis2Mark(
  payload: IsoNis2Payload,
): Promise<IsoNis2MarkRow> {
  const bag = await fetch(ROUTE, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (bag.status === 201) {
    return (await bag.json()) as IsoNis2MarkRow
  }
  throw new ApiError(
    await readApiDetail(bag, "Zapis znacznika ISO/NIS2 nieudany"),
    httpErrorStatus(bag),
  )
}
