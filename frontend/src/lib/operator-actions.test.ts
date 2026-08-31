import { afterEach, describe, expect, it } from "vitest"
import { commandPaletteActionIds } from "@/components/command-palette"
import {
  OPERATOR_ACTION_IDS,
  OPERATOR_ACTIONS,
  paletteHasRequiredOperatorActions,
  runOperatorAction,
  subscribeOperatorAction,
} from "@/lib/operator-actions"
import { getSessionToken, setSessionToken } from "@/lib/tenant"

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

afterEach(() => {
  store.clear()
})

describe("operator palette actions", () => {
  it("requires extract, accept-focus, save-view and clear-session", () => {
    const ids = OPERATOR_ACTIONS.map((action) => action.id)
    expect(ids).toEqual([...OPERATOR_ACTION_IDS])
    expect(paletteHasRequiredOperatorActions(ids)).toBe(true)
    expect(paletteHasRequiredOperatorActions(["nav-home", "nav-users"])).toBe(false)
    expect(paletteHasRequiredOperatorActions(commandPaletteActionIds())).toBe(true)
  })

  it("clear-session uses the existing client session clear", () => {
    setSessionToken("header.payload.sig")
    runOperatorAction("clear-session")
    expect(getSessionToken()).toBeNull()
  })

  it("dispatches extract so the queue can run, not only navigate", () => {
    const seen: string[] = []
    const stop = subscribeOperatorAction((id) => {
      seen.push(id)
    })
    runOperatorAction("extract")
    stop()
    expect(seen).toEqual(["extract"])
  })
})
