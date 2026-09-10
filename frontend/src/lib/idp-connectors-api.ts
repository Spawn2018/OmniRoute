import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/idp-connectors"

export type IdpConnectorRow = {
  id: string
  organization_id: string
  connector_code: string
  provider_code: string
  public_domain: string | null
  source_ref: string
}

export type IdpConnectorWrite = {
  connector_code: string
  provider_code: string
  source_ref: string
  public_domain: string | null
}

export function idpConnectorWrite(draft: {
  markCode: string
  providerToken: string
  hostLabel: string
  originHint: string
}): IdpConnectorWrite {
  const host = draft.hostLabel.trim()
  return {
    connector_code: draft.markCode.trim(),
    provider_code: draft.providerToken.trim(),
    source_ref: draft.originHint.trim(),
    public_domain: host === "" ? null : host,
  }
}

export async function listIdpConnectors(): Promise<IdpConnectorRow[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(await readApiDetail(listed, "Błąd listy konektorów IdP"), httpErrorStatus(listed))
  }
  return (await listed.json()) as IdpConnectorRow[]
}

export async function persistIdpConnector(payload: IdpConnectorWrite): Promise<IdpConnectorRow> {
  const saved = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (saved.status !== 201) {
    throw new ApiError(await readApiDetail(saved, "Błąd zapisu konektora IdP"), httpErrorStatus(saved))
  }
  return (await saved.json()) as IdpConnectorRow
}
