import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/pallet-pool-marks"

export type PalletPoolMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  pool_kind: string
  source_ref: string
}

export type PalletPoolWrite = {
  mark_code: string
  pool_kind: string
  source_ref: string
}

export function packPalletPoolWrite(
  code: string,
  kind: string,
  origin: string,
): PalletPoolWrite {
  return {
    mark_code: code.trim(),
    pool_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function loadJson<T>(res: Response, fail: string, ok: number): Promise<T> {
  if (res.status === ok) {
    return (await res.json()) as T
  }
  throw new ApiError(await readApiDetail(res, fail), httpErrorStatus(res))
}

export async function listPalletPoolMarks(): Promise<PalletPoolMarkRow[]> {
  const res = await fetch(PATH, { headers: requireAuthHeaders() })
  return loadJson(res, "Lista znaczników pallet-pool niedostępna", 200)
}

export async function savePalletPoolMark(body: PalletPoolWrite): Promise<PalletPoolMarkRow> {
  const res = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return loadJson(res, "Zapis znacznika pallet-pool nieudany", 201)
}
