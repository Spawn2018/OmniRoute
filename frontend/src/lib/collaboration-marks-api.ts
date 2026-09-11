import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const ENDPOINT = "/api/v1/collaboration-marks"

export type CollaborationMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  role_kind: string
  source_ref: string
}

export type CollaborationWriteBody = {
  mark_code: string
  role_kind: string
  source_ref: string
}

export function toCollaborationWrite(fields: {
  slug: string
  role: string
  pointer: string
}): CollaborationWriteBody {
  return {
    mark_code: fields.slug.trim(),
    role_kind: fields.role.trim().toLowerCase(),
    source_ref: fields.pointer.trim(),
  }
}

async function decode<T>(response: Response, fail: string, ok: number): Promise<T> {
  if (response.status !== ok) {
    throw new ApiError(await readApiDetail(response, fail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function listCollaborationMarks(): Promise<CollaborationMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: requireAuthHeaders() })
  return decode(response, "Błąd listy ról współpracy", 200)
}

export async function createCollaborationMark(
  body: CollaborationWriteBody,
): Promise<CollaborationMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return decode(response, "Błąd zapisu roli współpracy", 201)
}
