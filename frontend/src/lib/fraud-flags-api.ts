import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type FraudFlagRow = {
  id: string
  organization_id: string
  party_id: string
  flag_kind: string
  source_ref: string
}

const FLAGS_PATH = "/api/v1/fraud-flags"

export async function listFraudFlags(): Promise<FraudFlagRow[]> {
  const auth = requireAuthHeaders()
  const reply = await fetch(FLAGS_PATH, { headers: auth })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy flag oszustwa"), httpErrorStatus(reply))
  }
  return (await reply.json()) as FraudFlagRow[]
}

export async function saveFraudFlag(payload: {
  party_id: string
  flag_kind: string
  source_ref: string
}): Promise<FraudFlagRow> {
  const auth = requireAuthHeaders()
  const reply = await fetch(FLAGS_PATH, {
    method: "POST",
    headers: new Headers({
      ...auth,
      Accept: "application/json",
      "Content-Type": "application/json",
    }),
    body: JSON.stringify(payload),
  })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu flagi oszustwa"), httpErrorStatus(reply))
  }
  return (await reply.json()) as FraudFlagRow
}
