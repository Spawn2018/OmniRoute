import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/fuel-indexes"

export type IndexMark = {
  id: string
  organization_id: string
  index_kind: string
  published_on: string
  index_value: string
  source_ref: string
}

export type IndexMarkWrite = {
  index_kind: string
  published_on: string
  index_value: string
  source_ref: string
}

export function indexWrite(args: {
  kindToken: string
  dayStamp: string
  pointMark: string
  originStamp: string
}): IndexMarkWrite {
  return {
    index_kind: args.kindToken.trim().toLowerCase(),
    published_on: args.dayStamp.trim(),
    index_value: args.pointMark.trim(),
    source_ref: args.originStamp.trim(),
  }
}

export async function listIndexMarks(): Promise<IndexMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy indeksów paliwowych"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as IndexMark[]
}

export async function persistIndexMark(payload: IndexMarkWrite): Promise<IndexMark> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "index-mark",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu indeksu paliwowego"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as IndexMark
}
