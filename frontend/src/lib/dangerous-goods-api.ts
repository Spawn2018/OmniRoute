import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type DangerousGood = {
  id: string
  organization_id: string
  un_number: string
  imdg_class: string
  adr_tunnel_code: string
  segregation_group: string
  packing_group: string
  marine_pollutant: boolean
  name: string
  aliases: string[]
  source_ref: string
}

export function dangerousGoodCreateBody(input: {
  unNumber: string
  imdgClass: string
  name: string
  aliasesText: string
  tunnelCode: string
  segregationGroup: string
  packingGroup: string
  marinePollutant: boolean
}): {
  un_number: string
  imdg_class: string
  name: string
  aliases: string[]
  adr_tunnel_code: string
  segregation_group: string
  packing_group: string
  marine_pollutant: boolean
} {
  const aliases = input.aliasesText
    .split(",")
    .map((part) => part.trim())
    .filter((part) => part.length > 0)
  return {
    un_number: input.unNumber.trim(),
    imdg_class: input.imdgClass.trim(),
    name: input.name.trim(),
    aliases,
    adr_tunnel_code: input.tunnelCode.trim(),
    segregation_group: input.segregationGroup.trim(),
    packing_group: input.packingGroup.trim(),
    marine_pollutant: input.marinePollutant,
  }
}

async function readDangerousGood(response: Response, fallback: string): Promise<DangerousGood> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as DangerousGood
}

export async function fetchDangerousGoods(): Promise<DangerousGood[]> {
  const response = await fetch("/api/v1/dangerous-goods", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy towarów niebezpiecznych"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as DangerousGood[]
}

export async function createDangerousGood(body: {
  un_number: string
  imdg_class: string
  name: string
  aliases: string[]
  adr_tunnel_code: string
  segregation_group: string
  packing_group: string
  marine_pollutant: boolean
}): Promise<DangerousGood> {
  const response = await fetch("/api/v1/dangerous-goods", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readDangerousGood(response, "Błąd zapisu towaru niebezpiecznego")
}

export async function resolveDangerousGood(token: string): Promise<DangerousGood> {
  const params = new URLSearchParams({ token })
  const response = await fetch(`/api/v1/dangerous-goods/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return readDangerousGood(response, "Nieznany numer UN")
}
