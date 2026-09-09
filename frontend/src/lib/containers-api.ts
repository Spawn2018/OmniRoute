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
  superseded_by: string | null
}

export type ContainerWrite = {
  container_no: string
  iso_size_type: string
  shipment_id: string | null
  source_ref: string
  seal_no_1: string | null
  seal_no_2: string | null
}

const PATH = "/api/v1/containers"

function optionalId(raw: string): string | null {
  const token = raw.trim()
  return token === "" ? null : token
}

export function containerWrite(args: {
  number: string
  sizeType: string
  shipment: string
  seal: string
  seal2: string
}): ContainerWrite {
  const seal = args.seal.trim()
  const seal2 = args.seal2.trim()
  return {
    container_no: args.number.trim(),
    iso_size_type: args.sizeType.trim(),
    shipment_id: optionalId(args.shipment),
    source_ref: "tenant:manual",
    seal_no_1: seal === "" ? null : seal,
    seal_no_2: seal2 === "" ? null : seal2,
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
