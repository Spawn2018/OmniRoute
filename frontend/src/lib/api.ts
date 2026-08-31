export type TenantContext = {
  organizationId: string
  userId: string
}

const ORG_KEY = "omniroute.organizationId"
const USER_KEY = "omniroute.userId"

export function getTenantContext(): TenantContext {
  return {
    organizationId: localStorage.getItem(ORG_KEY) ?? "",
    userId: localStorage.getItem(USER_KEY) ?? "",
  }
}

export function setTenantContext(ctx: TenantContext): void {
  localStorage.setItem(ORG_KEY, ctx.organizationId)
  localStorage.setItem(USER_KEY, ctx.userId)
}

export type AppUser = {
  id: string
  organization_id: string
  email: string
  display_name: string
}

export class ApiError extends Error {
  readonly status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

export async function apiGet<T>(path: string): Promise<T> {
  const { organizationId, userId } = getTenantContext()
  if (!organizationId || !userId) {
    throw new ApiError("Ustaw X-Organization-Id i X-User-Id w ustawieniach sesji", 400)
  }

  const response = await fetch(path, {
    headers: {
      Accept: "application/json",
      "X-Organization-Id": organizationId,
      "X-User-Id": userId,
    },
  })

  if (!response.ok) {
    const detail = await response.text()
    throw new ApiError(detail || response.statusText, response.status)
  }

  return (await response.json()) as T
}

export async function fetchTenancyUsers(): Promise<AppUser[]> {
  return apiGet<AppUser[]>("/api/v1/tenancy/users")
}

export async function fetchHealth(): Promise<{ status: string }> {
  const response = await fetch("/health")
  if (!response.ok) {
    throw new ApiError("API niedostępne", response.status)
  }
  return (await response.json()) as { status: string }
}
