import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { createColumnHelper } from "@tanstack/react-table"
import { useEffect, useState } from "react"
import { CatalogHeading } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { comparisonChargeBody, createCharge, type Charge } from "@/lib/charges-api"
import {
  channelQuoteCreateBody,
  createChannelQuote,
  fetchChannelQuotes,
  resolveChannelQuote,
  type ChannelQuote,
} from "@/lib/channel-quotes-api"
import { fetchCommodityCodes } from "@/lib/commodity-codes-api"
import { fetchCustomerRfqs, type CustomerRfq } from "@/lib/customer-rfqs-api"
import { fetchDangerousGoods } from "@/lib/dangerous-goods-api"
import { resolveCreditReview, type CreditReview } from "@/lib/credit-reviews-api"
import { resolveNbpRate, type NbpRate } from "@/lib/nbp-rates-api"
import { fetchParties, type Party } from "@/lib/parties-api"
import { fetchPartyScorecard, type PartyScorecard } from "@/lib/party-scorecards-api"
import {
  createOperatorDecision,
  decideOperatorDecision,
  fetchOperatorDecisions,
  type OperatorDecideStatus,
  type OperatorDecision,
} from "@/lib/operator-decisions-api"
import { DecideStatusButtons } from "@/features/operator-decisions/decide-status-buttons"
import { CarryForwardPanel } from "@/features/quotations/carry-forward-panel"
import { ChecklistRulePanel } from "@/features/quotations/checklist-rule-panel"
import { DispatchRulePanel } from "@/features/quotations/dispatch-rule-panel"
import { IncotermResponsibilityPanel } from "@/features/quotations/incoterm-responsibility-panel"
import { fetchPorts } from "@/lib/ports-api"
import {
  createQuotation,
  createQuotationBatch,
  fetchQuotationDocumentLayout,
  fetchQuotations,
  issueQuotationDocumentNumber,
  negotiateQuotation,
  noteQuotationRisk,
  quotationBatchBody,
  quotationCreateBody,
  quotationCurrencies,
  quotationInquiryTrails,
  quotationAcceptancePending,
  quotationCarrierInquiries,
  quotationLanes,
  quotationResponseComparisons,
  quotationPartyIds,
  quotationSkipsNbpCatalog,
  type Quotation,
  type QuotationLane,
} from "@/lib/quotations-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<Quotation>()

const columns = [
  helper.accessor("charge_code", { header: "Kod opłaty" }),
  helper.accessor("amount", {
    header: "Kwota ze stawki",
    cell: ({ row }) => <Money amount={row.original.amount} currency={row.original.currency} />,
  }),
  helper.accessor("customer_rfq_id", {
    header: "RFQ",
    cell: ({ row }) => (
      <span className="font-mono text-xs">{row.original.customer_rfq_id ?? "—"}</span>
    ),
  }),
  helper.accessor("commodity_code_id", {
    header: "HS/CN",
    cell: ({ row }) => (
      <span className="font-mono text-xs">{row.original.commodity_code_id ?? "—"}</span>
    ),
  }),
  helper.accessor("dangerous_good_id", {
    header: "UN",
    cell: ({ row }) => (
      <span className="font-mono text-xs">{row.original.dangerous_good_id ?? "—"}</span>
    ),
  }),
  helper.accessor("party_id", {
    header: "Kontrahent",
    cell: ({ row }) => <span className="font-mono text-xs">{row.original.party_id ?? "—"}</span>,
  }),
  helper.accessor("origin_port_id", {
    header: "POL",
    cell: ({ row }) => <span className="font-mono text-xs">{row.original.origin_port_id ?? "—"}</span>,
  }),
  helper.accessor("destination_port_id", {
    header: "POD",
    cell: ({ row }) => (
      <span className="font-mono text-xs">{row.original.destination_port_id ?? "—"}</span>
    ),
  }),
  helper.accessor("source_ref", { header: "Pochodzenie" }),
  helper.accessor("rate_line_id", { header: "Stawka" }),
]

const COLUMN_LABELS = {
  charge_code: "Kod opłaty",
  amount: "Kwota ze stawki",
  customer_rfq_id: "RFQ",
  commodity_code_id: "HS/CN",
  dangerous_good_id: "UN",
  party_id: "Kontrahent",
  origin_port_id: "POL",
  destination_port_id: "POD",
  source_ref: "Pochodzenie",
  rate_line_id: "Stawka",
}

