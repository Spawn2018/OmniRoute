import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ResourceRow = {
  id: string
  organization_id: string
  resource_kind: string
  display_name: string
  registration_no: string | null
  capacity_kg: string | null
  capacity_ldm: string | null
  capacity_m3: string | null
  inventory_no: string | null
  adr_certified: boolean | null
  source_ref: string
  superseded_by: string | null
}

export type ResourceWrite = {
  resource_kind: string
  display_name: string
  registration_no: string | null
  capacity_kg: string | null
  capacity_ldm: string | null
  capacity_m3: string | null
  inventory_no: string | null
  adr_certified: boolean | null
  source_ref: string
}

const PATH = "/api/v1/resources"

export function resourceWrite(args: {
  kind: string
  label: string
  plate: string
  capacityKg: string
  capacityLdm: string
  capacityM3: string
  inventoryNo: string
  adr: string
}): ResourceWrite {
  const plate = args.plate.trim()
  const capacityKg = args.capacityKg.trim()
  const capacityLdm = args.capacityLdm.trim()
  const capacityM3 = args.capacityM3.trim()
  const inventoryNo = args.inventoryNo.trim()
  return {
    resource_kind: args.kind.trim(),
    display_name: args.label.trim(),
    registration_no: plate === "" ? null : plate,
    inventory_no: inventoryNo === "" ? null : inventoryNo,
    adr_certified: args.adr === "true" ? true : args.adr === "false" ? false : null,
    capacity_kg: capacityKg === "" ? null : capacityKg,
    capacity_ldm: capacityLdm === "" ? null : capacityLdm,
    capacity_m3: capacityM3 === "" ? null : capacityM3,
    source_ref: "tenant:manual",
  }
}

export async function fetchResources(kind: string): Promise<ResourceRow[]> {
  const query = new URLSearchParams()
  if (kind !== "") {
    query.set("resource_kind", kind)
  }
  const suffix = query.size === 0 ? "" : `?${query}`
  const reply = await fetch(`${PATH}${suffix}`, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy floty"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as ResourceRow[]
}

export async function saveResource(payload: ResourceWrite): Promise<ResourceRow> {
  const auth = requireAuthHeaders()
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      Authorization: auth.Authorization,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu zasobu"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as ResourceRow
}
