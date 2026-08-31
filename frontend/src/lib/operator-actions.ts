import { clearSessionToken } from "@/lib/tenant"

export const OPERATOR_ACTION_IDS = [
  "extract",
  "accept-focus",
  "save-view",
  "clear-session",
] as const

export type OperatorActionId = (typeof OPERATOR_ACTION_IDS)[number]

export type OperatorAction = {
  id: OperatorActionId
  label: string
  route?: "/extractions" | "/session"
}

export const OPERATOR_ACTIONS: readonly OperatorAction[] = [
  { id: "extract", label: "Ekstrahuj dokument", route: "/extractions" },
  { id: "accept-focus", label: "Ustaw focus na akceptacji HITL", route: "/extractions" },
  { id: "save-view", label: "Zapisz widok tabeli" },
  { id: "clear-session", label: "Wyczyść sesję" },
]

type OperatorActionHandler = (id: OperatorActionId) => void

const operatorActionHandlers = new Set<OperatorActionHandler>()

export function paletteHasRequiredOperatorActions(ids: readonly string[]): boolean {
  return OPERATOR_ACTION_IDS.every((id) => ids.includes(id))
}

export function runOperatorAction(id: OperatorActionId): void {
  if (id === "clear-session") {
    clearSessionToken()
  }
  for (const handler of operatorActionHandlers) {
    handler(id)
  }
}

export function subscribeOperatorAction(handler: OperatorActionHandler): () => void {
  operatorActionHandlers.add(handler)
  return () => {
    operatorActionHandlers.delete(handler)
  }
}
