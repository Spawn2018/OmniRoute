import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/memory-edges"

export type EdgeStamp = {
  id: string
  organization_id: string
  edge_kind: string
  source_ref: string
}

export type EdgeStampWrite = {
  edge_kind: string
  source_ref: string
}

export function edgeWrite(draft: { linkKind: string; originToken: string }): EdgeStampWrite {
  return {
    edge_kind: draft.linkKind.trim(),
    source_ref: draft.originToken.trim(),
  }
}

export async function listMemoryEdges(): Promise<EdgeStamp[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (!listed.ok) {
    throw new ApiError(await readApiDetail(listed, "Błąd listy krawędzi pamięci"), httpErrorStatus(listed))
  }
  return (await listed.json()) as EdgeStamp[]
}

export async function persistEdgeMark(payload: EdgeStampWrite): Promise<EdgeStamp> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status !== 201) {
    throw new ApiError(await readApiDetail(posted, "Błąd zapisu krawędzi pamięci"), httpErrorStatus(posted))
  }
  return (await posted.json()) as EdgeStamp
}
