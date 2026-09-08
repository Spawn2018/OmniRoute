import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type DocumentDispatchRuleRow = {
  id: string
  organization_id: string
  incoterm: string
  trade_side: string
  document_kind: string
  recipient_role: string
  source_ref: string
  superseded_by: string | null
}

export type DocumentDispatchRuleCreateBody = {
  incoterm: string
  trade_side: string
  document_kind: string
  recipient_role: string
  source_ref: string
}

const PATH = "/api/v1/document-dispatch-rules"

export function documentDispatchRuleBody(args: {
  incoterm: string
  tradeSide: string
  documentKind: string
  recipientRole: string
}): DocumentDispatchRuleCreateBody {
  return {
    incoterm: args.incoterm.trim(),
    trade_side: args.tradeSide.trim(),
    document_kind: args.documentKind.trim(),
    recipient_role: args.recipientRole.trim(),
    source_ref: "tenant:manual",
  }
}

export async function fetchDocumentDispatchRules(args: {
  incoterm: string
  tradeSide: string
  documentKind?: string
}): Promise<DocumentDispatchRuleRow[]> {
  const query = new URLSearchParams()
  query.append("incoterm", args.incoterm)
  query.append("trade_side", args.tradeSide)
  const kind = args.documentKind
  if (kind !== undefined && kind.length > 0) {
    query.append("document_kind", kind)
  }
  const reply = await fetch(`${PATH}?${query}`, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy adresatów"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as DocumentDispatchRuleRow[]
}

export async function saveDocumentDispatchRule(
  payload: DocumentDispatchRuleCreateBody,
): Promise<DocumentDispatchRuleRow> {
  const auth = requireAuthHeaders()
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      Authorization: auth.Authorization,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu adresata"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as DocumentDispatchRuleRow
}
