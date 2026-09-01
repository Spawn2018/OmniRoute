import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type Party = {
  id: string
  organization_id: string
  legal_name: string
  short_name: string | null
  tax_id: string | null
  country_code: string
  roles: string[]
  credit_limit: string | null
  credit_currency: string | null
  is_active: boolean
  source_ref: string
}

export type PartyDraft = {
  legal_name: string
  tax_id: string
  source: string
  vies_valid: boolean | null
}

export type PartyContact = {
  id: string
  party_id: string
  name: string
  email: string | null
  phone: string | null
  position: string | null
  is_primary: boolean
}

export type PartyBankAccount = {
  id: string
  party_id: string
  iban: string
  currency: string
  bank_name: string | null
  whitelist_status: string
}

export type PartyEmailDomain = {
  id: string
  party_id: string
  domain: string
  source_ref: string
}

export type PartyChargeOverride = {
  id: string
  party_id: string
  charge_code: string
  amount: string
  currency: string
  lane_pattern: string | null
  basis: string | null
  source_ref: string
}

export type CarrierProfile = {
  id: string
  party_id: string
  scac_code: string | null
  is_nvocc: boolean
  rate_source_email: string | null
  api_adapter: string
  dcsa_tnt_version: string | null
}

export function partyCreateBody(args: {
  legalName: string
  countryCode: string
  taxId: string
  rolesText: string
}): { legal_name: string; country_code: string; tax_id: string; roles: string[] } {
  const roles = args.rolesText
    .split(",")
    .map((part) => part.trim())
    .filter((part) => part.length > 0)
  return {
    legal_name: args.legalName.trim(),
    country_code: args.countryCode.trim().toUpperCase(),
    tax_id: args.taxId.replace(/[\s-]/g, ""),
    roles,
  }
}

async function parseBody<T>(response: Response, fallback: string): Promise<T> {
  if (!response.ok) {
    const detail = await readApiDetail(response, fallback)
    throw new ApiError(detail, httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchParties(): Promise<Party[]> {
  const response = await fetch("/api/v1/parties", { headers: requireAuthHeaders() })
  return parseBody<Party[]>(response, "Błąd listy kontrahentów")
}

export async function createParty(body: {
  legal_name: string
  country_code: string
  tax_id: string
  roles: string[]
}): Promise<Party> {
  const taxId = body.tax_id.trim()
  const response = await fetch("/api/v1/parties", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({
      legal_name: body.legal_name,
      country_code: body.country_code,
      roles: body.roles,
      tax_id: taxId === "" ? null : taxId,
    }),
  })
  return parseBody<Party>(response, "Błąd zapisu kontrahenta")
}

export async function resolveParty(taxId: string): Promise<Party> {
  const params = new URLSearchParams({ tax_id: taxId })
  const response = await fetch(`/api/v1/parties/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return parseBody<Party>(response, "Nieznany kontrahent")
}

export async function lookupParty(taxId: string, countryCode: string): Promise<PartyDraft> {
  const response = await fetch("/api/v1/parties/lookup", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ tax_id: taxId, country_code: countryCode }),
  })
  return parseBody<PartyDraft>(response, "Błąd lookupu kontrahenta")
}

export async function fetchContacts(partyId: string): Promise<PartyContact[]> {
  const response = await fetch(`/api/v1/parties/${partyId}/contacts`, {
    headers: requireAuthHeaders(),
  })
  return parseBody<PartyContact[]>(response, "Błąd listy kontaktów")
}

export async function createContact(partyId: string, name: string): Promise<PartyContact> {
  const response = await fetch(`/api/v1/parties/${partyId}/contacts`, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  })
  return parseBody<PartyContact>(response, "Błąd zapisu kontaktu")
}

export async function fetchBankAccounts(partyId: string): Promise<PartyBankAccount[]> {
  const response = await fetch(`/api/v1/parties/${partyId}/bank-accounts`, {
    headers: requireAuthHeaders(),
  })
  return parseBody<PartyBankAccount[]>(response, "Błąd listy rachunków")
}

export async function createBankAccount(
  partyId: string,
  iban: string,
  currency: string,
): Promise<PartyBankAccount> {
  const response = await fetch(`/api/v1/parties/${partyId}/bank-accounts`, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ iban, currency }),
  })
  return parseBody<PartyBankAccount>(response, "Błąd zapisu rachunku")
}

export async function fetchEmailDomains(partyId: string): Promise<PartyEmailDomain[]> {
  const response = await fetch(`/api/v1/parties/${partyId}/email-domains`, {
    headers: requireAuthHeaders(),
  })
  return parseBody<PartyEmailDomain[]>(response, "Błąd listy domen")
}

export async function createEmailDomain(partyId: string, domain: string): Promise<PartyEmailDomain> {
  const response = await fetch(`/api/v1/parties/${partyId}/email-domains`, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ domain }),
  })
  return parseBody<PartyEmailDomain>(response, "Błąd zapisu domeny")
}

export async function fetchChargeOverrides(partyId: string): Promise<PartyChargeOverride[]> {
  const response = await fetch(`/api/v1/parties/${partyId}/charge-overrides`, {
    headers: requireAuthHeaders(),
  })
  return parseBody<PartyChargeOverride[]>(response, "Błąd listy wyjątków stawek")
}

export async function createChargeOverride(
  partyId: string,
  chargeCode: string,
  amount: string,
  currency: string,
): Promise<PartyChargeOverride> {
  const response = await fetch(`/api/v1/parties/${partyId}/charge-overrides`, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ charge_code: chargeCode, amount, currency }),
  })
  return parseBody<PartyChargeOverride>(response, "Błąd zapisu wyjątku stawki")
}

export async function upsertCarrierProfile(
  partyId: string,
  scacCode: string,
): Promise<CarrierProfile> {
  const response = await fetch(`/api/v1/parties/${partyId}/carrier-profile`, {
    method: "PUT",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ scac_code: scacCode === "" ? null : scacCode, api_adapter: "none" }),
  })
  return parseBody<CarrierProfile>(response, "Błąd zapisu profilu armatora")
}