function OfferNbpFieldset(args: { currencies: string[]; signedIn: boolean }) {
  const [offerCurrency, setOfferCurrency] = useState("")
  const [offerOnDate, setOfferOnDate] = useState("")
  const [offerNbp, setOfferNbp] = useState<NbpRate | null>(null)
  const [plnSkip, setPlnSkip] = useState(false)

  const nbpLookup = useMutation({
    mutationFn: () => resolveNbpRate(offerCurrency.trim().toUpperCase(), offerOnDate),
    onSuccess: (row) => {
      setOfferNbp(row)
    },
    onError: () => {
      setOfferNbp(null)
    },
  })

  return (
    <fieldset className="flex flex-col gap-2 rounded-md border border-border bg-card p-3">
      <legend className="px-1 text-sm font-medium">Kurs NBP waluty oferty</legend>
      <p className="text-xs text-muted-foreground">
        ISO z wiersza wyceny · resolve katalogu 6.0 · nie przeliczaj amount
      </p>
      {args.currencies.length === 0 ? (
        <p className="text-sm text-muted-foreground">Najpierw wycena — waluta ze stawki.</p>
      ) : (
        <form
          className="flex flex-col gap-2 md:flex-row md:flex-wrap md:items-end"
          onSubmit={(event) => {
            event.preventDefault()
            if (quotationSkipsNbpCatalog(offerCurrency)) {
              setPlnSkip(true)
              setOfferNbp(null)
              return
            }
            setPlnSkip(false)
            nbpLookup.mutate()
          }}
        >
          <label className="flex flex-col gap-1 text-xs">
            quotation.currency
            <select
              aria-label="Waluta oferty"
              className="h-8 rounded-md border border-border bg-card px-2 text-sm"
              value={offerCurrency}
              onChange={(event) => setOfferCurrency(event.target.value)}
              required
            >
              <option value="">Waluta z listy wycen</option>
              {args.currencies.map((iso) => (
                <option key={iso} value={iso}>
                  {iso}
                </option>
              ))}
            </select>
          </label>
          <Input
            aria-label="Dzień kursu oferty"
            type="date"
            value={offerOnDate}
            onChange={(event) => setOfferOnDate(event.target.value)}
            required
          />
          <Button type="submit" disabled={nbpLookup.isPending || !args.signedIn}>
            Pokaż kurs NBP
          </Button>
        </form>
      )}
      {plnSkip ? (
        <p className="text-sm text-muted-foreground">PLN — katalog 6.0 nie trzyma kursu PLN</p>
      ) : null}
      {nbpLookup.isError && !plnSkip ? (
        <p className="text-sm text-destructive">{(nbpLookup.error as Error).message}</p>
      ) : null}
      {offerNbp ? (
        <p className="font-mono text-xs">
          {offerNbp.currency} {offerNbp.mid} {offerNbp.rate_date} {offerNbp.source_ref}
        </p>
      ) : null}
    </fieldset>
  )
}

function OfferRiskPanel(args: { rows: Quotation[]; signedIn: boolean }) {
  const queryClient = useQueryClient()
  const ctx = getTenantContext()
  const partyIds = quotationPartyIds(args.rows)
  const [partyId, setPartyId] = useState("")
  const [quoteId, setQuoteId] = useState("")
  const [onDate, setOnDate] = useState("")
  const [review, setReview] = useState<CreditReview | null>(null)
  const [card, setCard] = useState<PartyScorecard | null>(null)
  const [savedId, setSavedId] = useState<string | null>(null)
  const forParty = args.rows.filter((row) => row.party_id === partyId)

  const reviewLookup = useMutation({
    mutationFn: () => resolveCreditReview(partyId, onDate),
    onSuccess: (row) => {
      setReview(row)
    },
    onError: () => {
      setReview(null)
    },
  })

  const cardLookup = useMutation({
    mutationFn: () => fetchPartyScorecard(partyId),
    onSuccess: (row) => {
      setCard(row)
    },
    onError: () => {
      setCard(null)
    },
  })

  const saveFact = useMutation({
    mutationFn: () => {
      if (review === null || quoteId === "") {
        throw new Error("Wybierz wycenę i pokaż recenzję")
      }
      return noteQuotationRisk(quoteId, review.id)
    },
    onSuccess: (row) => {
      setSavedId(row.noted_credit_review_id)
      void queryClient.invalidateQueries({ queryKey: ["quotations", ctx.organizationId] })
    },
  })

  return (
    <aside className="space-y-2 rounded-md border border-dashed border-border p-3" data-offer-risk="fact">
      <h3 className="text-sm font-medium">Ryzyko kontrahenta oferty</h3>
      <p className="text-xs text-muted-foreground">
        recenzja 14.0 + karta 10.0 · wskazanie faktu · nie scoring
      </p>
      {partyIds.length === 0 ? (
        <p className="text-sm text-muted-foreground">Najpierw wycena z party_id.</p>
      ) : (
        <form
          className="grid gap-2 sm:grid-cols-[1fr_auto_auto]"
          onSubmit={(event) => {
            event.preventDefault()
            reviewLookup.mutate()
            cardLookup.mutate()
          }}
        >
          <label className="flex flex-col gap-1 text-xs">
            quotation.party_id
            <select
              aria-label="Kontrahent oferty"
              className="h-8 rounded-md border border-border bg-card px-2 text-sm"
              value={partyId}
              onChange={(event) => setPartyId(event.target.value)}
              required
            >
              <option value="">Kontrahent z listy wycen</option>
              {partyIds.map((id) => (
                <option key={id} value={id}>
                  {id}
                </option>
              ))}
            </select>
          </label>
          <Input
            aria-label="Dzień recenzji oferty"
            type="date"
            value={onDate}
            onChange={(event) => setOnDate(event.target.value)}
            required
          />
          <Button type="submit" disabled={reviewLookup.isPending || cardLookup.isPending || !args.signedIn}>
            Pokaż fakty ryzyka
          </Button>
        </form>
      )}
      {reviewLookup.isError ? (
        <p className="text-sm text-destructive">{(reviewLookup.error as Error).message}</p>
      ) : null}
      {cardLookup.isError ? (
        <p className="text-sm text-destructive">{(cardLookup.error as Error).message}</p>
      ) : null}
      {review ? (
        <p className="text-xs">
          recenzja {review.decision} {review.review_date} {review.source_ref}
        </p>
      ) : null}
      {card ? (
        <p className="text-xs">
          karta {card.computed_at} {card.source_ref} n={card.sample_size}
        </p>
      ) : null}
      {review !== null && forParty.length > 0 ? (
        <div className="flex flex-wrap items-center gap-2">
          <select
            aria-label="Wycena do faktu ryzyka"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={quoteId}
            onChange={(event) => setQuoteId(event.target.value)}
          >
            <option value="">Wycena</option>
            {forParty.map((row) => (
              <option key={row.id} value={row.id}>
                {row.charge_code} {row.id}
              </option>
            ))}
          </select>
          <Button
            type="button"
            disabled={saveFact.isPending || quoteId === "" || !args.signedIn}
            onClick={() => saveFact.mutate()}
          >
            Zapisz fakt
          </Button>
        </div>
      ) : null}
      {saveFact.isError ? (
        <p className="text-sm text-destructive">{(saveFact.error as Error).message}</p>
      ) : null}
      {savedId !== null ? <p className="text-xs font-mono">fakt {savedId}</p> : null}
    </aside>
  )
}

