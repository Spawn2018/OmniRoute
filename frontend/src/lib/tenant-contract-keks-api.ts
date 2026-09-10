import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const MARK_PATH = "/api/v1/tenant-contract-keks"

export type KekMarkRow = {
  id: string
  organization_id: string
  kek_code: string
  wrap_kind: string
  source_ref: string
}

export type KekMarkWrite = {
  kek_code: string
  wrap_kind: string
  source_ref: string
}

export function kekMarkWrite(draft: {
  markSlug: string
  wrapToken: string
  originRef: string
}): KekMarkWrite {
  return {
    kek_code: draft.markSlug.trim(),
    wrap_kind: draft.wrapToken.trim(),
    source_ref: draft.originRef.trim(),
  }
}

async function parseKekJson<T>(response: Response, fallback: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
}

export async function listKekMarks(): Promise<KekMarkRow[]> {
  const listed = await fetch(MARK_PATH, { headers: requireAuthHeaders() })
  return parseKekJson(listed, "Błąd listy znaczników KEK", 200)
}

export async function persistTenantContractKek(payload: KekMarkWrite): Promise<KekMarkRow> {
  const posted = await fetch(MARK_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  return parseKekJson(posted, "Błąd zapisu znacznika KEK", 201)
}
