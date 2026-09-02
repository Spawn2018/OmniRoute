import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  createInboundMessage,
  fetchInboundMessages,
  inboundMessageCreateBody,
  type InboundMessage,
} from "@/lib/inbound-messages-api"
import {
  fetchContacts,
  fetchEmailDomains,
  fetchParties,
  resolvePartyEmail,
  type Party,
} from "@/lib/parties-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<InboundMessage>()
const columns = [
  helper.accessor("from_address", {
    header: "Nadawca",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  helper.accessor("subject", { header: "Temat" }),
  helper.accessor("status", { header: "Status" }),
  helper.accessor("source_ref", { header: "Źródło" }),
]
const COLUMN_LABELS = {
  from_address: "Nadawca",
  subject: "Temat",
  status: "Status",
  source_ref: "Źródło",
}

const EMPTY_DRAFT = {
  source_ref: "fixture://inbound-mail/",
  from_address: "",
  subject: "",
  body_text: "",
}

export function MailIntegrationPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const [partyId, setPartyId] = useState("")
  const [email, setEmail] = useState("")
  const [resolved, setResolved] = useState<Party | null>(null)
  const [draft, setDraft] = useState(EMPTY_DRAFT)

  const parties = useQuery({
    queryKey: ["mail-parties", ctx.organizationId],
    queryFn: fetchParties,
    enabled: ready,
    retry: false,
  })
  const domains = useQuery({
    queryKey: ["mail-domains", partyId],
    queryFn: () => fetchEmailDomains(partyId),
    enabled: ready && partyId !== "",
    retry: false,
  })
  const contacts = useQuery({
    queryKey: ["mail-contacts", partyId],
    queryFn: () => fetchContacts(partyId),
    enabled: ready && partyId !== "",
    retry: false,
  })
  const inbound = useQuery({
    queryKey: ["inbound-messages", ctx.organizationId],
    queryFn: fetchInboundMessages,
    enabled: ready,
    retry: false,
  })
  const lookup = useMutation({
    mutationFn: () => resolvePartyEmail(email),
    onSuccess: (row) => {
      setResolved(row)
      setPartyId(row.id)
    },
    onError: () => {
      setResolved(null)
    },
  })
  const createMutation = useMutation({
    mutationFn: () => createInboundMessage(inboundMessageCreateBody(draft)),
    onSuccess: () => {
      setDraft(EMPTY_DRAFT)
      void queryClient.invalidateQueries({
        queryKey: ["inbound-messages", ctx.organizationId],
      })
    },
  })

  return (
    <div className="flex flex-col gap-4" data-mail-integration="board">
      <CatalogHeading
        title="Poczta"
        subtitle="mail_integration M-32 · znane adresy · inbound_message fixture · nie IMAP"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {parties.isError ? <CatalogError error={parties.error} /> : null}
      {domains.isError ? <CatalogError error={domains.error} /> : null}
      {contacts.isError ? <CatalogError error={contacts.error} /> : null}
      {lookup.isError ? <CatalogError error={lookup.error} /> : null}
      {inbound.isError ? <CatalogError error={inbound.error} /> : null}
      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}

      <section className="space-y-2" data-inbound-message="fixture">
        <h2 className="text-sm font-medium">Wiadomości przychodzące</h2>
        <form
          className="flex flex-col gap-2 rounded-md border border-border bg-card p-3"
          onSubmit={(event) => {
            event.preventDefault()
            if (ready) createMutation.mutate()
          }}
        >
          <Input
            aria-label="source_ref fixture"
            placeholder="fixture://inbound-mail/1"
            value={draft.source_ref}
            onChange={(event) => setDraft({ ...draft, source_ref: event.target.value })}
            required
          />
          <Input
            aria-label="Nadawca wiadomości"
            placeholder="ops@carrier.example"
            value={draft.from_address}
            onChange={(event) => setDraft({ ...draft, from_address: event.target.value })}
            required
          />
          <Input
            aria-label="Temat wiadomości"
            placeholder="RFQ Gdynia"
            value={draft.subject}
            onChange={(event) => setDraft({ ...draft, subject: event.target.value })}
            required
          />
          <textarea
            aria-label="Treść wiadomości"
            className="min-h-24 rounded-md border border-border bg-background px-2 py-1 text-sm"
            value={draft.body_text}
            onChange={(event) => setDraft({ ...draft, body_text: event.target.value })}
            required
          />
          <Button type="submit" disabled={!ready || createMutation.isPending}>
            Zapisz fixture
          </Button>
        </form>
        <CatalogLoadedTable
          loading={inbound.isLoading}
          error={inbound.error}
          data={inbound.data}
          tableKey="inbound_message"
          columns={columns}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Filtruj wiadomości"
        />
      </section>

      <form
        className="flex flex-col gap-2"
        onSubmit={(event) => {
          event.preventDefault()
          lookup.mutate()
        }}
      >
        <label className="flex flex-col gap-1 text-xs">
          resolve_email
          <Input
            aria-label="Adres do resolve_email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </label>
        <Button type="submit" disabled={!ready || lookup.isPending}>
          Sprawdź mail
        </Button>
      </form>
      {resolved ? <p className="text-xs">{resolved.legal_name}</p> : null}

      <label className="flex flex-col gap-1 text-xs">
        party.id
        <select
          aria-label="Kontrahent poczty"
          className="h-8 rounded-md border border-border bg-card px-2 text-sm"
          value={partyId}
          onChange={(event) => setPartyId(event.target.value)}
        >
          <option value="">Wybierz kontrahenta</option>
          {(parties.data ?? []).map((row) => (
            <option key={row.id} value={row.id}>
              {row.legal_name}
            </option>
          ))}
        </select>
      </label>

      <section className="space-y-1">
        <h2 className="text-sm font-medium">Domeny</h2>
        {(domains.data ?? []).map((row) => (
          <p key={row.id} className="font-mono text-xs">
            {row.domain}
          </p>
        ))}
      </section>
      <section className="space-y-1" data-mail-client="mailto">
        <h2 className="text-sm font-medium">Kontakty</h2>
        {(contacts.data ?? []).map((row) =>
          row.email === null ? null : (
            <p key={row.id} className="text-xs">
              {row.name}{" "}
              <a className="underline" href={`mailto:${row.email}`}>
                {row.email}
              </a>
            </p>
          ),
        )}
      </section>
    </div>
  )
}
