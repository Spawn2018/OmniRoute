import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type Port = {
  id: string
  organization_id: string
  unlocode: string
  name: string
  country_code: string
  lat: string | null
  lng: string | null
  is_seaport: boolean
  function_flags: string[]
  aliases: string[]
  is_official: boolean
  source_ref: string
  wpi_number: number | null
  harbor_size: string | null
  harbor_type: string | null
  shelter: string | null
  channel_depth_m: string | null
  cargo_pier_depth_m: string | null
  wpi_source_ref: string | null
}

export function railPorts<Row extends { function_flags: readonly string[] }>(
  ports: readonly Row[],
): Row[] {
  return ports.filter((row) => row.function_flags.includes("rail"))
}

export function chinaRailPorts<
  Row extends { country_code: string; function_flags: readonly string[] },
>(ports: readonly Row[]): Row[] {
  return railPorts(ports).filter((row) => row.country_code === "CN")
}

export function oceanLclPorts<Row extends { is_seaport: boolean }>(
  ports: readonly Row[],
): Row[] {
  return ports.filter((row) => row.is_seaport)
}

export function airPorts<Row extends { function_flags: readonly string[] }>(
  ports: readonly Row[],
): Row[] {
  return ports.filter((row) => row.function_flags.includes("airport"))
}

export type PortCreateBody = {
  unlocode: string
  name: string
  country_code: string
  aliases: string[]
}

export function portCreateBody(args: {
  unlocode: string
  name: string
  countryCode: string
  aliasesText: string
}): PortCreateBody {
  const aliases = args.aliasesText
    .split(",")
    .map((part) => part.trim())
    .filter((part) => part.length > 0)
  return {
    unlocode: args.unlocode.replace(/\s+/g, "").toUpperCase(),
    name: args.name.trim(),
    country_code: args.countryCode.trim().toUpperCase(),
    aliases,
  }
}

async function readPort(response: Response, fallback: string): Promise<Port> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as Port
}

export async function fetchPorts(search: string): Promise<Port[]> {
  const query = search.trim() === "" ? "" : `?${new URLSearchParams({ search }).toString()}`
  const response = await fetch(`/api/v1/ports${query}`, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy portów"), httpErrorStatus(response))
  }
  return (await response.json()) as Port[]
}

export async function createPort(body: PortCreateBody): Promise<Port> {
  const response = await fetch("/api/v1/ports", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readPort(response, "Błąd zapisu portu")
}

export async function resolvePort(token: string): Promise<Port> {
  const params = new URLSearchParams({ token })
  const response = await fetch(`/api/v1/ports/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return readPort(response, "Nieznany port")
}
