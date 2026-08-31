export type TenantContext = {
  organizationId: string
  userId: string
}

const TOKEN_KEY = "omniroute.sessionToken"

function storageGet(key: string): string | null {
  if (typeof localStorage === "undefined") {
    return null
  }
  return localStorage.getItem(key)
}

function storageSet(key: string, value: string): void {
  if (typeof localStorage === "undefined") {
    return
  }
  localStorage.setItem(key, value)
}

function storageRemove(key: string): void {
  if (typeof localStorage === "undefined") {
    return
  }
  localStorage.removeItem(key)
}

function decodeBase64Url(segment: string): string {
  const normalized = segment.replace(/-/g, "+").replace(/_/g, "/")
  const pad = normalized.length % 4 === 0 ? "" : "=".repeat(4 - (normalized.length % 4))
  return atob(normalized + pad)
}

export function claimsFromSessionToken(token: string): TenantContext | null {
  const parts = token.split(".")
  if (parts.length !== 3 || parts[1] === undefined) {
    return null
  }
  try {
    const payload: unknown = JSON.parse(decodeBase64Url(parts[1]))
    if (typeof payload !== "object" || payload === null) {
      return null
    }
    const record = payload as Record<string, unknown>
    if (typeof record.org !== "string" || typeof record.sub !== "string") {
      return null
    }
    return { organizationId: record.org, userId: record.sub }
  } catch {
    return null
  }
}

export function getSessionToken(): string | null {
  const token = storageGet(TOKEN_KEY)
  if (token === null || token.length === 0) {
    return null
  }
  return token
}

export function setSessionToken(token: string): void {
  storageSet(TOKEN_KEY, token)
}

export function clearSessionToken(): void {
  storageRemove(TOKEN_KEY)
}

export function getTenantContext(): TenantContext {
  const token = getSessionToken()
  if (token === null) {
    return { organizationId: "", userId: "" }
  }
  return claimsFromSessionToken(token) ?? { organizationId: "", userId: "" }
}

export function requireAuthHeaders(): { Authorization: string } {
  const token = getSessionToken()
  if (token === null) {
    throw new Error("Zaloguj się w ustawieniach sesji")
  }
  return { Authorization: `Bearer ${token}` }
}
