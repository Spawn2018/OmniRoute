import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type HandoverNoteRow = {
  id: string
  organization_id: string
  note_code: string
  situation: string
  background: string
  assessment: string
  recommendation: string
  source_ref: string
}

export type HandoverNotePayload = {
  note_code: string
  situation: string
  background: string
  assessment: string
  recommendation: string
  source_ref: string
}

const PATH = "/api/v1/handover-notes"

export function buildHandoverNoteWrite(args: {
  code: string
  situation: string
  background: string
  assessment: string
  recommendation: string
  origin: string
}): HandoverNotePayload {
  return {
    note_code: args.code.trim(),
    situation: args.situation.trim(),
    background: args.background.trim(),
    assessment: args.assessment.trim(),
    recommendation: args.recommendation.trim(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchHandoverNotes(): Promise<HandoverNoteRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać notatek SBAR"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as HandoverNoteRow[]
}

export async function saveHandoverNote(
  payload: HandoverNotePayload,
): Promise<HandoverNoteRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "handover-note-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać notatki SBAR"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as HandoverNoteRow
}
