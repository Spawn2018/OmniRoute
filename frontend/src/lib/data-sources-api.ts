import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type DataSourceRow = {
  id: string
  organization_id: string
  source_code: string
  license_label: string
  rights_scope: string
  source_ref: string
}

export type DataSourcePayload = {
  source_code: string
  license_label: string
  rights_scope: string
  source_ref: string
}

const PATH = "/api/v1/data-sources"

export function buildDataSourceWrite(args: {
  code: string
  license: string
  rights: string
  origin: string
}): DataSourcePayload {
  return {
    source_code: args.code.trim(),
    license_label: args.license.trim(),
    rights_scope: args.rights.trim(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchDataSources(): Promise<DataSourceRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udalo sie wczytac katalogu zrodel"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as DataSourceRow[]
}

export async function saveDataSource(
  payload: DataSourcePayload,
): Promise<DataSourceRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "data-source-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udalo sie zapisac zrodla danych"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as DataSourceRow
}