function OfferNegotiationPanel(args: { lanes: QuotationLane[]; signedIn: boolean }) {
  const queryClient = useQueryClient()
  const ctx = getTenantContext()
  const [quoteId, setQuoteId] = useState("")
  const [onDate, setOnDate] = useState("")
  const [channel, setChannel] = useState<ChannelQuote | null>(null)
  const [savedId, setSavedId] = useState<string | null>(null)
  const selected = args.lanes.find((lane) => lane.id === quoteId)

  const lookup = useMutation({
    mutationFn: () => {
      if (selected === undefined) {
        throw new Error("Wybierz wycenę z POL/POD i kontrahentem")
      }
      return resolveChannelQuote({
        partyId: selected.partyId,
        originPortId: selected.originPortId,
        destinationPortId: selected.destinationPortId,
        onDate,
      })
    },
    onSuccess: (row) => {
      setChannel(row)
    },
    onError: () => {
      setChannel(null)
    },
  })

  const saveResult = useMutation({
    mutationFn: () => {
      if (selected === undefined || channel === null) {
        throw new Error("Najpierw pokaż ofertę kanału")
      }
      return negotiateQuotation(selected.id, channel.id)
    },
    onSuccess: (row) => {
      setSavedId(row.negotiated_channel_quote_id)
      void queryClient.invalidateQueries({ queryKey: ["quotations", ctx.organizationId] })
    },
  })

  return (
    <div className="space-y-2 bg-card p-3 ring-1 ring-border" data-offer-negotiation="result">
      <h3 className="text-sm font-medium">Oferta kanału przy wycenie</h3>
      <p className="text-xs text-muted-foreground">
        channel_quote 13.0 na tej samej lane · wskazanie oferty · nie odejmuj kwot
      </p>
      {args.lanes.length === 0 ? (
        <p className="text-sm text-muted-foreground">Najpierw wycena z party_id, POL i POD.</p>
      ) : (
        <form
          className="flex flex-col gap-2"
          onSubmit={(event) => {
            event.preventDefault()
            lookup.mutate()
          }}
        >
          <label className="flex flex-col gap-1 text-xs">
            quotation.id
            <select
              aria-label="Wycena do porównania z kanałem"
              className="h-8 rounded-md border border-border bg-card px-2 text-sm"
              value={quoteId}
              onChange={(event) => setQuoteId(event.target.value)}
              required
            >
              <option value="">Wycena z lane</option>
              {args.lanes.map((lane) => (
                <option key={lane.id} value={lane.id}>
                  {lane.chargeCode} {lane.id}
                </option>
              ))}
            </select>
          </label>
          <Input
            aria-label="Dzień oferty kanału"
            type="date"
            value={onDate}
            onChange={(event) => setOnDate(event.target.value)}
            required
          />
          <Button type="submit" disabled={lookup.isPending || !args.signedIn}>
            Pokaż ofertę kanału
          </Button>
        </form>
      )}
      {lookup.isError ? (
        <p className="text-sm text-destructive">{(lookup.error as Error).message}</p>
      ) : null}
      {selected ? (
        <p className="text-xs">
          wycena <Money amount={selected.amount} currency={selected.currency} />
        </p>
      ) : null}
      {channel ? (
        <p className="text-xs">
          kanał <Money amount={channel.amount} currency={channel.currency} /> {channel.source_ref}
        </p>
      ) : null}
      {channel !== null && selected !== undefined ? (
        <Button
          type="button"
          disabled={saveResult.isPending || !args.signedIn}
          onClick={() => saveResult.mutate()}
        >
          Zapisz wynik
        </Button>
      ) : null}
      {saveResult.isError ? (
        <p className="text-sm text-destructive">{(saveResult.error as Error).message}</p>
      ) : null}
      {savedId !== null ? (
        <p className="text-xs font-mono">wskazanie {savedId}</p>
      ) : null}
    </div>
  )
}

function printOfferDocument() {
  window.print()
}

function OfferDocumentFacts(args: { selected: Quotation }) {
  const selected = args.selected
  return (
    <dl className="grid gap-1 text-xs">
      <div>
        <dt className="text-muted-foreground">Numer oferty</dt>
        <dd className="font-mono">{selected.document_number ?? "—"}</dd>
      </div>
      <div>
        <dt className="text-muted-foreground">Kod opłaty</dt>
        <dd>{selected.charge_code}</dd>
      </div>
      <div>
        <dt className="text-muted-foreground">Kwota ze stawki</dt>
        <dd>
          <Money amount={selected.amount} currency={selected.currency} />
        </dd>
      </div>
      <div>
        <dt className="text-muted-foreground">party_id</dt>
        <dd className="font-mono">{selected.party_id ?? "—"}</dd>
      </div>
      <div>
        <dt className="text-muted-foreground">origin_port_id</dt>
        <dd className="font-mono">{selected.origin_port_id ?? "—"}</dd>
      </div>
      <div>
        <dt className="text-muted-foreground">destination_port_id</dt>
        <dd className="font-mono">{selected.destination_port_id ?? "—"}</dd>
      </div>
      <div>
        <dt className="text-muted-foreground">source_ref</dt>
        <dd>{selected.source_ref}</dd>
      </div>
    </dl>
  )
}

