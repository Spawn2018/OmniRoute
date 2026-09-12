import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type JitJisMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  flow_kind: string
  source_ref: string
}

export type JitJisPayload = {
  mark_code: string
  flow_kind: string
  source_ref: string
}

const ROUTE = "/api/v1/jit-jis-marks"

export function makeJitJisPayload(
  code: string,
  kind: string,
  ref: string,
): JitJisPayload {
  return {
    mark_code: code.trim(),
    flow_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadJitJisMarks(): Promise<JitJisMarkRow[]> {
  const blob = await fetch(ROUTE, { headers: requireAuthHeaders() })
  if (blob.ok) {
    return (await blob.json()) as JitJisMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(blob, "Lista znacznikow JIT/JIS niedostepna"),
    httpErrorStatus(blob),
  )
}

export async function createJitJisMark(
  payload: JitJisPayload,
): Promise<JitJisMarkRow> {
  const blob = await fetch(ROUTE, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (blob.status === 201) {
    return (await blob.json()) as JitJisMarkRow
  }
  throw new ApiError(
    await readApiDetail(blob, "Zapis znacznika JIT/JIS nieudany"),
    httpErrorStatus(blob),
  )
}
