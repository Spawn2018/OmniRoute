import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type OrganizationSetting = {
  id: string
  organization_id: string
  setting_key: string
  setting_value: string
}

export function organizationSettingUpsertBody(args: {
  settingKey: string
  settingValue: string
}): { setting_key: string; setting_value: string } {
  return {
    setting_key: args.settingKey.trim(),
    setting_value: args.settingValue.trim(),
  }
}

async function readSetting(response: Response, fallback: string): Promise<OrganizationSetting> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as OrganizationSetting
}

export async function fetchOrganizationSettings(): Promise<OrganizationSetting[]> {
  const response = await fetch("/api/v1/organization-settings", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy ustawień"), httpErrorStatus(response))
  }
  return (await response.json()) as OrganizationSetting[]
}

export function rolloutSettings<Row extends { setting_key: string }>(rows: readonly Row[]): Row[] {
  return rows.filter((row) => row.setting_key === "default_currency")
}

export function inquiryDefaultN(rows: readonly OrganizationSetting[]): number {
  const found = rows.find((row) => row.setting_key === "inquiry_default_n")
  if (found === undefined) {
    return 3
  }
  const parsed = Number.parseInt(found.setting_value, 10)
  if (!Number.isInteger(parsed) || parsed < 1 || parsed > 20) {
    return 3
  }
  return parsed
}

export async function upsertOrganizationSetting(body: {
  setting_key: string
  setting_value: string
}): Promise<OrganizationSetting> {
  const response = await fetch("/api/v1/organization-settings", {
    method: "PUT",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readSetting(response, "Błąd zapisu ustawienia")
}