function OfferDocumentActions(args: {
  quoteId: string
  numbered: string | null
  pending: boolean
  error: string | null
  onIssue: () => void
}) {
  return (
    <div className="flex flex-wrap gap-2">
      <Button
        type="button"
        size="sm"
        disabled={args.quoteId === "" || args.numbered !== null || args.pending}
        onClick={args.onIssue}
      >
        Nadaj numer
      </Button>
      <Button type="button" size="sm" variant="outline" onClick={printOfferDocument}>
        Drukuj
      </Button>
      {args.error ? <p className="text-sm text-destructive">{args.error}</p> : null}
    </div>
  )
}

function OfferDocumentPanel(args: { rows: Quotation[] }) {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [quoteId, setQuoteId] = useState("")
  const selected = args.rows.find((row) => row.id === quoteId)
  const layout = useQuery({
    queryKey: ["quotation-document-layout", ctx.organizationId],
    queryFn: fetchQuotationDocumentLayout,
    enabled: Boolean(ctx.organizationId),
  })
  const issue = useMutation({
    mutationFn: issueQuotationDocumentNumber,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["quotations", ctx.organizationId] })
    },
  })
  const printTemplate = layout.data?.print_template ?? "plain"
  return (
    <article
      className="space-y-2 p-3 outline outline-1 outline-border"
      data-offer-document="preview"
      data-print-template={printTemplate}
    >
      <h3 className="text-sm font-medium">Dokument oferty</h3>
      <p className="text-xs text-muted-foreground">
        fakty z quotation · numer z prefiksu · druk 57.0 · nie PDF
      </p>
      {args.rows.length === 0 ? (
        <p className="text-sm text-muted-foreground">Najpierw wycena — dokument z wiersza.</p>
      ) : (
        <label className="flex flex-col gap-1 text-xs">
          quotation.id
          <select
            aria-label="Wycena do dokumentu"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={quoteId}
            onChange={(event) => setQuoteId(event.target.value)}
          >
            <option value="">Wybierz wycenę</option>
            {args.rows.map((row) => (
              <option key={row.id} value={row.id}>
                {row.document_number ?? row.charge_code} {row.id}
              </option>
            ))}
          </select>
        </label>
      )}
      {selected ? <OfferDocumentFacts selected={selected} /> : null}
      <OfferDocumentActions
        quoteId={quoteId}
        numbered={selected?.document_number ?? null}
        pending={issue.isPending}
        error={issue.isError ? (issue.error as Error).message : null}
        onIssue={() => issue.mutate(quoteId)}
      />
    </article>
  )
}

function OfferInquiryPanel(args: { rows: Quotation[]; parties: Party[] }) {
  const trails = quotationInquiryTrails(args.rows)
  if (trails.length === 0) {
    return null
  }
  const names = new Map(args.parties.map((party) => [party.id, party.legal_name]))
  return (
    <article className="space-y-2 p-3 outline outline-1 outline-border" data-customer-inquiry="trail">
      <h3 className="text-sm font-medium">Zapytania od klientów</h3>
      <p className="text-xs text-muted-foreground">ślad quotation per party · nie RFQ · nie skrzynka</p>
      {trails.map((trail) => (
        <div key={trail.partyId} className="space-y-1">
          <p className="text-xs font-medium">{names.get(trail.partyId) ?? trail.partyId}</p>
          <ul className="space-y-1 text-xs">
            {trail.quotations.map((row) => (
              <li key={row.id}>
                {row.charge_code}{" "}
                <Money amount={row.amount} currency={row.currency} />
              </li>
            ))}
          </ul>
        </div>
      ))}
    </article>
  )
}

function OfferAcceptancePanel(args: {
  rows: Quotation[]
  decisions: OperatorDecision[]
  signedIn: boolean
}) {
  const queryClient = useQueryClient()
  const ctx = getTenantContext()
  const pending = quotationAcceptancePending(args.rows, args.decisions)
  const decideOffer = useMutation({
    mutationFn: async (input: { quotationId: string; status: OperatorDecideStatus }) => {
      const open = args.decisions.find(
        (row) =>
          row.subject_kind === "quotation" &&
          row.subject_id === input.quotationId &&
          row.status === "pending",
      )
      const created =
        open ??
        (await createOperatorDecision({
          subject_kind: "quotation",
          subject_id: input.quotationId,
          source_ref: "tenant:manual",
        }))
      return decideOperatorDecision(created.id, input.status, created.lock_version)
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["operator-decisions", ctx.organizationId] })
    },
  })
  if (pending.length === 0) {
    return null
  }
  return (
    <article className="space-y-2 p-3 outline outline-1 outline-border" data-offer-acceptance="pending">
      <h3 className="text-sm font-medium">Akceptacja oferty</h3>
      <p className="text-xs text-muted-foreground">decyzja S11 · nie HITL extract · nie skrzynka</p>
      <ul className="space-y-1 text-xs">
        {pending.map((row) => (
          <li key={row.id} className="flex flex-wrap items-center gap-2">
            {row.charge_code}{" "}
            <Money amount={row.amount} currency={row.currency} />
            <DecideStatusButtons
              acceptLabel="Przyjmij"
              disabled={decideOffer.isPending || !args.signedIn}
              onDecide={(status) => decideOffer.mutate({ quotationId: row.id, status })}
            />
          </li>
        ))}
      </ul>
      {decideOffer.isError ? (
        <p className="text-sm text-destructive">{(decideOffer.error as Error).message}</p>
      ) : null}
    </article>
  )
}

