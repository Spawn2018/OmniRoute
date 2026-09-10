import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const HEADER_PATH = "/api/v1/customer-contracts"

export type CustomerContractHeader = {
  id: string
  organization_id: string
  contract_code: string
  shipper_label: string
  their_customer_label: string
  source_ref: string
  has_ciphertext: boolean
}

export type CustomerContractHeaderWrite = {
  contract_code: string
  shipper_label: string
  their_customer_label: string
  source_ref: string
  opaque_fixture?: boolean
}

export function pactHeaderWrite(draft: {
  pactMark: string
  loaderHint: string
  buyerHint: string
  originHint: string
  attachOpaque: boolean
}): CustomerContractHeaderWrite {
  return {
    contract_code: draft.pactMark.trim(),
    shipper_label: draft.loaderHint.trim(),
    their_customer_label: draft.buyerHint.trim(),
    source_ref: draft.originHint.trim(),
    opaque_fixture: draft.attachOpaque,
  }
}

export async function listCustomerContractHeaders(): Promise<CustomerContractHeader[]> {
  const listed = await fetch(HEADER_PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(
      await readApiDetail(listed, "Błąd listy nagłówków umów"),
      httpErrorStatus(listed),
    )
  }
  return (await listed.json()) as CustomerContractHeader[]
}

export async function persistCustomerContract(
  payload: CustomerContractHeaderWrite,
): Promise<CustomerContractHeader> {
  const posted = await fetch(HEADER_PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status !== 201) {
    throw new ApiError(
      await readApiDetail(posted, "Błąd zapisu nagłówka umowy"),
      httpErrorStatus(posted),
    )
  }
  return (await posted.json()) as CustomerContractHeader
}
