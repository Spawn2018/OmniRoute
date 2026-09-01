import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type FreightNetwork = {
  id: string
  organization_id: string
  code: string
  name: string
  aliases: string[]
  website: string | null
  region_scope: string | null
  is_global: boolean
  source_ref: string
}

export function networkCreateBody(input: {
  code: string
  name: string
  aliasesText: string
  website: string
  regionScope: string
  isGlobal: boolean
}): {
  code: string
  name: string
  aliases: string[]
  website: string | null
  region_scope: string | null
  is_global: boolean
} {
  const aliases = input.aliasesText
    .split(",")
    .map((part) => part.trim())
    .filter((part) => part.length > 0)
  const website = input.website.trim()
  const regionScope = input.regionScope.trim()
  return {
    code: input.code.trim(),
    name: input.name.trim(),
    aliases,
    website: website.length === 0 ? null : website,
    region_scope: regionScope.length === 0 ? null : regionScope,
    is_global: input.isGlobal,
  }
}

async function readNetwork(response: Response, fallback: string): Promise<FreightNetwork> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as FreightNetwork
}

export async function fetchNetworks(): Promise<FreightNetwork[]> {
  const response = await fetch("/api/v1/networks", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy sieci"), httpErrorStatus(response))
  }
  return (await response.json()) as FreightNetwork[]
}

export async function createNetwork(body: {
  code: string
  name: string
  aliases: string[]
  website: string | null
  region_scope: string | null
  is_global: boolean
}): Promise<FreightNetwork> {
  const response = await fetch("/api/v1/networks", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readNetwork(response, "Błąd zapisu sieci")
}

export async function resolveNetwork(token: string): Promise<FreightNetwork> {
  const params = new URLSearchParams({ token })
  const response = await fetch(`/api/v1/networks/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return readNetwork(response, "Nieznana sieć")
}