function OfferCarrierInquiryPanel(args: { lanes: QuotationLane[]; quotes: ChannelQuote[] }) {
  const matched = quotationCarrierInquiries(args.lanes, args.quotes)
  if (matched.length === 0) {
    return null
  }
  return (
    <article className="space-y-2 p-3 outline outline-1 outline-border" data-carrier-inquiry="trail">
      <h3 className="text-sm font-medium">Zapytania do armatorów</h3>
      <p className="text-xs text-muted-foreground">channel_quote na lane wyceny · nie HTTP · nie odejmuj</p>
      <ul className="space-y-1 text-xs">
        {matched.map((quote) => (
          <li key={quote.id}>
            {quote.quote_date} {quote.source_ref}{" "}
            <Money amount={quote.amount} currency={quote.currency} />
          </li>
        ))}
      </ul>
    </article>
  )
}

function OfferManualChannelQuotePanel(args: { lanes: QuotationLane[]; signedIn: boolean }) {
  const queryClient = useQueryClient()
  const first = args.lanes[0]
  const [partyId, setPartyId] = useState("")
  const [originPortId, setOriginPortId] = useState(first?.originPortId ?? "")
  const [destinationPortId, setDestinationPortId] = useState(first?.destinationPortId ?? "")
  const [quoteDate, setQuoteDate] = useState("")
  const [amount, setAmount] = useState("")
  const [currency, setCurrency] = useState("")
  const [transitDays, setTransitDays] = useState("")
  const createQuote = useMutation({
    mutationFn: () =>
      createChannelQuote(
        channelQuoteCreateBody({
          partyId,
          originPortId,
          destinationPortId,
          quoteDate,
          amount,
          currency,
          transitDays,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["channel-quotes"] })
    },
  })
  if (args.lanes.length === 0 || !args.signedIn) {
    return null
  }
  return (
    <article className="space-y-2 p-3 outline outline-1 outline-border" data-channel-quote="from-quote">
      <h3 className="text-sm font-medium">Wpis oferty kanału</h3>
      <p className="text-xs text-muted-foreground">
        POST channel_quote z lane wyceny · nie mutuj kwoty · nie rate_line
      </p>
      <form
        className="grid gap-2 md:grid-cols-2"
        onSubmit={(event) => {
          event.preventDefault()
          createQuote.mutate()
        }}
      >
        <Input
          aria-label="Armator oferty z wyceny"
          placeholder="party_id"
          value={partyId}
          onChange={(event) => setPartyId(event.target.value)}
          required
        />
        <Input
          aria-label="POL oferty z wyceny"
          placeholder="origin_port_id"
          value={originPortId}
          onChange={(event) => setOriginPortId(event.target.value)}
          required
        />
        <Input
          aria-label="POD oferty z wyceny"
          placeholder="destination_port_id"
          value={destinationPortId}
          onChange={(event) => setDestinationPortId(event.target.value)}
          required
        />
        <Input
          aria-label="Dzień oferty z wyceny"
          type="date"
          value={quoteDate}
          onChange={(event) => setQuoteDate(event.target.value)}
          required
        />
        <Input
          aria-label="Kwota oferty z wyceny"
          placeholder="kwota kupna"
          inputMode="decimal"
          value={amount}
          onChange={(event) => setAmount(event.target.value)}
          required
        />
        <Input
          aria-label="Waluta oferty z wyceny"
          placeholder="USD"
          maxLength={3}
          value={currency}
          onChange={(event) => setCurrency(event.target.value)}
          required
        />
        <Input
          aria-label="TT oferty z wyceny"
          placeholder="dni"
          inputMode="numeric"
          value={transitDays}
          onChange={(event) => setTransitDays(event.target.value)}
        />
        <Button type="submit" disabled={createQuote.isPending}>
          Zapisz ofertę kanału
        </Button>
      </form>
      {createQuote.isError ? <p className="text-xs text-destructive">{String(createQuote.error)}</p> : null}
    </article>
  )
}

