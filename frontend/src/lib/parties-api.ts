import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type Party = {
  id: string
  organization_id: string
  legal_name: string
  short_name: string | null
  tax_id: string | null
  vat_eu: string | null
  eori: string | null
  duns: string | null
  country_code: string
  roles: string[]
  is_sole_trader: boolean
  parent_party_id: string | null
  credit_limit: string | null
  credit_currency: string | null
  is_active: boolean
  source_ref: string
  sanctions_list_ref: string | null
  sanctions_checked_at: string | null
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
  tracking_consent: boolean
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

export type PartyCreatePayload = {
  legal_name: string
  country_code: string
  tax_id: string
  roles: string[]
  vat_eu?: string
  eori?: string
  duns?: string
  is_sole_trader?: boolean
  parent_party_id?: string
}

export function partyCreateBody(args: {
  legalName: string
  countryCode: string
  taxId: string
  rolesText: string
  vatEu?: string
  eori?: string
  duns?: string
  isSoleTrader?: boolean
  parentPartyId?: string
}): PartyCreatePayload {
  const roles = args.rolesText
    .split(",")
    .map((part) => part.trim())
    .filter((part) => part.length > 0)
  const vatEu = (args.vatEu ?? "").replace(/[\s-]/g, "").toUpperCase()
  const eori = (args.eori ?? "").replace(/[\s-]/g, "").toUpperCase()
  const duns = (args.duns ?? "").replace(/\D/g, "")
  return {
    legal_name: args.legalName.trim(),
    country_code: args.countryCode.trim().toUpperCase(),
    tax_id: args.taxId.replace(/[\s-]/g, ""),
    roles,
    ...(vatEu === "" ? {} : { vat_eu: vatEu }),
    ...(eori === "" ? {} : { eori }),
    ...(duns === "" ? {} : { duns }),
    ...(args.isSoleTrader === true ? { is_sole_trader: true } : {}),
    ...(args.parentPartyId && args.parentPartyId.trim() !== ""
      ? { parent_party_id: args.parentPartyId.trim() }
      : {}),
  }
}

export function partyConflictHref(payload: unknown): string | null {
  if (typeof payload !== "object" || payload === null || !("href" in payload)) {
    return null
  }
  const href = (payload as { href: unknown }).href
  if (typeof href !== "string" || !href.startsWith("/parties/")) {
    return null
  }
  return href
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

export function sanctionsParties<Row extends { is_active: boolean }>(
  parties: readonly Row[],
): Row[] {
  return parties.filter((row) => row.is_active)
}

export async function createParty(body: PartyCreatePayload): Promise<Party> {
  const taxId = body.tax_id.trim()
  const response = await fetch("/api/v1/parties", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({
      legal_name: body.legal_name,
      country_code: body.country_code,
      roles: body.roles,
      tax_id: taxId === "" ? null : taxId,
      vat_eu: body.vat_eu ?? null,
      eori: body.eori ?? null,
      duns: body.duns ?? null,
      is_sole_trader: body.is_sole_trader ?? false,
      parent_party_id: body.parent_party_id ?? null,
    }),
  })
  if (response.status === 409) {
    const payload: unknown = await response.json().catch(() => null)
    const href = partyConflictHref(payload)
    const detail =
      typeof payload === "object" && payload !== null && "detail" in payload
        ? String((payload as { detail: unknown }).detail)
        : "Kontrahent już istnieje"
    throw new ApiError(href === null ? detail : `${detail} ${href}`, 409)
  }
  return parseBody<Party>(response, "Błąd zapisu kontrahenta")
}

export async function resolveParty(taxId: string): Promise<Party> {
  const params = new URLSearchParams({ tax_id: taxId })
  const response = await fetch(`/api/v1/parties/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return parseBody<Party>(response, "Nieznany kontrahent")
}

export async function resolvePartyEmail(email: string): Promise<Party> {
  const params = new URLSearchParams({ email })
  const response = await fetch(`/api/v1/parties/resolve-email?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return parseBody<Party>(response, "Nieznana domena mailowa")
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

export async function createContact(
  partyId: string,
  name: string,
  trackingConsent = false,
): Promise<PartyContact> {
  const response = await fetch(`/api/v1/parties/${partyId}/contacts`, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ name, tracking_consent: trackingConsent }),
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

export type IbanDraft = {
  iban: string
  whitelist_status: string
}

export async function lookupIban(iban: string): Promise<IbanDraft> {
  const response = await fetch("/api/v1/parties/iban-lookup", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ iban }),
  })
  return parseBody<IbanDraft>(response, "Błąd lookupu IBAN")
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

export async function screenPartySanctions(
  partyId: string,
  body: { sanctions_list_ref: string },
): Promise<Party> {
  const response = await fetch(`/api/v1/parties/${partyId}/screen-sanctions`, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return parseBody<Party>(response, "Błąd zapisu sprawdzenia listy")
}
