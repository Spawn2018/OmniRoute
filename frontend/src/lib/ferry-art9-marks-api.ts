import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/ferry-art9-marks"

export type FerryArt9MarkRow = {
  id: string
  organization_id: string
  mark_code: string
  ferry_kind: string
  source_ref: string
}

export type FerryArt9Write = {
  mark_code: string
  ferry_kind: string
  source_ref: string
}

export function buildFerryArt9Write(
  code: string,
  kind: string,
  origin: string,
): FerryArt9Write {
  return {
    mark_code: code.trim(),
    ferry_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function decode<T>(res: Response, label: string, code: number): Promise<T> {
  if (res.status === code) {
    return (await res.json()) as T
  }
  throw new ApiError(await readApiDetail(res, label), httpErrorStatus(res))
}

export async function listFerryArt9Marks(): Promise<FerryArt9MarkRow[]> {
  const res = await fetch(PATH, { headers: requireAuthHeaders() })
  return decode(res, "Lista ferry art. 9 niedostępna", 200)
}

export async function createFerryArt9Mark(body: FerryArt9Write): Promise<FerryArt9MarkRow> {
  const res = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return decode(res, "Zapis ferry art. 9 nieudany", 201)
}
