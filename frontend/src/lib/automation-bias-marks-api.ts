import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type AutomationBiasMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  bias_kind: string
  source_ref: string
}

export type AutomationBiasMarkPayload = {
  mark_code: string
  bias_kind: string
  source_ref: string
}

const PATH = "/api/v1/automation-bias-marks"

export function buildAutomationBiasMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): AutomationBiasMarkPayload {
  return {
    mark_code: args.code.trim(),
    bias_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchAutomationBiasMarks(): Promise<AutomationBiasMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu automation bias"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as AutomationBiasMarkRow[]
}

export async function saveAutomationBiasMark(
  payload: AutomationBiasMarkPayload,
): Promise<AutomationBiasMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "automation-bias-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika automation bias"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as AutomationBiasMarkRow
}
