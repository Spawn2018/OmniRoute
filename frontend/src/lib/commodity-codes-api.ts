import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { catalogCreateBody } from "@/lib/catalog-create"
import { requireAuthHeaders } from "@/lib/tenant"

export type CommodityCode = {
  id: string
  organization_id: string
  code: string
  name: string
  aliases: string[]
  source_ref: string
}

export const commodityCodeCreateBody = catalogCreateBody

async function readCommodityCode(response: Response, fallback: string): Promise<CommodityCode> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as CommodityCode
}

export async function fetchCommodityCodes(): Promise<CommodityCode[]> {
  const response = await fetch("/api/v1/commodity-codes", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy kodów towarowych"), httpErrorStatus(response))
  }
  return (await response.json()) as CommodityCode[]
}

export async function createCommodityCode(body: {
  code: string
  name: string
  aliases: string[]
}): Promise<CommodityCode> {
  const response = await fetch("/api/v1/commodity-codes", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readCommodityCode(response, "Błąd zapisu kodu towarowego")
}

export async function resolveCommodityCode(token: string): Promise<CommodityCode> {
  const params = new URLSearchParams({ token })
  const response = await fetch(`/api/v1/commodity-codes/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return readCommodityCode(response, "Nieznany kod towarowy")
}
