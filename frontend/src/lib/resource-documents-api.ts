import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ResourceDocumentRow = {
  id: string
  organization_id: string
  resource_id: string
  document_kind: string
  valid_until: string
  source_ref: string
}

const PATH = "/api/v1/resource-documents"

export async function fetchResourceDocuments(): Promise<ResourceDocumentRow[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy ważności"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as ResourceDocumentRow[]
}

export async function saveResourceDocument(args: {
  resourceId: string
  documentKind: string
  validUntil: string
}): Promise<ResourceDocumentRow> {
  const auth = requireAuthHeaders()
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      Authorization: auth.Authorization,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      resource_id: args.resourceId.trim(),
      document_kind: args.documentKind.trim(),
      valid_until: args.validUntil.trim(),
      source_ref: "tenant:manual",
    }),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu ważności"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as ResourceDocumentRow
}