function OfferResponseComparisonPanel(args: { lanes: QuotationLane[]; quotes: ChannelQuote[] }) {
  const rows = quotationResponseComparisons(args.lanes, args.quotes)
  const [laneId, setLaneId] = useState("")
  const [quoteId, setQuoteId] = useState("")
  const [saved, setSaved] = useState<Charge | null>(null)
  const saveMargin = useMutation({
    mutationFn: () => {
      const lane = args.lanes.find((row) => row.id === laneId)
      const quote = args.quotes.find((row) => row.id === quoteId)
      if (lane === undefined || quote === undefined) {
        return Promise.reject(new Error("Wybierz wycenę i ofertę kanału"))
      }
      return createCharge(comparisonChargeBody(lane, quote))
    },
    onSuccess: setSaved,
  })
  if (rows.length === 0) {
    return null
  }
  return (
    <article className="space-y-2 p-3 outline outline-1 outline-border" data-response-comparison="lanes">
      <h3 className="text-sm font-medium">Porównanie odpowiedzi</h3>
      <p className="text-xs text-muted-foreground">
        wycena i channel_quote na POL/POD · marża w charge · nie odejmuj
      </p>
      {rows.map((row) => (
        <div key={`${row.originPortId}:${row.destinationPortId}`} className="space-y-1">
          {row.quotations.map((lane) => (
            <p key={lane.id} className="text-xs">
              wycena {lane.chargeCode} <Money amount={lane.amount} currency={lane.currency} />
            </p>
          ))}
          {row.quotes.map((quote) => (
            <p key={quote.id} className="text-xs">
              kanał {quote.quote_date} {quote.source_ref}{" "}
              <Money amount={quote.amount} currency={quote.currency} />
              {quote.transit_days === null ? null : ` · ${String(quote.transit_days)} dni`}
              {quote.is_cheapest ? " · najtańsza" : ""}
              {quote.is_fastest_tt ? " · najszybszy TT" : ""}
            </p>
          ))}
        </div>
      ))}
      <form
        className="flex flex-col gap-2 lg:flex-row"
        onSubmit={(event) => {
          event.preventDefault()
          if (laneId !== "" && quoteId !== "") saveMargin.mutate()
        }}
      >
        <select
          aria-label="Wycena do opłaty"
          className="h-8 rounded-md border border-border bg-card px-2 text-sm"
          value={laneId}
          onChange={(event) => setLaneId(event.target.value)}
        >
          <option value="">Wycena</option>
          {args.lanes.map((lane) => (
            <option key={lane.id} value={lane.id}>
              {lane.chargeCode} {lane.amount} {lane.currency}
            </option>
          ))}
        </select>
        <select
          aria-label="Oferta kanału do opłaty"
          className="h-8 rounded-md border border-border bg-card px-2 text-sm"
          value={quoteId}
          onChange={(event) => setQuoteId(event.target.value)}
        >
          <option value="">Kanał</option>
          {args.quotes.map((quote) => (
            <option key={quote.id} value={quote.id}>
              {quote.source_ref} {quote.amount} {quote.currency}
            </option>
          ))}
        </select>
        <Button type="submit" disabled={saveMargin.isPending || laneId === "" || quoteId === ""}>
          Zapisz marżę
        </Button>
      </form>
      {saveMargin.isError ? <p className="text-xs text-destructive">{String(saveMargin.error)}</p> : null}
      {saved === null ? null : (
        <p className="text-xs">
          marża <Money amount={saved.margin_amount} currency={saved.margin_currency} />
        </p>
      )}
    </article>
  )
}

function initialSearchRfq(): string {
  if (typeof window === "undefined") {
    return ""
  }
  return new URLSearchParams(window.location.search).get("rfq") ?? ""
}

function rfqPartyId(rows: readonly CustomerRfq[], rfqId: string): string {
  const found = rows.find((row) => row.id === rfqId)
  return found?.party_id ?? ""
}

function rfqCommodityCodeId(rows: readonly CustomerRfq[], rfqId: string): string {
  const found = rows.find((row) => row.id === rfqId)
  return found?.commodity_code_id ?? ""
}

function rfqDangerousGoodId(rows: readonly CustomerRfq[], rfqId: string): string {
  const found = rows.find((row) => row.id === rfqId)
  return found?.dangerous_good_id ?? ""
}

