import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type PortSurcharge = {
  id: string
  organization_id: string
  port_id: string
  code: string
  title: string
  applies_when: string
  amount: string
  currency: string
  source_ref: string
}

export type PortSurchargeDraft = {
  portId: string
  code: string
  title: string
  appliesWhen: string
  amount: string
  currency: string
}

export const EMPTY_SURCHARGE_DRAFT: PortSurchargeDraft = {
  portId: "",
  code: "",
  title: "",
  appliesWhen: "",
  amount: "",
  currency: "",
}

export function portSurchargeCreateBody(draft: PortSurchargeDraft): {
  port_id: string
  code: string
  title: string
  applies_when: string
  amount: string
  currency: string
} {
  return {
    port_id: draft.portId.trim(),
    code: draft.code.trim(),
    title: draft.title.trim(),
    applies_when: draft.appliesWhen.trim(),
    amount: draft.amount.trim(),
    currency: draft.currency.trim().toUpperCase(),
  }
}

async function readSurcharge(response: Response, fallback: string): Promise<PortSurcharge> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as PortSurcharge
}

export async function fetchPortSurcharges(): Promise<PortSurcharge[]> {
  const response = await fetch("/api/v1/port-surcharges", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy extra portowych"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as PortSurcharge[]
}

export async function createPortSurcharge(
  body: ReturnType<typeof portSurchargeCreateBody>,
): Promise<PortSurcharge> {
  const response = await fetch("/api/v1/port-surcharges", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readSurcharge(response, "Błąd zapisu extra portowego")
}

export async function matchPortSurcharges(
  portId: string,
  appliesWhen: string,
): Promise<PortSurcharge[]> {
  const params = new URLSearchParams({
    port_id: portId,
    applies_when: appliesWhen,
  })
  const response = await fetch(`/api/v1/port-surcharges/matching?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd dopasowania extra portowych"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as PortSurcharge[]
}

export async function resolvePortSurcharge(portId: string, code: string): Promise<PortSurcharge> {
  const params = new URLSearchParams({ port_id: portId, code })
  const response = await fetch(`/api/v1/port-surcharges/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return readSurcharge(response, "Nieznane extra portowe")
}
