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
  rejectExtractionDraft,
  type ExtractionDraft,
} from "@/lib/extractions-api"
import { getTenantContext } from "@/lib/tenant"

const columnHelper = createColumnHelper<ExtractionDraft>()

const COLUMN_LABELS = {
  source_ref: "Źródło",
  status: "Status",
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
        }),
      ),
    onSuccess: () => {
      track("extraction_draft_created")
      invalidate()
    },
  })

  const [acceptedRateNote, setAcceptedRateNote] = useState(false)

  const acceptMutation = useMutation({
    mutationFn: (draftId: string) => acceptExtractionDraft(draftId),
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
          Parser A/B · MockExtractor · akceptacja zapisuje stawki kupna w tej samej transakcji
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
          Albo plik (PDF / tekst)
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
        busy={acceptMutation.isPending || rejectMutation.isPending}
        onAccept={(draftId) => acceptMutation.mutate(draftId)}
        onReject={(draftId) => rejectMutation.mutate(draftId)}
      />
      {acceptMutation.isError ? (
        <p className="text-sm text-destructive">{(acceptMutation.error as Error).message}</p>
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
