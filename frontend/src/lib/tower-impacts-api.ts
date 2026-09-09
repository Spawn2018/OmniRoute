import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tower-impacts"

export type ImpactMark = {
  id: string
  organization_id: string
  chain_stage: string
  contract_data_status: string
  source_ref: string
  contract_gap_label: string | null
}

export type ImpactMarkWrite = {
  chain_stage: string
  contract_data_status: string
  source_ref: string
}

export function impactWrite(draft: {
  stageStamp: string
  pactStamp: string
  originStamp: string
}): ImpactMarkWrite {
  return {
    chain_stage: draft.stageStamp.trim(),
    contract_data_status: draft.pactStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listImpactMarks(): Promise<ImpactMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status === 200) {
    return (await listed.json()) as ImpactMark[]
  }
  throw new ApiError(await readApiDetail(listed, "Błąd listy skutków wieży"), httpErrorStatus(listed))
}

export async function persistImpactMark(payload: ImpactMarkWrite): Promise<ImpactMark> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status === 201) {
    return (await posted.json()) as ImpactMark
  }
  throw new ApiError(await readApiDetail(posted, "Błąd zapisu skutku wieży"), httpErrorStatus(posted))
}
