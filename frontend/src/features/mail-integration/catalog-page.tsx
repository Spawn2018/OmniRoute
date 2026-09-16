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
import { fetchCommodityCodes } from "@/lib/commodity-codes-api"
import {
  createCustomerRfq,
  fetchCustomerRfqs,
  patchCustomerRfqCommodity,
  patchCustomerRfqDangerous,
} from "@/lib/customer-rfqs-api"
import { fetchDangerousGoods } from "@/lib/dangerous-goods-api"
import {
  createInboundMessage,
  extractInboundMessage,
  fetchInboundMessages,
  inboundMessageCreateBody,
  ingestGraphInboundMessage,
  ingestMailboxInboundMessage,
  resolveInboundMessageEmail,
  type InboundMessage,
} from "@/lib/inbound-messages-api"
import {
  fetchContacts,
  fetchEmailDomains,
  fetchParties,
  resolvePartyEmail,
  type Party,
} from "@/lib/parties-api"
import {
  DEFAULT_MAIL_GROUP_BY,
  groupInboundMessages,
  mailGroupByOrDefault,
  type MailGroupBy,
} from "@/lib/mail-groups"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<InboundMessage>()
const columns = [
  helper.accessor("from_address", {
    header: "Nadawca",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  helper.accessor("subject", { header: "Temat" }),
  helper.accessor("status", { header: "Status" }),
  helper.accessor("party_id", {
    header: "party_id",
    cell: (info) => info.getValue() ?? "—",
  }),
  helper.accessor("source_ref", { header: "Źródło" }),
  helper.accessor("external_id", {
    header: "external_id",
    cell: (info) => info.getValue() ?? "—",
  }),
  helper.accessor("rfc822_message_id", {
    header: "Message-ID",
    cell: (info) => info.getValue() ?? "—",
  }),
  helper.accessor("in_reply_to", {
    header: "In-Reply-To",
    cell: (info) => info.getValue() ?? "—",
  }),
]
const COLUMN_LABELS = {
  from_address: "Nadawca",
  subject: "Temat",
  status: "Status",
  party_id: "party_id",
  source_ref: "Źródło",
  external_id: "external_id",
  rfc822_message_id: "Message-ID",
  in_reply_to: "In-Reply-To",
}

const EMPTY_DRAFT = {
  source_ref: "fixture://inbound-mail/",
  from_address: "",
  subject: "",
  body_text: "",
  rfc822_message_id: "",
  in_reply_to: "",
}

export function MailIntegrationPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const [partyId, setPartyId] = useState("")
  const [email, setEmail] = useState("")
  const [resolved, setResolved] = useState<Party | null>(null)
  const [draft, setDraft] = useState(EMPTY_DRAFT)
  const [graphDraft, setGraphDraft] = useState({
    external_id: "",
    source_ref: "graph://inbox/",
    from_address: "",
    subject: "",
    body_text: "",
  })
  const [mailboxDraft, setMailboxDraft] = useState({
    external_id: "",
    source_ref: "imap://inbox/",
    from_address: "",
    subject: "",
    body_text: "",
  })
  const [hsCodeId, setHsCodeId] = useState("")
  const [unCodeId, setUnCodeId] = useState("")
  const [groupBy, setGroupBy] = useState<MailGroupBy>(DEFAULT_MAIL_GROUP_BY)

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
  const rfqs = useQuery({
    queryKey: ["customer-rfqs", ctx.organizationId],
    queryFn: fetchCustomerRfqs,
    enabled: ready,
    retry: false,
  })
  const commodityCodes = useQuery({
    queryKey: ["commodity-codes", ctx.organizationId],
    queryFn: fetchCommodityCodes,
    enabled: ready,
    retry: false,
  })
  const dangerousGoods = useQuery({
    queryKey: ["dangerous-goods", ctx.organizationId],
    queryFn: fetchDangerousGoods,
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
  const ingestGraph = useMutation({
    mutationFn: () => ingestGraphInboundMessage(graphDraft),
    onSuccess: () => {
      setGraphDraft({
        external_id: "",
        source_ref: "graph://inbox/",
        from_address: "",
        subject: "",
        body_text: "",
      })
      void queryClient.invalidateQueries({
        queryKey: ["inbound-messages", ctx.organizationId],
      })
    },
  })
  const ingestMailbox = useMutation({
    mutationFn: () => ingestMailboxInboundMessage(mailboxDraft),
    onSuccess: () => {
      setMailboxDraft({
        external_id: "",
        source_ref: "imap://inbox/",
        from_address: "",
        subject: "",
        body_text: "",
      })
      void queryClient.invalidateQueries({
        queryKey: ["inbound-messages", ctx.organizationId],
      })
    },
  })
  const extractDraft = useMutation({
    mutationFn: extractInboundMessage,
  })
  const resolveSender = useMutation({
    mutationFn: resolveInboundMessageEmail,
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["inbound-messages", ctx.organizationId],
      })
    },
  })
  const createRfq = useMutation({
    mutationFn: createCustomerRfq,
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["customer-rfqs", ctx.organizationId],
      })
    },
  })
  const attachHs = useMutation({
    mutationFn: (rfqId: string) => patchCustomerRfqCommodity(rfqId, hsCodeId),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["customer-rfqs", ctx.organizationId],
      })
    },
  })
  const attachUn = useMutation({
    mutationFn: (rfqId: string) => patchCustomerRfqDangerous(rfqId, unCodeId),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["customer-rfqs", ctx.organizationId],
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
      {resolveSender.isError ? <CatalogError error={resolveSender.error} /> : null}
      {extractDraft.isError ? <CatalogError error={extractDraft.error} /> : null}
      {rfqs.isError ? <CatalogError error={rfqs.error} /> : null}
      {createRfq.isError ? <CatalogError error={createRfq.error} /> : null}
      {commodityCodes.isError ? <CatalogError error={commodityCodes.error} /> : null}
      {dangerousGoods.isError ? <CatalogError error={dangerousGoods.error} /> : null}
      {attachHs.isError ? <CatalogError error={attachHs.error} /> : null}
      {attachUn.isError ? <CatalogError error={attachUn.error} /> : null}

      <section className="space-y-2" data-inbound-message="fixture">
        <h2 className="text-sm font-medium">Wiadomości przychodzące</h2>
        <label className="flex flex-col gap-1 text-xs">
          group_by
          <select
            aria-label="Grupowanie wiadomości"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={groupBy}
            onChange={(event) => setGroupBy(mailGroupByOrDefault(event.target.value))}
          >
            <option value="party">party</option>
            <option value="country">country</option>
            <option value="status">status</option>
            <option value="thread">thread</option>
          </select>
        </label>
        <ul className="text-xs" data-mail="groups">
          {groupInboundMessages(inbound.data ?? [], parties.data ?? [], groupBy).map((group) => (
            <li key={group.key}>
              {group.key} · {group.rows.length}
            </li>
          ))}
        </ul>
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
          <Input
            aria-label="Message-ID"
            placeholder="<id@example.com>"
            value={draft.rfc822_message_id}
            onChange={(event) =>
              setDraft({ ...draft, rfc822_message_id: event.target.value })
            }
          />
          <Input
            aria-label="In-Reply-To"
            placeholder="<parent@example.com>"
            value={draft.in_reply_to}
            onChange={(event) => setDraft({ ...draft, in_reply_to: event.target.value })}
          />
          <Button type="submit" disabled={!ready || createMutation.isPending}>
            Zapisz fixture
          </Button>
        </form>
        <form
          className="grid gap-2 rounded-md border border-border bg-card p-3"
          data-inbound-message="graph-ingest"
          onSubmit={(event) => {
            event.preventDefault()
            if (ready) ingestGraph.mutate()
          }}
        >
          <Input
            aria-label="Identyfikator Graph"
            placeholder="external_id"
            value={graphDraft.external_id}
            onChange={(event) =>
              setGraphDraft({ ...graphDraft, external_id: event.target.value })
            }
            required
          />
          <Input
            aria-label="Źródło Graph"
            placeholder="graph://inbox/1"
            value={graphDraft.source_ref}
            onChange={(event) =>
              setGraphDraft({ ...graphDraft, source_ref: event.target.value })
            }
            required
          />
          <Input
            aria-label="Nadawca Graph"
            placeholder="ops@carrier.example"
            value={graphDraft.from_address}
            onChange={(event) =>
              setGraphDraft({ ...graphDraft, from_address: event.target.value })
            }
            required
          />
          <Input
            aria-label="Temat Graph"
            placeholder="RFQ"
            value={graphDraft.subject}
            onChange={(event) =>
              setGraphDraft({ ...graphDraft, subject: event.target.value })
            }
            required
          />
          <textarea
            aria-label="Treść Graph"
            className="min-h-24 rounded-md border border-border bg-background px-2 py-1 text-sm"
            value={graphDraft.body_text}
            onChange={(event) =>
              setGraphDraft({ ...graphDraft, body_text: event.target.value })
            }
            required
          />
          <Button type="submit" disabled={!ready || ingestGraph.isPending}>
            Ingest Graph
          </Button>
        </form>
        <form
          className="grid gap-2 rounded-md border border-border bg-card p-3"
          data-inbound-message="mailbox-ingest"
          onSubmit={(event) => {
            event.preventDefault()
            if (ready) ingestMailbox.mutate()
          }}
        >
          <Input
            aria-label="Identyfikator skrzynki"
            placeholder="external_id"
            value={mailboxDraft.external_id}
            onChange={(event) =>
              setMailboxDraft({ ...mailboxDraft, external_id: event.target.value })
            }
            required
          />
          <Input
            aria-label="Źródło skrzynki"
            placeholder="imap://inbox/1"
            value={mailboxDraft.source_ref}
            onChange={(event) =>
              setMailboxDraft({ ...mailboxDraft, source_ref: event.target.value })
            }
            required
          />
          <Input
            aria-label="Nadawca skrzynki"
            placeholder="ops@carrier.example"
            value={mailboxDraft.from_address}
            onChange={(event) =>
              setMailboxDraft({ ...mailboxDraft, from_address: event.target.value })
            }
            required
          />
          <Input
            aria-label="Temat skrzynki"
            placeholder="RFQ"
            value={mailboxDraft.subject}
            onChange={(event) =>
              setMailboxDraft({ ...mailboxDraft, subject: event.target.value })
            }
            required
          />
          <textarea
            aria-label="Treść skrzynki"
            className="min-h-24 rounded-md border border-border bg-background px-2 py-1 text-sm"
            value={mailboxDraft.body_text}
            onChange={(event) =>
              setMailboxDraft({ ...mailboxDraft, body_text: event.target.value })
            }
            required
          />
          <Button type="submit" disabled={!ready || ingestMailbox.isPending}>
            Ingest skrzynka
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
        {(inbound.data ?? [])
          .filter((row) => row.party_id === null)
          .map((row) => (
            <Button
              key={row.id}
              type="button"
              variant="outline"
              disabled={!ready || resolveSender.isPending}
              onClick={() => resolveSender.mutate(row.id)}
            >
              Dopasuj nadawcę {row.from_address}
            </Button>
          ))}
        {(inbound.data ?? []).map((row) => (
          <Button
            key={`extract-${row.id}`}
            type="button"
            variant="outline"
            disabled={!ready || extractDraft.isPending}
            onClick={() => extractDraft.mutate(row.id)}
          >
            Extract HITL {row.subject}
          </Button>
        ))}
        {(inbound.data ?? [])
          .filter(
            (row) =>
              !(rfqs.data ?? []).some((rfq) => rfq.inbound_message_id === row.id),
          )
          .map((row) => (
            <Button
              key={`rfq-${row.id}`}
              type="button"
              variant="outline"
              disabled={!ready || createRfq.isPending}
              onClick={() => createRfq.mutate(row.id)}
            >
              Utwórz RFQ {row.subject}
            </Button>
          ))}
        <label className="flex flex-col gap-1 text-xs">
          commodity_code_id
          <select
            aria-label="Kod towarowy RFQ"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={hsCodeId}
            onChange={(event) => setHsCodeId(event.target.value)}
          >
            <option value="">Bez HS/CN</option>
            {(commodityCodes.data ?? []).map((row) => (
              <option key={row.id} value={row.id}>
                {row.code} {row.name}
              </option>
            ))}
          </select>
        </label>
        <fieldset data-customer-rfq="un" className="flex flex-col gap-1 text-xs">
          <legend>numer UN</legend>
          <select
            aria-label="Towar niebezpieczny RFQ"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={unCodeId}
            onChange={(event) => setUnCodeId(event.target.value)}
          >
            <option value="">Bez UN</option>
            {(dangerousGoods.data ?? []).map((row) => (
              <option key={row.id} value={row.id}>
                {row.un_number} {row.name}
              </option>
            ))}
          </select>
        </fieldset>
        <ul data-customer-rfq="list" className="text-xs">
          {(rfqs.data ?? []).map((row) => (
            <li key={row.id}>
              RFQ {row.id} · wiadomość {row.inbound_message_id} · HS{" "}
              {row.commodity_code_id ?? "—"} · UN {row.dangerous_good_id ?? "—"}{" "}
              <Button
                type="button"
                variant="outline"
                disabled={!ready || hsCodeId === "" || attachHs.isPending}
                onClick={() => attachHs.mutate(row.id)}
              >
                Podpnij HS
              </Button>{" "}
              <Button
                type="button"
                variant="outline"
                disabled={!ready || unCodeId === "" || attachUn.isPending}
                onClick={() => attachUn.mutate(row.id)}
              >
                Podpnij UN
              </Button>{" "}
              <a className="underline" href={`/quotations?rfq=${row.id}`}>
                Wycena
              </a>
            </li>
          ))}
        </ul>
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
