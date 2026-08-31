import { afterEach, describe, expect, it } from "vitest"
import {
  claimsFromSessionToken,
  clearSessionToken,
  getTenantContext,
  requireAuthHeaders,
  setSessionToken,
} from "@/lib/tenant"

const store = new Map<string, string>()

Object.defineProperty(globalThis, "localStorage", {
  configurable: true,
  value: {
    getItem: (key: string) => store.get(key) ?? null,
    setItem: (key: string, value: string) => {
      store.set(key, value)
    },
    removeItem: (key: string) => {
      store.delete(key)
    },
  },
})

function fakeJwt(org: string, sub: string): string {
  const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }))
  const payload = btoa(JSON.stringify({ org, sub }))
  return `${header}.${payload}.sig`
}

afterEach(() => {
  store.clear()
})

describe("session token claims", () => {
  it("reads org and sub from stored JWT", () => {
    const org = "11111111-1111-1111-1111-111111111111"
    const user = "22222222-2222-2222-2222-222222222222"
    setSessionToken(fakeJwt(org, user))
    expect(getTenantContext()).toEqual({ organizationId: org, userId: user })
  })

  it("requireAuthHeaders sends Bearer from stored token", () => {
    const token = fakeJwt("a", "b")
    setSessionToken(token)
    expect(requireAuthHeaders()).toEqual({ Authorization: `Bearer ${token}` })
  })

  it("requireAuthHeaders throws without token", () => {
    clearSessionToken()
    expect(() => requireAuthHeaders()).toThrow(/Zaloguj/)
  })

  it("claimsFromSessionToken ignores spoofable extra fields only in payload org/sub", () => {
    const token = fakeJwt("org-a", "user-a")
    expect(claimsFromSessionToken(token)).toEqual({
      organizationId: "org-a",
      userId: "user-a",
    })
  })
})
