import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { ledgerWrite, listLedgerMarks, persistLedgerMark } from "@/lib/prediction-ledgers-api"

type LedgerDraft = {
  kindStamp: string
  horizonStamp: string
  lowStamp: string
  highStamp: string
  crpsStamp: string
  maeStamp: string
  modelStamp: string
  originStamp: string
}

const EMPTY_LEDGER: LedgerDraft = {
  kindStamp: "eta",
  horizonStamp: "h24h",
  lowStamp: "30",
  highStamp: "90",
  crpsStamp: "0.25",
  maeStamp: "12",
  modelStamp: "hist_eta",
  originStamp: "fixture://prediction-ledger/",
}

function LedgerSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_LEDGER)
  const persist = useMutation({
    mutationFn: () => persistLedgerMark(ledgerWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_LEDGER })
      void cache.invalidateQueries({ queryKey: ["ledger-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-prediction-ledger="ledger-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Przedział i metryka po fakcie. Serwis nie liczy CRPS. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj
        <select
          aria-label="Rodzaj predykcji"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindStamp}
          onChange={(change) => setDraft({ ...draft, kindStamp: change.target.value })}
        >
          <option value="eta">eta</option>
          <option value="transit">transit</option>
          <option value="disrupt">disrupt</option>
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Horyzont
        <select
          aria-label="Horyzont predykcji"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.horizonStamp}
          onChange={(change) => setDraft({ ...draft, horizonStamp: change.target.value })}
        >
          <option value="h1h">h1h</option>
          <option value="h6h">h6h</option>
          <option value="h24h">h24h</option>
          <option value="h7d">h7d</option>
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Przedział low (minuty)
        <input
          aria-label="Przedział low"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.lowStamp}
          onChange={(change) => setDraft({ ...draft, lowStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Przedział high (minuty)
        <input
          aria-label="Przedział high"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.highStamp}
          onChange={(change) => setDraft({ ...draft, highStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        CRPS
        <input
          aria-label="CRPS"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.crpsStamp}
          onChange={(change) => setDraft({ ...draft, crpsStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        MAE
        <input
          aria-label="MAE"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.maeStamp}
          onChange={(change) => setDraft({ ...draft, maeStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kod modelu (snake)
        <input
          aria-label="Kod modelu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.modelStamp}
          onChange={(change) => setDraft({ ...draft, modelStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        source_ref (tenant:manual albo fixture://prediction-ledger/…)
        <input
          aria-label="source_ref ledgeru predykcji"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz ledger predykcji
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function LedgerRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["ledger-marks", args.organizationId],
    queryFn: listLedgerMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-prediction-ledger="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.prediction_kind} {row.horizon_code} crps {row.crps}
          </li>
        ))}
      </ul>
    </>
  )
}

export function LedgerPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <LedgerSave organizationId={args.organizationId} />
      <LedgerRows organizationId={args.organizationId} />
    </div>
  )
}
