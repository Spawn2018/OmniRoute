import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type LclConsoleMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  console_kind: string
  source_ref: string
}

export type LclConsoleMarkPayload = {
  mark_code: string
  console_kind: string
  source_ref: string
}

const PATH = "/api/v1/lcl-console-marks"

export function buildLclConsoleMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): LclConsoleMarkPayload {
  return {
    mark_code: args.code.trim(),
    console_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchLclConsoleMarks(): Promise<LclConsoleMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu konsoli LCL"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as LclConsoleMarkRow[]
}

export async function saveLclConsoleMark(
  payload: LclConsoleMarkPayload,
): Promise<LclConsoleMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "lcl-console-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać stance konsoli LCL"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as LclConsoleMarkRow
}
