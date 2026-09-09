import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-rfp-intakes"

export type IntakeMark = {
  id: string
  organization_id: string
  tender_id: string
  intake_code: string
  source_ref: string
}

export type IntakeMarkWrite = {
  tender_id: string
  intake_code: string
  source_ref: string
}

export function intakeWrite(draft: {
  boardStamp: string
  codeStamp: string
  originStamp: string
}): IntakeMarkWrite {
  return {
    tender_id: draft.boardStamp.trim(),
    intake_code: draft.codeStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listIntakeMarks(): Promise<IntakeMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(
      await readApiDetail(listed, "Błąd listy przyjęć RFP"),
      httpErrorStatus(listed),
    )
  }
  const pack: unknown = await listed.json()
  return pack as IntakeMark[]
}

export async function persistIntakeMark(payload: IntakeMarkWrite): Promise<IntakeMark> {
  const packed = JSON.stringify(payload)
  const posted = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "intake-desk",
    },
    body: packed,
  })
  const failed = posted.status !== 201
  if (failed) {
    const note = await readApiDetail(posted, "Błąd zapisu przyjęcia RFP")
    throw new ApiError(note, httpErrorStatus(posted))
  }
  const intake: unknown = await posted.json()
  return intake as IntakeMark
}
