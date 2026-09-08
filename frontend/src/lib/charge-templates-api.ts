import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/charge-templates"

export type BundleSlot = {
  id: string
  organization_id: string
  template_code: string
  charge_code: string
  valid_from: string
  valid_until: string
  source_ref: string
}

export type BundleSlotWrite = {
  template_code: string
  charge_code: string
  valid_from: string
  valid_until: string
  source_ref: string
}

export function bundleWrite(args: {
  packToken: string
  feeToken: string
  fromStamp: string
  untilStamp: string
  originStamp: string
}): BundleSlotWrite {
  return {
    template_code: args.packToken.trim(),
    charge_code: args.feeToken.trim().toUpperCase(),
    valid_from: args.fromStamp.trim(),
    valid_until: args.untilStamp.trim(),
    source_ref: args.originStamp.trim(),
  }
}

export async function listBundleSlots(): Promise<BundleSlot[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy szablonów opłat"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as BundleSlot[]
}

export async function persistBundleSlot(payload: BundleSlotWrite): Promise<BundleSlot> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "bundle-slot",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu szablonu opłat"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as BundleSlot
}
