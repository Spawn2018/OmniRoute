import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/circle-sims"
const PAIR_PATH = "/api/v1/circle-sim-pairs"

export type CircleSimRow = {
  id: string
  organization_id: string
  sim_code: string
  unload_unlocode: string
  load_unlocode: string
  source_ref: string
}

export type CircleSimPairRow = {
  organization_id: string
  left_sim_id: string
  right_sim_id: string
  left_sim_code: string
  right_sim_code: string
  unload_unlocode: string
  load_unlocode: string
}

export type CircleSimWrite = {
  sim_code: string
  unload_unlocode: string
  load_unlocode: string
  source_ref: string
}

export function circleWrite(draft: {
  codeStamp: string
  unloadStamp: string
  loadStamp: string
  originStamp: string
}): CircleSimWrite {
  return {
    sim_code: draft.codeStamp.trim(),
    unload_unlocode: draft.unloadStamp.trim(),
    load_unlocode: draft.loadStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

async function parseCircle<T>(res: Response, fallback: string, ok: number): Promise<T> {
  if (res.status !== ok) {
    throw new ApiError(await readApiDetail(res, fallback), httpErrorStatus(res))
  }
  return (await res.json()) as T
}

export async function listCircleSims(): Promise<CircleSimRow[]> {
  return parseCircle(
    await fetch(PATH, { headers: requireAuthHeaders() }),
    "Błąd listy kółek",
    200,
  )
}

export async function listCircleSimPairs(): Promise<CircleSimPairRow[]> {
  return parseCircle(
    await fetch(PAIR_PATH, { headers: requireAuthHeaders() }),
    "Błąd listy par kółek",
    200,
  )
}

export async function persistCircleSim(payload: CircleSimWrite): Promise<CircleSimRow> {
  return parseCircle(
    await fetch(PATH, {
      method: "POST",
      headers: { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),
    "Błąd zapisu kółka",
    201,
  )
}
