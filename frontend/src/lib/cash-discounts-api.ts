import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/cash-discounts"

export type SkontoMark = {
  id: string
  organization_id: string
  sales_invoice_id: string
  discount_kind: string
  source_ref: string
}

export type SkontoMarkWrite = {
  sales_invoice_id: string
  discount_kind: string
  source_ref: string
}

export function skontoWrite(draft: {
  invoiceStamp: string
  kindStamp: string
  originStamp: string
}): SkontoMarkWrite {
  return {
    sales_invoice_id: draft.invoiceStamp.trim(),
    discount_kind: draft.kindStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listSkontoMarks(): Promise<SkontoMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(await readApiDetail(listed, "Błąd listy skonta"), httpErrorStatus(listed))
  }
  return (await listed.json()) as SkontoMark[]
}

export async function persistSkontoMark(payload: SkontoMarkWrite): Promise<SkontoMark> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status !== 201) {
    throw new ApiError(await readApiDetail(posted, "Błąd zapisu skonta"), httpErrorStatus(posted))
  }
  return (await posted.json()) as SkontoMark
}
