import { client } from "@/api/client.gen"
import {
  createSessionTokenApiV1SessionTokenPost,
  healthHealthGet,
  listUsersApiV1TenancyUsersGet,
} from "@/api/sdk.gen"
import type { AppUserResponse, SessionTokenRequest } from "@/api/types.gen"
import { getSessionToken } from "@/lib/tenant"

client.setConfig({
  baseUrl: "",
  auth: () => getSessionToken() ?? undefined,
})

export type AppUser = AppUserResponse

export class ApiError extends Error {
  readonly status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

export { clearSessionToken, getTenantContext, setSessionToken } from "@/lib/tenant"

export function httpErrorStatus(response: Response | undefined): number {
  return response?.status ?? 500
}

export async function issueSessionToken(input: {
  email: string
  password: string
}): Promise<string> {
  const { data, error, response } = await createSessionTokenApiV1SessionTokenPost({
    body: {
      email: input.email,
      password: input.password,
    } as SessionTokenRequest,
  })
  if (error || !data?.access_token) {
    throw new ApiError("Nie udało się uzyskać tokenu sesji", httpErrorStatus(response))
  }
  return data.access_token
}

export async function fetchTenancyUsers(): Promise<AppUser[]> {
  const { data, error, response } = await listUsersApiV1TenancyUsersGet()
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd listy użytkowników", httpErrorStatus(response))
  }
  return data
}

export async function fetchHealth(): Promise<{ status: string }> {
  const { data, error, response } = await healthHealthGet()
  if (error || !data || typeof data.status !== "string") {
    throw new ApiError("API niedostępne", httpErrorStatus(response))
  }
  return { status: data.status }
}