export function QuotationCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [chargeCode, setChargeCode] = useState("")
  const [partyId, setPartyId] = useState("")
  const [rfqId, setRfqId] = useState(initialSearchRfq)
  const [commodityCodeId, setCommodityCodeId] = useState("")
  const [dangerousGoodId, setDangerousGoodId] = useState("")
  const [originPortId, setOriginPortId] = useState("")
  const [destinationPortId, setDestinationPortId] = useState("")
  const [filterPartyId, setFilterPartyId] = useState("")
  const [filterOriginPortId, setFilterOriginPortId] = useState("")
  const [filterDestinationPortId, setFilterDestinationPortId] = useState("")
  const [filterRfqId, setFilterRfqId] = useState("")
  const [batchCodes, setBatchCodes] = useState("")
  const [incoterm, setIncoterm] = useState("")
  const [incotermsVersion, setIncotermsVersion] = useState("")
  const [tradeSide, setTradeSide] = useState("")
  const [namedPlace, setNamedPlace] = useState("")
  const signedIn = Boolean(ctx.organizationId && ctx.userId)

  const partiesQuery = useQuery({
    queryKey: ["parties-picker", ctx.organizationId],
    queryFn: fetchParties,
    enabled: signedIn,
    retry: false,
  })

  const portsQuery = useQuery({
    queryKey: ["ports-picker", ctx.organizationId],
    queryFn: () => fetchPorts(""),
    enabled: signedIn,
    retry: false,
  })

  const rfqsQuery = useQuery({
    queryKey: ["customer-rfqs", ctx.organizationId],
    queryFn: fetchCustomerRfqs,
    enabled: signedIn,
    retry: false,
  })

  const commodityCodesQuery = useQuery({
    queryKey: ["commodity-codes", ctx.organizationId],
    queryFn: fetchCommodityCodes,
    enabled: signedIn,
    retry: false,
  })

  const dangerousGoodsQuery = useQuery({
    queryKey: ["dangerous-goods", ctx.organizationId],
    queryFn: fetchDangerousGoods,
    enabled: signedIn,
    retry: false,
  })

  useEffect(() => {
    if (rfqId === "") {
      return
    }
    const partyFromRfq = rfqPartyId(rfqsQuery.data ?? [], rfqId)
    if (partyFromRfq !== "") {
      setPartyId(partyFromRfq)
    }
    const hsFromRfq = rfqCommodityCodeId(rfqsQuery.data ?? [], rfqId)
    if (hsFromRfq !== "") {
      setCommodityCodeId(hsFromRfq)
    }
    const unFromRfq = rfqDangerousGoodId(rfqsQuery.data ?? [], rfqId)
    if (unFromRfq !== "") {
      setDangerousGoodId(unFromRfq)
    }
  }, [rfqId, rfqsQuery.data])

  const channelQuotesQuery = useQuery({
    queryKey: ["channel-quotes", ctx.organizationId],
    queryFn: fetchChannelQuotes,
    enabled: signedIn,
    retry: false,
  })

  const decisionsQuery = useQuery({
    queryKey: ["operator-decisions", ctx.organizationId],
    queryFn: fetchOperatorDecisions,
    enabled: signedIn,
    retry: false,
  })

  const query = useQuery({
    queryKey: [
      "quotations",
      ctx.organizationId,
      filterPartyId,
      filterOriginPortId,
      filterDestinationPortId,
      filterRfqId,
    ],
    queryFn: () =>
      fetchQuotations({
        partyId: filterPartyId,
        originPortId: filterOriginPortId,
        destinationPortId: filterDestinationPortId,
        customerRfqId: filterRfqId,
      }),
    enabled: signedIn,
    retry: false,
  })

  const quoteMutation = useMutation({
    mutationFn: () =>
      createQuotation(
        quotationCreateBody({
          chargeCode,
          originPortId,
          destinationPortId,
          partyId,
          customerRfqId: rfqId,
          commodityCodeId,
          dangerousGoodId,
          incoterm,
          incotermsVersion,
          tradeSide,
          namedPlace,
        }),
      ),
    onSuccess: () => {
      setChargeCode("")
      void queryClient.invalidateQueries({ queryKey: ["quotations", ctx.organizationId] })
    },
  })

  const batchMutation = useMutation({
    mutationFn: () =>
      createQuotationBatch(
        quotationBatchBody({
          chargeCodesText: batchCodes,
          originPortId,
          destinationPortId,
          partyId,
          customerRfqId: rfqId,
          commodityCodeId,
          dangerousGoodId,
          incoterm,
          incotermsVersion,
          tradeSide,
          namedPlace,
        }),
      ),
    onSuccess: () => {
      setBatchCodes("")
      void queryClient.invalidateQueries({ queryKey: ["quotations", ctx.organizationId] })
    },
  })

  const parties = partiesQuery.data ?? []
  const ports = portsQuery.data ?? []
  const rfqs = rfqsQuery.data ?? []
  const commodityCodes = commodityCodesQuery.data ?? []
  const dangerousGoods = dangerousGoodsQuery.data ?? []
  const selectedRfqParty = rfqPartyId(rfqs, rfqId)
  const rfqMissingParty = rfqId !== "" && selectedRfqParty === ""

  return (
    <section className="space-y-3">
      <CatalogHeading
        title="Wyceny"
        subtitle="quotation M-21 · kwota z bieżącego rate_line w SQL · wsad kodów na tej samej lane · nie licz w formularzu"
      />

      {signedIn ? null : (
        <p className="text-sm">
          Najpierw ustaw tenant na stronie <Link className="underline" to="/session">Sesja</Link>.
        </p>
      )}

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          quoteMutation.mutate()
        }}
      >
        <Input
          aria-label="Kod opłaty"
          placeholder="THC"
          value={chargeCode}
          onChange={(event) => setChargeCode(event.target.value)}
          required
        />
        <label className="flex flex-col gap-1 text-xs">
          customer_rfq_id
          <select
            aria-label="Zapytanie ofertowe"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={rfqId}
            onChange={(event) => {
              const next = event.target.value
              setRfqId(next)
              const partyFromRfq = rfqPartyId(rfqs, next)
              if (partyFromRfq !== "") {
                setPartyId(partyFromRfq)
              }
            }}
          >
            <option value="">Bez RFQ</option>
            {rfqs.map((row) => (
              <option key={row.id} value={row.id}>
                {row.id}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          commodity_code_id
          <select
            aria-label="Kod towarowy"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={commodityCodeId}
            onChange={(event) => setCommodityCodeId(event.target.value)}
          >
            <option value="">Bez HS/CN</option>
            {commodityCodes.map((row) => (
              <option key={row.id} value={row.id}>
                {row.code} {row.name}
              </option>
            ))}
          </select>
        </label>
        <fieldset data-quote-un="picker" className="flex flex-col gap-1 text-xs">
          <legend>dangerous_good_id</legend>
          <select
            aria-label="Towar niebezpieczny"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={dangerousGoodId}
            onChange={(event) => setDangerousGoodId(event.target.value)}
          >
            <option value="">Bez UN</option>
            {dangerousGoods.map((row) => (
              <option key={row.id} value={row.id}>
                {row.un_number} {row.name}
              </option>
            ))}
          </select>
        </fieldset>
        <label className="flex flex-col gap-1 text-xs">
          party_id
          <select
            aria-label="Kontrahent"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={partyId}
            onChange={(event) => setPartyId(event.target.value)}
            required
            disabled={selectedRfqParty !== ""}
          >
            <option value="">Kontrahent</option>
            {parties.map((party) => (
              <option key={party.id} value={party.id}>
                {party.legal_name}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          origin_port_id
          <select
            aria-label="Port załadunku"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={originPortId}
            onChange={(event) => setOriginPortId(event.target.value)}
            required
          >
            <option value="">POL</option>
            {ports.map((port) => (
              <option key={port.id} value={port.id}>
                {port.unlocode} {port.name}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          destination_port_id
          <select
            aria-label="Port wyładunku"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={destinationPortId}
            onChange={(event) => setDestinationPortId(event.target.value)}
            required
          >
            <option value="">POD</option>
            {ports.map((port) => (
              <option key={port.id} value={port.id}>
                {port.unlocode} {port.name}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs" data-quote-incoterm="picker">
          incoterm
          <select
            aria-label="Incoterm"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={incoterm}
            onChange={(event) => setIncoterm(event.target.value)}
          >
            <option value="">Bez Incoterms</option>
            {["EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"].map(
              (code) => (
                <option key={code} value={code}>
                  {code}
                </option>
              ),
            )}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          incoterms_version
          <select
            aria-label="Wersja Incoterms"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={incotermsVersion}
            onChange={(event) => setIncotermsVersion(event.target.value)}
          >
            <option value="">Wersja</option>
            <option value="2020">2020</option>
            <option value="2010">2010</option>
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          trade_side
          <select
            aria-label="Strona handlu"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={tradeSide}
            onChange={(event) => setTradeSide(event.target.value)}
          >
            <option value="">Strona</option>
            <option value="import">import</option>
            <option value="export">export</option>
          </select>
        </label>
        <Input
          aria-label="Miejsce nazwane"
          placeholder="named_place"
          value={namedPlace}
          onChange={(event) => setNamedPlace(event.target.value)}
        />
        <Button type="submit" disabled={quoteMutation.isPending || !signedIn || rfqMissingParty}>
          Wycen z bieżącej stawki
        </Button>
        <textarea
          aria-label="Kody wsadowe"
          className="min-h-16 w-full rounded-md border border-border bg-card px-2 py-1 text-sm md:w-40"
          placeholder={"THC\nBAF"}
          value={batchCodes}
          onChange={(event) => setBatchCodes(event.target.value)}
        />
        <Button
          type="button"
          disabled={batchMutation.isPending || !signedIn || rfqMissingParty}
          onClick={() => batchMutation.mutate()}
        >
          Wycen wsadowo
        </Button>
      </form>

      <div className="flex flex-col gap-2 md:flex-row md:flex-wrap">
        <label className="flex flex-col gap-1 text-xs">
          filtr customer_rfq_id
          <select
            aria-label="Filtr zapytania ofertowego"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={filterRfqId}
            onChange={(event) => setFilterRfqId(event.target.value)}
          >
            <option value="">Wszystkie RFQ</option>
            {rfqs.map((row) => (
              <option key={row.id} value={row.id}>
                {row.id}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          filtr party_id
          <select
            aria-label="Filtr kontrahenta"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={filterPartyId}
            onChange={(event) => setFilterPartyId(event.target.value)}
          >
            <option value="">Wszyscy kontrahenci</option>
            {parties.map((party) => (
              <option key={party.id} value={party.id}>
                {party.legal_name}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          filtr origin_port_id
          <select
            aria-label="Filtr POL"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={filterOriginPortId}
            onChange={(event) => setFilterOriginPortId(event.target.value)}
          >
            <option value="">Wszystkie POL</option>
            {ports.map((port) => (
              <option key={port.id} value={port.id}>
                {port.unlocode} {port.name}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          filtr destination_port_id
          <select
            aria-label="Filtr POD"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={filterDestinationPortId}
            onChange={(event) => setFilterDestinationPortId(event.target.value)}
          >
            <option value="">Wszystkie POD</option>
            {ports.map((port) => (
              <option key={port.id} value={port.id}>
                {port.unlocode} {port.name}
              </option>
            ))}
          </select>
        </label>
      </div>

      {quoteMutation.isError ? (
        <p className="text-sm text-destructive">{(quoteMutation.error as Error).message}</p>
      ) : null}
      {batchMutation.isError ? (
        <p className="text-sm text-destructive">{(batchMutation.error as Error).message}</p>
      ) : null}

      {query.data ? (
        <>
          <OfferNbpFieldset currencies={quotationCurrencies(query.data)} signedIn={signedIn} />
          <OfferRiskPanel rows={query.data} signedIn={signedIn} />
          <OfferNegotiationPanel lanes={quotationLanes(query.data)} signedIn={signedIn} />
          <OfferDocumentPanel rows={query.data} />
          <OfferInquiryPanel rows={query.data} parties={parties} />
          <OfferAcceptancePanel
            rows={query.data}
            decisions={decisionsQuery.data ?? []}
            signedIn={signedIn}
          />
          <OfferCarrierInquiryPanel
            lanes={quotationLanes(query.data)}
            quotes={channelQuotesQuery.data ?? []}
          />
          <OfferManualChannelQuotePanel
            lanes={quotationLanes(query.data)}
            signedIn={signedIn}
          />
          <OfferResponseComparisonPanel
            lanes={quotationLanes(query.data)}
            quotes={channelQuotesQuery.data ?? []}
          />
          <CarryForwardPanel rows={query.data} signedIn={signedIn} />
          <ChecklistRulePanel signedIn={signedIn} />
          <IncotermResponsibilityPanel signedIn={signedIn} />
          <DispatchRulePanel signedIn={signedIn} />
        </>
      ) : null}

      {query.isPending ? <p className="text-sm text-muted-foreground">Pobieranie wycen…</p> : null}
      {query.isError ? <p className="text-sm text-destructive">{(query.error as Error).message}</p> : null}
      {query.data ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.quotations.tableKey}
          columns={columns}
          data={query.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Szukaj wyceny…"
        />
      ) : null}
    </section>
  )
}
