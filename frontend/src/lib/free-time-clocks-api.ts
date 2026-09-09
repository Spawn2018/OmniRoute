import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/free-time-clocks"

export type ClockMark = {
  id: string
  organization_id: string
  clock_kind: string
  free_days: number
  source_ref: string
}

export type ClockMarkWrite = {
  clock_kind: string
  free_days: number
  source_ref: string
}

export function clockWrite(draft: {
  kindStamp: string
  daysStamp: string
  originStamp: string
}): ClockMarkWrite {
  return {
    clock_kind: draft.kindStamp.trim(),
    free_days: Number.parseInt(draft.daysStamp.trim(), 10),
    source_ref: draft.originStamp.trim(),
  }
}

async function parseClock<T>(res: Response, fallback: string, ok: number): Promise<T> {
  if (res.status !== ok) {
    throw new ApiError(await readApiDetail(res, fallback), httpErrorStatus(res))
  }
  return (await res.json()) as T
}

export async function listClockMarks(): Promise<ClockMark[]> {
  return parseClock(await fetch(PATH, { headers: requireAuthHeaders() }), "Błąd listy zegarów D&D", 200)
}

export async function persistClockMark(payload: ClockMarkWrite): Promise<ClockMark> {
  const headers = { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" }
  return parseClock(
    await fetch(PATH, { method: "POST", headers, body: JSON.stringify(payload) }),
    "Błąd zapisu zegara D&D",
    201,
  )
}
