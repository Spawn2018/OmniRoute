import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/bin-pack-marks"

export type BinPackMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  pack_kind: string
  source_ref: string
}

export type BinPackWrite = {
  mark_code: string
  pack_kind: string
  source_ref: string
}

export function packBinPackWrite(
  code: string,
  kind: string,
  origin: string,
): BinPackWrite {
  return {
    mark_code: code.trim(),
    pack_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function loadJson<T>(res: Response, fail: string, ok: number): Promise<T> {
  if (res.status === ok) {
    return (await res.json()) as T
  }
  throw new ApiError(await readApiDetail(res, fail), httpErrorStatus(res))
}

export async function listBinPackMarks(): Promise<BinPackMarkRow[]> {
  const res = await fetch(PATH, { headers: requireAuthHeaders() })
  return loadJson(res, "Lista znaczników bin-pack niedostępna", 200)
}

export async function saveBinPackMark(body: BinPackWrite): Promise<BinPackMarkRow> {
  const res = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return loadJson(res, "Zapis znacznika bin-pack nieudany", 201)
}
