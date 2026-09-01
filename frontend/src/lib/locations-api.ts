import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type Location = {
  id: string
  organization_id: string
  kind: string
  name: string
  code: string | null
  port_id: string | null
  country_code: string | null
  city: string | null
  address_line: string | null
  postal_code: string | null
  lat: string | null
  lng: string | null
  source_ref: string
}

export type ZoneMember = {
  id: string
  organization_id: string
  zone_location_id: string
  country_code: string
  postal_from: string
  postal_to: string
  source_ref: string
}

export type ZoneCreateBody = {
  code: string
  name: string
}

export type ZoneMemberCreateBody = {
  country_code: string
  postal_from: string
  postal_to: string
}

export function zoneCreateBody(args: { code: string; name: string }): ZoneCreateBody {
  return {
    code: args.code.trim().toUpperCase().replace(/\s+/g, "_"),
    name: args.name.trim(),
  }
}

export function zoneMemberCreateBody(args: {
  countryCode: string
  postalFrom: string
  postalTo: string
}): ZoneMemberCreateBody {
  const normalize = (value: string) => value.replace(/[\s-]/g, "").toUpperCase()
  return {
    country_code: args.countryCode.trim().toUpperCase(),
    postal_from: normalize(args.postalFrom),
    postal_to: normalize(args.postalTo),
  }
}

async function readJson<T>(response: Response, fallback: string): Promise<T> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchLocations(search: string): Promise<Location[]> {
  const query = search.trim() === "" ? "" : `?${new URLSearchParams({ search }).toString()}`
  const response = await fetch(`/api/v1/locations${query}`, { headers: requireAuthHeaders() })
  return readJson<Location[]>(response, "Błąd listy lokalizacji")
}

export async function fetchZoneMembers(zoneId: string): Promise<ZoneMember[]> {
  const response = await fetch(`/api/v1/locations/${zoneId}/members`, {
    headers: requireAuthHeaders(),
  })
  return readJson<ZoneMember[]>(response, "Błąd listy zakresów strefy")
}

export async function createZone(body: ZoneCreateBody): Promise<Location> {
  const response = await fetch("/api/v1/locations", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readJson<Location>(response, "Błąd zapisu strefy")
}

export async function addZoneMember(
  zoneId: string,
  body: ZoneMemberCreateBody,
): Promise<ZoneMember> {
  const response = await fetch(`/api/v1/locations/${zoneId}/members`, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readJson<ZoneMember>(response, "Błąd zapisu zakresu")
}

export async function resolvePostalCode(
  countryCode: string,
  postalCode: string,
): Promise<Location> {
  const params = new URLSearchParams({
    country_code: countryCode.trim().toUpperCase(),
    postal_code: postalCode.replace(/[\s-]/g, "").toUpperCase(),
  })
  const response = await fetch(`/api/v1/locations/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return readJson<Location>(response, "Kod pocztowy poza strefami")
}
