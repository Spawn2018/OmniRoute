import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/carbon-methods"

export type MethodMark = {
  id: string
  organization_id: string
  method_code: string
  method_version: string
  source_ref: string
}

export type MethodMarkWrite = {
  method_code: string
  method_version: string
  source_ref: string
}

export function methodWrite(draft: {
  codeStamp: string
  versionStamp: string
  originStamp: string
}): MethodMarkWrite {
  return {
    method_code: draft.codeStamp.trim(),
    method_version: draft.versionStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

async function parseMethod<T>(res: Response, fallback: string, ok: number): Promise<T> {
  if (res.status !== ok) {
    throw new ApiError(await readApiDetail(res, fallback), httpErrorStatus(res))
  }
  return (await res.json()) as T
}

export async function listMethodMarks(): Promise<MethodMark[]> {
  return parseMethod(
    await fetch(PATH, { headers: requireAuthHeaders() }),
    "Błąd listy metodyk CO₂",
    200,
  )
}

export async function persistMethodMark(payload: MethodMarkWrite): Promise<MethodMark> {
  return parseMethod(
    await fetch(PATH, {
      method: "POST",
      headers: { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),
    "Błąd zapisu metodyki CO₂",
    201,
  )
}
