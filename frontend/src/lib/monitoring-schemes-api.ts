import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/monitoring-schemes"

export type SchemeMark = {
  id: string
  organization_id: string
  scheme_code: string
  source_ref: string
}

export type SchemeMarkWrite = {
  scheme_code: string
  source_ref: string
}

export function schemeWrite(draft: {
  codeStamp: string
  originStamp: string
}): SchemeMarkWrite {
  return {
    scheme_code: draft.codeStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listSchemeMarks(): Promise<SchemeMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(
      await readApiDetail(listed, "Błąd listy schematów monitoringu"),
      httpErrorStatus(listed),
    )
  }
  return (await listed.json()) as SchemeMark[]
}

export async function persistSchemeMark(payload: SchemeMarkWrite): Promise<SchemeMark> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status !== 201) {
    throw new ApiError(
      await readApiDetail(posted, "Błąd zapisu schematu monitoringu"),
      httpErrorStatus(posted),
    )
  }
  return (await posted.json()) as SchemeMark
}
