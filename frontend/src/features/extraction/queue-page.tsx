import { Link } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useEffect, useState } from "react"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { HitlReviewSplit } from "@/features/extraction/hitl-review-split"
import { track } from "@/lib/analytics"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { subscribeOperatorAction } from "@/lib/operator-actions"
import {
  acceptExtractionDraft,
  createExtractionDraft,
  extractionCreateBody,
  fetchExtractionDrafts,
  patchExtractionCandidates,
  rejectExtractionDraft,
  undoExtractionDraft,
  type ExtractionCandidate,
  type ExtractionDraft,
} from "@/lib/extractions-api"
import { getTenantContext } from "@/lib/tenant"

const columnHelper = createColumnHelper<ExtractionDraft>()

const COLUMN_LABELS = {
  source_ref: "Źródło",
  status: "Status",
  draft_kind: "Rodzaj",
  parser: "Parser",
  candidates: "Kandydaci",
  unparsed: "Nierozpoznane",
  actions: "Akcje",
}

export function ExtractionQueuePage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [sourceRef, setSourceRef] = useState("tariff://demo")
  const [inputText, setInputText] = useState("THC 125.50 EUR\nweekend note\nBAF 12 USD")
  const [documentBase64, setDocumentBase64] = useState<string | null>(null)
  const [fileName, setFileName] = useState<string | null>(null)
  const [selectedDraftId, setSelectedDraftId] = useState<string | null>(null)
  const [draftKind, setDraftKind] = useState("rate_line")
  const [quotePartyId, setQuotePartyId] = useState("")
  const [quoteOrigin, setQuoteOrigin] = useState("")
  const [quoteDest, setQuoteDest] = useState("")
  const [quoteDate, setQuoteDate] = useState("2026-09-08")
  const [quoteAmount, setQuoteAmount] = useState("")
  const [quoteCurrency, setQuoteCurrency] = useState("USD")
  const [rfpTenderId, setRfpTenderId] = useState("")
  const [rfpIntakeCode, setRfpIntakeCode] = useState("scope")
  const [extractPath, setExtractPath] = useState("text")
  const [sheetIndex, setSheetIndex] = useState("0")
  const [sheetName, setSheetName] = useState("")

  const query = useQuery({
    queryKey: ["extractions", "pending", ctx.organizationId],
    queryFn: () => fetchExtractionDrafts("pending"),
    enabled: Boolean(ctx.organizationId && ctx.userId),
    retry: false,
  })

  const invalidate = () =>
    void queryClient.invalidateQueries({ queryKey: ["extractions", "pending", ctx.organizationId] })

  const createMutation = useMutation({
    mutationFn: () =>
      createExtractionDraft(
        extractionCreateBody({
          sourceRef,
          inputText,
          documentBase64,
          draftKind,
          extractPath,
          sheetIndex: (() => {
            if (sheetName.trim() !== "") {
              return undefined
            }
            const parsed = Number.parseInt(sheetIndex, 10)
            return Number.isFinite(parsed) && parsed >= 0 ? parsed : 0
          })(),
          sheetName: sheetName.trim() !== "" ? sheetName.trim() : undefined,
          quote:
            draftKind === "carrier_quote"
              ? {
                  party_id: quotePartyId.trim(),
                  origin_port_id: quoteOrigin.trim(),
                  destination_port_id: quoteDest.trim(),
                  quote_date: quoteDate.trim(),
                  amount: quoteAmount.trim(),
                  currency: quoteCurrency.trim(),
                }
              : undefined,
          rfp:
            draftKind === "tender_rfp"
              ? {
                  tender_id: rfpTenderId.trim(),
                  intake_code: rfpIntakeCode.trim(),
                }
              : undefined,
        }),
      ),
    onSuccess: () => {
      track("extraction_draft_created")
      invalidate()
    },
  })

  const [acceptedRateNote, setAcceptedRateNote] = useState(false)

  const acceptMutation = useMutation({
    mutationFn: (args: { draftId: string; candidateIndexes?: number[] }) =>
      acceptExtractionDraft(args.draftId, args.candidateIndexes),
    onSuccess: () => {
      track("extraction_draft_accepted")
      setAcceptedRateNote(true)
      setSelectedDraftId(null)
      invalidate()
    },
  })

  const rejectMutation = useMutation({
    mutationFn: (draftId: string) => rejectExtractionDraft(draftId),
    onSuccess: () => {
      track("extraction_draft_rejected")
      setSelectedDraftId(null)
      invalidate()
    },
  })

  const patchMutation = useMutation({
    mutationFn: (args: { draftId: string; candidates: ExtractionCandidate[] }) =>
      patchExtractionCandidates(args.draftId, args.candidates),
    onSuccess: () => {
      track("extraction_draft_patched")
      invalidate()
    },
  })

  const undoMutation = useMutation({
    mutationFn: (draftId: string) => undoExtractionDraft(draftId),
    onSuccess: () => {
      track("extraction_draft_undone")
      invalidate()
    },
  })

  useEffect(() => {
    return subscribeOperatorAction((id) => {
      if (id === "extract") {
        document.querySelector<HTMLButtonElement>("[data-operator-target=extract]")?.click()
        return
      }
      if (id === "accept-focus") {
        setSelectedDraftId((current) => current ?? query.data?.[0]?.id ?? null)
        queueMicrotask(() => {
          document.querySelector<HTMLButtonElement>("[data-operator-target=accept]")?.focus()
        })
      }
    })
  }, [query.data])

  const columns = [
    columnHelper.accessor("source_ref", {
      id: "source_ref",
      header: "Źródło",
      cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
    }),
    columnHelper.accessor("status", {
      id: "status",
      header: "Status",
      cell: (info) => info.getValue(),
    }),
    columnHelper.accessor("draft_kind", {
      id: "draft_kind",
      header: "Rodzaj",
      cell: (info) => info.getValue(),
    }),
    columnHelper.display({
      id: "parser",
      header: "Parser",
      cell: ({ row }) => {
        const name = row.original.payload.parser_name ?? "plain"
        const delta = row.original.payload.ab_delta_chars
        const deltaLabel = typeof delta === "number" ? ` Δ${delta}` : ""
        return (
          <span className="font-mono text-xs">
            {name}
            {deltaLabel}
          </span>
        )
      },
    }),
    columnHelper.display({
      id: "candidates",
      header: "Kandydaci",
      cell: ({ row }) => {
        const candidates = row.original.payload.candidates ?? []
        return (
          <span className="text-xs">
            {candidates.map((c) => `${c.code} ${c.amount_text} ${c.currency}`).join(" · ") || "—"}
          </span>
        )
      },
    }),
    columnHelper.display({
      id: "unparsed",
      header: "Nierozpoznane",
      cell: ({ row }) => {
        const regions = row.original.payload.unparsed_regions ?? []
        return <span className="text-xs text-muted-foreground">{regions.join(" · ") || "—"}</span>
      },
    }),
    columnHelper.display({
      id: "actions",
      header: "Akcje",
      cell: ({ row }) => (
        <Button
          type="button"
          size="sm"
          variant="outline"
          onClick={() => setSelectedDraftId(row.original.id)}
        >
          Otwórz
        </Button>
      ),
    }),
  ]

  return (
    <div className="space-y-3">
      <div>
        <h2 className="text-base font-semibold">Kolejka ekstrakcji (HITL)</h2>
        <p className="text-xs text-muted-foreground">
          Parser A/B · MockExtractor · akceptacja zapisuje stawkę, ofertę kanału albo przyjęcie RFP (`draft_kind`)
        </p>
      </div>

      {!ctx.organizationId || !ctx.userId ? (
        <div className="rounded-md border border-border bg-card p-3 text-sm">
          Ustaw identyfikatory sesji na stronie{" "}
          <Link className="underline" to="/session">
            Sesja
          </Link>
          .
        </div>
      ) : null}

      <div className="space-y-2 rounded-md border border-border bg-card p-3">
        <label className="block text-xs text-muted-foreground">
          draft_kind
          <select
            aria-label="Rodzaj szkicu"
            className="mt-1 h-8 w-full rounded-md border border-input bg-background px-2 text-sm"
            value={draftKind}
            onChange={(event) => setDraftKind(event.target.value)}
          >
            <option value="rate_line">rate_line</option>
            <option value="carrier_quote">carrier_quote</option>
            <option value="tender_rfp">tender_rfp</option>
          </select>
        </label>
        <label className="block text-xs text-muted-foreground">
          extract_path
          <select
            aria-label="Ścieżka ekstrakcji"
            className="mt-1 h-8 w-full rounded-md border border-input bg-background px-2 text-sm"
            value={extractPath}
            onChange={(event) => setExtractPath(event.target.value)}
          >
            <option value="text">text</option>
            <option value="image">image</option>
          </select>
        </label>
        {draftKind === "carrier_quote" ? (
          <div className="grid gap-2 lg:grid-cols-2">
            <Input aria-label="Kontrahent oferty" placeholder="party_id" value={quotePartyId} onChange={(e) => setQuotePartyId(e.target.value)} />
            <Input aria-label="POL oferty" placeholder="origin_port_id" value={quoteOrigin} onChange={(e) => setQuoteOrigin(e.target.value)} />
            <Input aria-label="POD oferty" placeholder="destination_port_id" value={quoteDest} onChange={(e) => setQuoteDest(e.target.value)} />
            <Input aria-label="Dzień oferty" placeholder="quote_date" value={quoteDate} onChange={(e) => setQuoteDate(e.target.value)} />
            <Input aria-label="Kwota oferty" placeholder="amount" value={quoteAmount} onChange={(e) => setQuoteAmount(e.target.value)} />
            <Input aria-label="Waluta oferty" placeholder="currency" value={quoteCurrency} onChange={(e) => setQuoteCurrency(e.target.value)} />
          </div>
        ) : null}
        {draftKind === "tender_rfp" ? (
          <div className="grid gap-2 lg:grid-cols-2">
            <Input aria-label="Przetarg przyjęcia RFP" placeholder="tender_id" value={rfpTenderId} onChange={(e) => setRfpTenderId(e.target.value)} />
            <Input aria-label="Kod przyjęcia RFP" placeholder="intake_code" value={rfpIntakeCode} onChange={(e) => setRfpIntakeCode(e.target.value)} />
          </div>
        ) : null}
        <label className="block text-xs text-muted-foreground">
          source_ref
          <Input
            className="mt-1"
            value={sourceRef}
            onChange={(e) => setSourceRef(e.target.value)}
          />
        </label>
        <label className="block text-xs text-muted-foreground">
          Tekst wejściowy
          <textarea
            className="mt-1 min-h-24 w-full rounded-md border border-input bg-background px-2 py-1.5 text-sm"
            value={inputText}
            onChange={(e) => {
              setDocumentBase64(null)
              setFileName(null)
              setInputText(e.target.value)
            }}
          />
        </label>
        <label className="block text-xs text-muted-foreground">
          Albo plik (PDF / tekst / Excel)
          <input
            className="mt-1 block w-full text-sm"
            type="file"
            onChange={(event) => {
              const file = event.target.files?.[0]
              if (!file) {
                setDocumentBase64(null)
                setFileName(null)
                return
              }
              void file.arrayBuffer().then((buffer) => {
                const bytes = new Uint8Array(buffer)
                let binary = ""
                for (const byte of bytes) {
                  binary += String.fromCharCode(byte)
                }
                setDocumentBase64(btoa(binary))
                setFileName(file.name)
              })
            }}
          />
          {fileName ? <span className="mt-1 block text-xs">{fileName}</span> : null}
        </label>
        {documentBase64 ? (
          <div className="grid gap-2 lg:grid-cols-2">
            <label className="block text-xs text-muted-foreground">
              Indeks arkusza Excel (0 = pierwszy)
              <Input
                className="mt-1"
                aria-label="Indeks arkusza Excel"
                inputMode="numeric"
                value={sheetIndex}
                disabled={sheetName.trim() !== ""}
                onChange={(event) => setSheetIndex(event.target.value)}
              />
            </label>
            <label className="block text-xs text-muted-foreground">
              Albo nazwa arkusza
              <Input
                className="mt-1"
                aria-label="Nazwa arkusza Excel"
                value={sheetName}
                onChange={(event) => setSheetName(event.target.value)}
              />
            </label>
          </div>
        ) : null}
        <Button
          type="button"
          data-operator-target="extract"
          disabled={createMutation.isPending || !ctx.organizationId}
          onClick={() => createMutation.mutate()}
        >
          Ekstrahuj → szkic
        </Button>
        {createMutation.isError ? (
          <p className="text-sm text-destructive">{(createMutation.error as Error).message}</p>
        ) : null}
      </div>

      {query.isLoading ? <div className="text-sm text-muted-foreground">Ładowanie…</div> : null}
      {query.isError ? (
        <div className="rounded-md border border-destructive/40 bg-card p-3 text-sm text-destructive">
          {(query.error as Error).message}
        </div>
      ) : null}

      <HitlReviewSplit
        draft={query.data?.find((row) => row.id === selectedDraftId) ?? null}
        pdfBase64={documentBase64}
        busy={
          acceptMutation.isPending ||
          rejectMutation.isPending ||
          patchMutation.isPending ||
          undoMutation.isPending
        }
        onAccept={(draftId, candidateIndexes) =>
          acceptMutation.mutate({ draftId, candidateIndexes })
        }
        onReject={(draftId) => rejectMutation.mutate(draftId)}
        onUndo={(draftId) => undoMutation.mutate(draftId)}
        onPatchCandidates={(draftId, candidates) =>
          patchMutation.mutate({ draftId, candidates })
        }
      />
      {acceptMutation.isError ? (
        <p className="text-sm text-destructive">{(acceptMutation.error as Error).message}</p>
      ) : null}
      {patchMutation.isError ? (
        <p className="text-sm text-destructive">{(patchMutation.error as Error).message}</p>
      ) : null}
      {undoMutation.isError ? (
        <p className="text-sm text-destructive">{(undoMutation.error as Error).message}</p>
      ) : null}
      {acceptedRateNote ? (
        <p className="text-sm">
          Zaakceptowano — zapisano stawki kupna.{" "}
          <Link className="underline" to="/rate-lines">
            Stawki
          </Link>
        </p>
      ) : null}

      {query.data ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.extractions.tableKey}
          columns={columns}
          data={query.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Szukaj szkicu…"
        />
      ) : null}
    </div>
  )
}
