import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/relation-document-requirements"

export type RelationDocumentRequirementRow = {
  id: string
  organization_id: string
  requirement_code: string
  relation_kind: string
  source_ref: string
}

export type RelationDocumentRequirementWrite = {
  requirement_code: string
  relation_kind: string
  source_ref: string
}

export function buildRelationDocumentRequirementWrite(fields: {
  code: string
  kind: string
  origin: string
}): RelationDocumentRequirementWrite {
  return {
    requirement_code: fields.code.trim(),
    relation_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchRelationDocumentRequirements(): Promise<RelationDocumentRequirementRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Blad listy znacznikow wymogu dokumentow relacji", 200)
}

export async function saveRelationDocumentRequirement(
  body: RelationDocumentRequirementWrite,
): Promise<RelationDocumentRequirementRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Blad zapisu znacznika wymogu dokumentow relacji", 201)
}
