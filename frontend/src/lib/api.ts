import { client } from "@/api/client.gen"
import {
  healthHealthGet,
  listUsersApiV1TenancyUsersGet,
} from "@/api/sdk.gen"
import type { AppUserResponse } from "@/api/types.gen"
import { requireTenantHeaders } from "@/lib/tenant"

client.setConfig({ baseUrl: "" })

export type AppUser = AppUserResponse

export class ApiError extends Error {
  readonly status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

export { getTenantContext, setTenantContext } from "@/lib/tenant"

function statusOf(response: Response | undefined): number {
  return response?.status ?? 500
}

export async function fetchTenancyUsers(): Promise<AppUser[]> {
  const { data, error, response } = await listUsersApiV1TenancyUsersGet({
    headers: requireTenantHeaders(),
  })
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd listy użytkowników", statusOf(response))
  }
  return data
}

export async function fetchHealth(): Promise<{ status: string }> {
  const { data, error, response } = await healthHealthGet()
  if (error || !data || typeof data.status !== "string") {
    throw new ApiError("API niedostępne", statusOf(response))
  }
  return { status: data.status }
}
