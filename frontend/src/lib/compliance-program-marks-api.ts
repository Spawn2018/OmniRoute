import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ComplianceProgramMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  program_kind: string
  source_ref: string
}

export type ComplianceProgramMarkPayload = {
  mark_code: string
  program_kind: string
  source_ref: string
}

const PATH = "/api/v1/compliance-program-marks"

export function buildComplianceProgramMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): ComplianceProgramMarkPayload {
  return {
    mark_code: args.code.trim(),
    program_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchComplianceProgramMarks(): Promise<ComplianceProgramMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu programu zgodności"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as ComplianceProgramMarkRow[]
}

export async function saveComplianceProgramMark(
  payload: ComplianceProgramMarkPayload,
): Promise<ComplianceProgramMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "compliance-program-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać stancji programu zgodności"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as ComplianceProgramMarkRow
}
