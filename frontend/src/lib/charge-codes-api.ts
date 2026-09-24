import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ChargeCode = {
  id: string
  organization_id: string
  code: string
  name: string
  aliases: string[]
  source_ref: string
}

export function chargeCodeCreateBody(args: {
  code: string
  name: string
  aliasesText: string
  sourceRef: string
}): { code: string; name: string; aliases: string[]; source_ref: string } {
  const aliases = args.aliasesText
    .split(",")
    .map((part) => part.trim())
    .filter((part) => part.length > 0)
  return {
    code: args.code.trim(),
    name: args.name.trim(),
    aliases,
    source_ref: args.sourceRef.trim(),
  }
}

async function readChargeCode(response: Response, fallback: string): Promise<ChargeCode> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as ChargeCode
}

export async function fetchChargeCodes(): Promise<ChargeCode[]> {
  const response = await fetch("/api/v1/charge-codes", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy kodów opłat"), httpErrorStatus(response))
  }
  return (await response.json()) as ChargeCode[]
}

export async function createChargeCode(body: {
  code: string
  name: string
  aliases: string[]
  source_ref: string
}): Promise<ChargeCode> {
  const response = await fetch("/api/v1/charge-codes", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readChargeCode(response, "Błąd zapisu kodu opłaty")
}

export async function resolveChargeCode(token: string): Promise<ChargeCode> {
  const params = new URLSearchParams({ token })
  const response = await fetch(`/api/v1/charge-codes/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return readChargeCode(response, "Nieznany kod opłaty")
}
