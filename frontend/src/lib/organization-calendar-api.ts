import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type OrganizationCalendarRow = {
  id: string
  organization_id: string
  country_code: string
  calendar_day: string
  day_kind: string
  source_ref: string
  superseded_by: string | null
}

export type CalendarDayWrite = {
  country_code: string
  calendar_day: string
  day_kind: string
  source_ref: string
}

const PATH = "/api/v1/organization-calendars"

export function calendarDayWrite(args: {
  country: string
  day: string
  kind: string
}): CalendarDayWrite {
  return {
    country_code: args.country.trim().toUpperCase(),
    calendar_day: args.day.trim(),
    day_kind: args.kind.trim(),
    source_ref: "tenant:manual",
  }
}

export async function fetchCalendarDays(country: string): Promise<OrganizationCalendarRow[]> {
  const query = new URLSearchParams({ country_code: country })
  const reply = await fetch(`${PATH}?${query}`, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy kalendarza"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as OrganizationCalendarRow[]
}

export async function fetchWorkingDay(args: {
  country: string
  day: string
}): Promise<{ is_working_day: boolean }> {
  const query = new URLSearchParams({
    country_code: args.country,
    calendar_day: args.day,
  })
  const reply = await fetch(`${PATH}/working-day?${query}`, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd dnia roboczego"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as { is_working_day: boolean }
}

export async function saveCalendarDay(payload: CalendarDayWrite): Promise<OrganizationCalendarRow> {
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
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu dnia"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as OrganizationCalendarRow
}
