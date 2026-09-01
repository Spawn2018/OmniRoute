import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type NbpRate = {
  id: string
  organization_id: string
  currency: string
  rate_date: string
  mid: string
  source_ref: string
}

export function nbpRateCreateBody(input: {
  currency: string
  rateDate: string
  mid: string
}): { currency: string; rate_date: string; mid: string } {
  return {
    currency: input.currency.trim().toUpperCase(),
    rate_date: input.rateDate,
    mid: input.mid.trim(),
  }
}

async function readNbpRate(response: Response, fallback: string): Promise<NbpRate> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as NbpRate
}

export async function fetchNbpRates(): Promise<NbpRate[]> {
  const response = await fetch("/api/v1/nbp-rates", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy kursów NBP"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as NbpRate[]
}

export async function createNbpRate(body: {
  currency: string
  rate_date: string
  mid: string
}): Promise<NbpRate> {
  const response = await fetch("/api/v1/nbp-rates", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readNbpRate(response, "Błąd zapisu kursu NBP")
}

export async function resolveNbpRate(currency: string, onDate: string): Promise<NbpRate> {
  const params = new URLSearchParams({ currency, on_date: onDate })
  const response = await fetch(`/api/v1/nbp-rates/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return readNbpRate(response, "Brak kursu NBP")
}
