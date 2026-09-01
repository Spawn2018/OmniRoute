import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  ResolveTokenForm,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  createBankAccount,
  createChargeOverride,
  createContact,
  createEmailDomain,
  createParty,
  fetchBankAccounts,
  fetchChargeOverrides,
  fetchContacts,
  fetchEmailDomains,
  fetchParties,
  lookupParty,
  partyCreateBody,
  resolveParty,
  resolvePartyEmail,
  upsertCarrierProfile,
  type Party,
  type PartyDraft,
} from "@/lib/parties-api"
import {
  EMPTY_SCORECARD_DRAFT,
  fetchPartyScorecard,
  scorecardUpsertBody,
  upsertPartyScorecard,
} from "@/lib/party-scorecards-api"
import {
  EMPTY_SOP_DRAFT,
  approveCustomerSop,
  createCustomerSop,
  customerSopCreateBody,
  fetchCustomerSops,
} from "@/lib/customer-sops-api"
import { getTenantContext } from "@/lib/tenant"

const columnHelper = createColumnHelper<Party>()

const columns = [
  columnHelper.accessor("legal_name", {
    id: "legal_name",
    header: "Nazwa",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("tax_id", {
    id: "tax_id",
    header: "Tax ID",
    cell: (info) => <span className="font-mono text-xs">{info.getValue() ?? "—"}</span>,
  }),
  columnHelper.accessor("country_code", {
    id: "country_code",
    header: "Kraj",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("roles", {
    id: "roles",
    header: "Role",
    cell: (info) => info.getValue().join(", "),
  }),
  columnHelper.accessor("credit_limit", {
    id: "credit_limit",
    header: "Limit",
    cell: (info) => {
      const amount = info.getValue()
      const currency = info.row.original.credit_currency
      if (amount === null || currency === null) {
        return "—"
      }
      return <Money amount={amount} currency={currency} />
    },
  }),
]

const COLUMN_LABELS = {
  legal_name: "Nazwa",
  tax_id: "Tax ID",
  country_code: "Kraj",
  roles: "Role",
  credit_limit: "Limit",
}

export function PartyCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [legalName, setLegalName] = useState("")
  const [countryCode, setCountryCode] = useState("PL")
  const [taxId, setTaxId] = useState("")
  const [rolesText, setRolesText] = useState("customer")
  const [resolved, setResolved] = useState<Party | null>(null)
  const [resolvedEmail, setResolvedEmail] = useState<Party | null>(null)
  const [draft, setDraft] = useState<PartyDraft | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [contactName, setContactName] = useState("")
  const [iban, setIban] = useState("")
  const [ibanCurrency, setIbanCurrency] = useState("PLN")
  const [domain, setDomain] = useState("")
  const [overrideCode, setOverrideCode] = useState("")
  const [overrideAmount, setOverrideAmount] = useState("")
  const [overrideCurrency, setOverrideCurrency] = useState("USD")
  const [scac, setScac] = useState("")
  const [scoreDraft, setScoreDraft] = useState(EMPTY_SCORECARD_DRAFT)
  const [sopDraft, setSopDraft] = useState(EMPTY_SOP_DRAFT)

  const listQuery = useQuery({
    queryKey: ["parties", ctx.organizationId],
    queryFn: fetchParties,
    enabled: Boolean(ctx.organizationId && ctx.userId),
    retry: false,
  })

  const contactsQuery = useQuery({
    queryKey: ["party-contacts", selectedId],
    queryFn: () => fetchContacts(selectedId ?? ""),
    enabled: selectedId !== null,
    retry: false,
  })
  const banksQuery = useQuery({
    queryKey: ["party-banks", selectedId],
    queryFn: () => fetchBankAccounts(selectedId ?? ""),
    enabled: selectedId !== null,
    retry: false,
  })
  const domainsQuery = useQuery({
    queryKey: ["party-email-domains", selectedId],
    queryFn: () => fetchEmailDomains(selectedId ?? ""),
    enabled: selectedId !== null,
    retry: false,
  })
  const overridesQuery = useQuery({
    queryKey: ["party-charge-overrides", selectedId],
    queryFn: () => fetchChargeOverrides(selectedId ?? ""),
    enabled: selectedId !== null,
    retry: false,
  })
  const scorecardQuery = useQuery({
    queryKey: ["party-scorecard", selectedId],
    queryFn: () => fetchPartyScorecard(selectedId ?? ""),
    enabled: selectedId !== null,
    retry: false,
  })
  const sopsQuery = useQuery({
    queryKey: ["customer-sops", ctx.organizationId],
    queryFn: fetchCustomerSops,
    enabled: selectedId !== null,
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () =>
      createParty(partyCreateBody({ legalName, countryCode, taxId, rolesText })),
    onSuccess: (row) => {
      setLegalName("")
      setTaxId("")
      setSelectedId(row.id)
      void queryClient.invalidateQueries({ queryKey: ["parties", ctx.organizationId] })
    },
  })

  const resolveMutation = useMutation({
    mutationFn: (token: string) => resolveParty(token),
    onSuccess: (row) => {
      setResolved(row)
      setSelectedId(row.id)
    },
    onError: () => {
      setResolved(null)
    },
  })

  const lookupMutation = useMutation({
    mutationFn: () => lookupParty(taxId, countryCode),
    onSuccess: (row) => {
      setDraft(row)
      setLegalName(row.legal_name)
      setTaxId(row.tax_id)
    },
    onError: () => {
      setDraft(null)
    },
  })

  const resolveEmailMutation = useMutation({
    mutationFn: resolvePartyEmail,
    onSuccess: (row) => {
      setResolvedEmail(row)
      setSelectedId(row.id)
    },
    onError: () => setResolvedEmail(null),
  })

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Katalog kontrahentów"
        subtitle="party M-10 · tax_id i mail domeny, nie luźna nazwa; lookup to szkic"
      />

      {!ctx.organizationId || !ctx.userId ? <TenantSessionNotice /> : null}

      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-2 xl:grid-cols-5"
        onSubmit={(event) => {
          event.preventDefault()
          createMutation.mutate()
        }}
      >
        <Input
          aria-label="Nazwa prawna"
          placeholder="ACME Sp. z o.o."
          value={legalName}
          onChange={(event) => setLegalName(event.target.value)}
          required
        />
        <Input
          aria-label="Kod kraju"
          placeholder="PL"
          value={countryCode}
          onChange={(event) => setCountryCode(event.target.value)}
          required
        />
        <Input
          aria-label="Identyfikator podatkowy"
          placeholder="NIP"
          value={taxId}
          onChange={(event) => setTaxId(event.target.value)}
        />
        <Input
          aria-label="Role kontrahenta"
          placeholder="customer, vendor"
          value={rolesText}
          onChange={(event) => setRolesText(event.target.value)}
          required
        />
        <div className="flex gap-2">
          <Button type="submit" disabled={createMutation.isPending || !ctx.organizationId}>
            Dodaj
          </Button>
          <Button
            type="button"
            variant="outline"
            disabled={lookupMutation.isPending || taxId.trim() === ""}
            onClick={() => lookupMutation.mutate()}
          >
            Lookup
          </Button>
        </div>
      </form>

      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}
      {lookupMutation.isError ? <CatalogError error={lookupMutation.error} /> : null}
      {draft !== null ? (
        <p className="text-xs text-muted-foreground">
          Szkic {draft.source}: {draft.legal_name} · {draft.tax_id}
        </p>
      ) : null}

      <ResolveTokenForm
        label="Sprawdź tax_id"
        placeholder="NIP albo VAT"
        pending={resolveMutation.isPending}
        resolved={resolved === null ? null : `${resolved.tax_id ?? "—"} · ${resolved.legal_name}`}
        onResolve={(token) => resolveMutation.mutate(token)}
      />
      {resolveMutation.isError ? <CatalogError error={resolveMutation.error} /> : null}

      <ResolveTokenForm
        label="Sprawdź mail"
        placeholder="ops@acme.test"
        pending={resolveEmailMutation.isPending}
        resolved={
          resolvedEmail === null ? null : `${resolvedEmail.legal_name} · ${resolvedEmail.tax_id ?? "—"}`
        }
        onResolve={(token) => resolveEmailMutation.mutate(token)}
      />
      {resolveEmailMutation.isError ? <CatalogError error={resolveEmailMutation.error} /> : null}

      {listQuery.isLoading ? <div className="text-sm text-muted-foreground">Ładowanie…</div> : null}
      {listQuery.isError ? <CatalogError error={listQuery.error} /> : null}
      {listQuery.data ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.parties.tableKey}
          columns={columns}
          data={listQuery.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Szukaj kontrahenta…"
        />
      ) : null}

      <label className="flex items-center gap-2 text-sm">
        Panel wybranego kontrahenta
        <Input
          aria-label="Identyfikator kontrahenta"
          placeholder="party_id"
          value={selectedId ?? ""}
          onChange={(event) => setSelectedId(event.target.value === "" ? null : event.target.value)}
        />
      </label>

      {selectedId !== null ? (
        <div className="grid gap-3 md:grid-cols-2">
          <fieldset className="space-y-2 rounded-md border border-border p-3">
            <legend className="text-sm font-medium">Kontakty</legend>
            <form
              className="flex gap-2"
              onSubmit={(event) => {
                event.preventDefault()
                createContact(selectedId, contactName).then(() => {
                  setContactName("")
                  void queryClient.invalidateQueries({ queryKey: ["party-contacts", selectedId] })
                })
              }}
            >
              <Input
                aria-label="Nazwa kontaktu"
                value={contactName}
                onChange={(event) => setContactName(event.target.value)}
                required
              />
              <Button type="submit">Dodaj</Button>
            </form>
            <p className="text-xs text-muted-foreground">
              {contactsQuery.data?.map((row) => row.name).join(", ") || "brak"}
            </p>
          </fieldset>

          <fieldset className="space-y-2 rounded-md border border-border p-3">
            <legend className="text-sm font-medium">Rachunki bank</legend>
            <form
              className="flex gap-2"
              onSubmit={(event) => {
                event.preventDefault()
                createBankAccount(selectedId, iban, ibanCurrency).then(() => {
                  setIban("")
                  void queryClient.invalidateQueries({ queryKey: ["party-banks", selectedId] })
                })
              }}
            >
              <Input
                aria-label="IBAN"
                value={iban}
                onChange={(event) => setIban(event.target.value)}
                required
              />
              <Input
                aria-label="Waluta rachunku"
                value={ibanCurrency}
                onChange={(event) => setIbanCurrency(event.target.value)}
                required
              />
              <Button type="submit">Dodaj</Button>
            </form>
            <p className="text-xs text-muted-foreground">
              {banksQuery.data?.map((row) => row.iban).join(", ") || "brak"}
            </p>
          </fieldset>

          <fieldset className="space-y-2 rounded-md border border-border p-3">
            <legend className="text-sm font-medium">Domena email-domain</legend>
            <form
              className="flex gap-2"
              onSubmit={(event) => {
                event.preventDefault()
                createEmailDomain(selectedId, domain).then(() => {
                  setDomain("")
                  void queryClient.invalidateQueries({
                    queryKey: ["party-email-domains", selectedId],
                  })
                })
              }}
            >
              <Input
                aria-label="Domena mailowa"
                value={domain}
                onChange={(event) => setDomain(event.target.value)}
                required
              />
              <Button type="submit">Dodaj</Button>
            </form>
            <p className="text-xs text-muted-foreground">
              {domainsQuery.data?.map((row) => row.domain).join(", ") || "brak"}
            </p>
          </fieldset>

          <fieldset className="space-y-2 rounded-md border border-border p-3">
            <legend className="text-sm font-medium">Profil carrier</legend>
            <form
              className="flex gap-2"
              onSubmit={(event) => {
                event.preventDefault()
                void upsertCarrierProfile(selectedId, scac)
              }}
            >
              <Input
                aria-label="Kod SCAC"
                value={scac}
                onChange={(event) => setScac(event.target.value)}
              />
              <Button type="submit">Zapisz</Button>
            </form>
          </fieldset>

          <fieldset className="space-y-2 rounded-md border border-border p-3 md:col-span-2">
            <legend className="text-sm font-medium">Wyjątek charge-override</legend>
            <form
              className="grid gap-2 md:grid-cols-4"
              onSubmit={(event) => {
                event.preventDefault()
                createChargeOverride(
                  selectedId,
                  overrideCode,
                  overrideAmount,
                  overrideCurrency,
                ).then(() => {
                  setOverrideCode("")
                  setOverrideAmount("")
                  void queryClient.invalidateQueries({
                    queryKey: ["party-charge-overrides", selectedId],
                  })
                })
              }}
            >
              <Input
                aria-label="Kod opłaty wyjątku"
                value={overrideCode}
                onChange={(event) => setOverrideCode(event.target.value)}
                required
              />
              <Input
                aria-label="Kwota wyjątku"
                value={overrideAmount}
                onChange={(event) => setOverrideAmount(event.target.value)}
                required
              />
              <Input
                aria-label="Waluta wyjątku"
                value={overrideCurrency}
                onChange={(event) => setOverrideCurrency(event.target.value)}
                required
              />
              <Button type="submit">Dodaj</Button>
            </form>
            <ul className="text-xs">
              {overridesQuery.data?.map((row) => (
                <li key={row.id}>
                  {row.charge_code}{" "}
                  <Money amount={row.amount} currency={row.currency} />
                </li>
              ))}
            </ul>
          </fieldset>

          <fieldset className="space-y-2 rounded-md border border-border p-3 md:col-span-2">
            <legend className="text-sm font-medium">Karta wyników</legend>
            <form
              className="grid gap-2 md:grid-cols-4"
              onSubmit={(event) => {
                event.preventDefault()
                void upsertPartyScorecard(
                  selectedId,
                  scorecardUpsertBody({ ...scoreDraft, partyId: selectedId }),
                ).then(() => {
                  void queryClient.invalidateQueries({ queryKey: ["party-scorecard", selectedId] })
                })
              }}
            >
              <Input
                aria-label="Wskaźnik odpowiedzi panelu"
                placeholder="response_rate 0–1"
                value={scoreDraft.responseRate}
                onChange={(event) =>
                  setScoreDraft({ ...scoreDraft, responseRate: event.target.value })
                }
              />
              <Input
                aria-label="Mediana godzin panelu"
                placeholder="median_response_hours"
                value={scoreDraft.medianHours}
                onChange={(event) =>
                  setScoreDraft({ ...scoreDraft, medianHours: event.target.value })
                }
              />
              <Input
                aria-label="Wielkość próby panelu"
                placeholder="sample_size"
                value={scoreDraft.sampleSize}
                onChange={(event) =>
                  setScoreDraft({ ...scoreDraft, sampleSize: event.target.value })
                }
              />
              <Button type="submit">Zapisz kartę</Button>
            </form>
            <p className="text-xs text-muted-foreground">
              {scorecardQuery.data
                ? `snapshot ${scorecardQuery.data.response_rate ?? "—"} · ${scorecardQuery.data.source_ref}`
                : "brak snapshotu"}
            </p>
          </fieldset>

          <fieldset className="space-y-2 rounded-md border border-border p-3 md:col-span-2">
            <legend className="text-sm font-medium">Procedury operacyjne</legend>
            <form
              className="grid gap-2 md:grid-cols-2"
              onSubmit={(event) => {
                event.preventDefault()
                void createCustomerSop(
                  customerSopCreateBody({ ...sopDraft, partyId: selectedId ?? "" }),
                ).then(() => {
                  setSopDraft(EMPTY_SOP_DRAFT)
                  void queryClient.invalidateQueries({
                    queryKey: ["customer-sops", ctx.organizationId],
                  })
                })
              }}
            >
              <Input
                aria-label="Kod procedury panelu"
                placeholder="pre_alert"
                value={sopDraft.code}
                onChange={(event) => setSopDraft({ ...sopDraft, code: event.target.value })}
                required
              />
              <Input
                aria-label="Tytuł procedury panelu"
                placeholder="tytuł"
                value={sopDraft.title}
                onChange={(event) => setSopDraft({ ...sopDraft, title: event.target.value })}
                required
              />
              <textarea
                aria-label="Treść procedury panelu"
                placeholder="treść operacyjna"
                className="min-h-20 w-full rounded-md border border-input bg-card px-3 py-1.5 text-sm md:col-span-2"
                value={sopDraft.body}
                onChange={(event) => setSopDraft({ ...sopDraft, body: event.target.value })}
                required
              />
              <Button type="submit">Dodaj szkic SOP</Button>
            </form>
            <ul className="text-xs">
              {sopsQuery.data
                ?.filter((row) => row.party_id === selectedId)
                .map((row) => (
                  <li key={row.id} className="flex items-center gap-2">
                    <span className="font-mono">{row.code}</span>
                    <span>{row.title}</span>
                    <span>{row.status}</span>
                    {row.status === "draft" ? (
                      <Button
                        type="button"
                        onClick={() => {
                          void approveCustomerSop(row.id).then(() => {
                            void queryClient.invalidateQueries({
                              queryKey: ["customer-sops", ctx.organizationId],
                            })
                          })
                        }}
                      >
                        Zatwierdź
                      </Button>
                    ) : null}
                  </li>
                ))}
            </ul>
          </fieldset>
        </div>
      ) : null}
    </div>
  )
}
