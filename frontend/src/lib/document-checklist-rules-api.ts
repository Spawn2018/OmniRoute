import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type DocumentChecklistRuleRow = {
  id: string
  organization_id: string
  incoterm: string
  trade_side: string
  mode: string
  document_kind: string
  blocks_dispatch: boolean
}

export type DocumentChecklistRuleCreateBody = {
  incoterm: string
  trade_side: string
  mode: string
  document_kind: string
  blocks_dispatch: boolean
}

const PATH = "/api/v1/document-checklist-rules"

export function documentChecklistRuleBody(args: {
  incoterm: string
  tradeSide: string
  mode: string
  documentKind: string
  blocksDispatch: boolean
}): DocumentChecklistRuleCreateBody {
  return {
    incoterm: args.incoterm.trim(),
    trade_side: args.tradeSide.trim(),
    mode: args.mode.trim(),
    document_kind: args.documentKind.trim(),
    blocks_dispatch: args.blocksDispatch,
  }
}

export async function fetchDocumentChecklistRules(args: {
  incoterm: string
  tradeSide: string
  mode: string
}): Promise<DocumentChecklistRuleRow[]> {
  const query = new URLSearchParams({
    incoterm: args.incoterm,
    trade_side: args.tradeSide,
    mode: args.mode,
  })
  const reply = await fetch(`${PATH}?${query}`, { headers: requireAuthHeaders() })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy checklisty"), httpErrorStatus(reply))
  }
  return (await reply.json()) as DocumentChecklistRuleRow[]
}

export async function saveDocumentChecklistRule(
  payload: DocumentChecklistRuleCreateBody,
): Promise<DocumentChecklistRuleRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: new Headers({
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    }),
    body: JSON.stringify(payload),
  })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu checklisty"), httpErrorStatus(reply))
  }
  return (await reply.json()) as DocumentChecklistRuleRow
}
