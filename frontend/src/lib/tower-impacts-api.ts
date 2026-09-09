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

async function parseImpact<T>(res: Response, fallback: string, ok: number): Promise<T> {
  if (res.status !== ok) {
    throw new ApiError(await readApiDetail(res, fallback), httpErrorStatus(res))
  }
  return (await res.json()) as T
}

export async function listImpactMarks(): Promise<ImpactMark[]> {
  return parseImpact(
    await fetch(PATH, { headers: requireAuthHeaders() }),
    "Błąd listy skutków wieży",
    200,
  )
}

export async function persistImpactMark(payload: ImpactMarkWrite): Promise<ImpactMark> {
  const headers = { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" }
  return parseImpact(
    await fetch(PATH, { method: "POST", headers, body: JSON.stringify(payload) }),
    "Błąd zapisu skutku wieży",
    201,
  )
}
