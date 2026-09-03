import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type OperationalException = {
  id: string
  organization_id: string
  shipment_id: string
  exception_kind: string
  source_ref: string
}

export async function fetchOperationalExceptions(): Promise<OperationalException[]> {
  const response = await fetch("/api/v1/operational-exceptions", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy wyjątków"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as OperationalException[]
}

export async function createOperationalException(input: {
  shipment_id: string
  exception_kind: string
  source_ref: string
}): Promise<OperationalException> {
  const response = await fetch("/api/v1/operational-exceptions", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd zapisu wyjątku"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as OperationalException
}
