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

export function requireTenantHeaders(): {
  "X-Organization-Id": string
  "X-User-Id": string
} {
  const { organizationId, userId } = getTenantContext()
  if (!organizationId || !userId) {
    throw new Error("Ustaw X-Organization-Id i X-User-Id w ustawieniach sesji")
  }
  return {
    "X-Organization-Id": organizationId,
    "X-User-Id": userId,
  }
}
