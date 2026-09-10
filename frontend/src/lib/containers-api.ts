import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ContainerRow = {
  id: string
  organization_id: string
  container_no: string
  iso_size_type: string
  shipment_id: string | null
  source_ref: string
  seal_no_1: string | null
  seal_no_2: string | null
  seal_no_3: string | null
  vessel_name: string | null
  voyage_no: string | null
  remarks: string | null
  cargo_description: string | null
  packaging_code: string | null
  ref_1: string | null
  ref_2: string | null
  ref_3: string | null
  ref_4: string | null
  ref_5: string | null
  reefer: boolean
  pickup_terminal: string | null
  return_terminal: string | null
  bl_kind: string | null
  free_time_origin_h: number | null
  free_time_dest_h: number | null
  si_cutoff_at: string | null
  ams_cutoff_at: string | null
  cy_cutoff_at: string | null
  cfs_cutoff_at: string | null
  vgm_kg: string | null
  vgm_method: string | null
  vgm_cutoff_at: string | null
  superseded_by: string | null
}

export type ContainerWrite = {
  container_no: string
  iso_size_type: string
  shipment_id: string | null
  source_ref: string
  seal_no_1: string | null
  seal_no_2: string | null
  seal_no_3: string | null
  vessel_name: string | null
  voyage_no: string | null
  remarks: string | null
  cargo_description: string | null
  packaging_code: string | null
  ref_1: string | null
  ref_2: string | null
  ref_3: string | null
  ref_4: string | null
  ref_5: string | null
  reefer: boolean
  pickup_terminal?: string | null
  return_terminal?: string | null
  bl_kind?: string | null
  free_time_origin_h?: number | null
  free_time_dest_h?: number | null
  si_cutoff_at?: string | null
  ams_cutoff_at?: string | null
  cy_cutoff_at?: string | null
  cfs_cutoff_at?: string | null
  vgm_kg?: string | null
  vgm_method?: string | null
  vgm_cutoff_at?: string | null
}

const PATH = "/api/v1/containers"

export function optionalToken(raw: string): string | null {
  const token = raw.trim()
  return token === "" ? null : token
}

export function optionalHours(raw: string): number | null {
  const token = raw.trim()
  if (token === "") {
    return null
  }
  return Number.parseInt(token, 10)
}

export function containerWrite(args: {
  number: string
  sizeType: string
  shipment: string
  seal: string
  seal2: string
  seal3: string
  vessel: string
  voyage: string
  note: string
  goods: string
  pack: string
  mark: string
  mark2: string
  mark3: string
  mark4: string
  mark5: string
  cold: boolean
}): ContainerWrite {
  return {
    container_no: args.number.trim(),
    iso_size_type: args.sizeType.trim(),
    shipment_id: optionalToken(args.shipment),
    source_ref: "tenant:manual",
    seal_no_1: optionalToken(args.seal),
    seal_no_2: optionalToken(args.seal2),
    seal_no_3: optionalToken(args.seal3),
    vessel_name: optionalToken(args.vessel),
    voyage_no: optionalToken(args.voyage),
    remarks: optionalToken(args.note),
    cargo_description: optionalToken(args.goods),
    packaging_code: optionalToken(args.pack),
    ref_1: optionalToken(args.mark),
    ref_2: optionalToken(args.mark2),
    ref_3: optionalToken(args.mark3),
    ref_4: optionalToken(args.mark4),
    ref_5: optionalToken(args.mark5),
    reefer: args.cold,
  }
}

export async function fetchContainers(sizeType: string): Promise<ContainerRow[]> {
  const suffix = sizeType === "" ? "" : `?iso_size_type=${encodeURIComponent(sizeType)}`
  const reply = await fetch(`${PATH}${suffix}`, { headers: requireAuthHeaders() })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy kontenerów"), httpErrorStatus(reply))
  }
  return (await reply.json()) as ContainerRow[]
}

export async function saveContainer(payload: ContainerWrite): Promise<ContainerRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu kontenera"), httpErrorStatus(reply))
  }
  return (await reply.json()) as ContainerRow
}
