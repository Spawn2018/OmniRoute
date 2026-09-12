import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type PhytoAtaMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  permit_kind: string
  source_ref: string
}

export type PhytoAtaPayload = {
  mark_code: string
  permit_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/phyto-ata-marks"

export function makePhytoAtaPayload(
  markCode: string,
  permitKind: string,
  sourceRef: string,
): PhytoAtaPayload {
  return {
    mark_code: markCode.trim(),
    permit_kind: permitKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadPhytoAtaMarks(): Promise<PhytoAtaMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Lista pozwolen phyto/ATA niedostepna"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as PhytoAtaMarkRow[]
}

export async function createPhytoAtaMark(
  payload: PhytoAtaPayload,
): Promise<PhytoAtaMarkRow> {
  const response = await fetch(ENDPOINT, {
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
      await readApiDetail(response, "Zapis pozwolenia phyto/ATA nieudany"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as PhytoAtaMarkRow
}
