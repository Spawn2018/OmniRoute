import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/repair-playbooks"

export type RepairPlaybookRow = {
  id: string
  organization_id: string
  playbook_code: string
  stance_kind: string
  source_ref: string
}

export type RepairPlaybookWrite = {
  playbook_code: string
  stance_kind: string
  source_ref: string
}

export function buildRepairPlaybookWrite(fields: {
  code: string
  kind: string
  origin: string
}): RepairPlaybookWrite {
  return {
    playbook_code: fields.code.trim(),
    stance_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchRepairPlaybooks(): Promise<RepairPlaybookRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy playbooków naprawy", 200)
}

export async function saveRepairPlaybook(
  body: RepairPlaybookWrite,
): Promise<RepairPlaybookRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu playbooka naprawy", 201)
}
