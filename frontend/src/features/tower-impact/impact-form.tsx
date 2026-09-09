import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { impactWrite, listImpactMarks, persistImpactMark } from "@/lib/tower-impacts-api"

type ChainDraft = {
  stageStamp: string
  pactStamp: string
  originStamp: string
}

const EMPTY_CHAIN: ChainDraft = {
  stageStamp: "stock",
  pactStamp: "missing",
  originStamp: "fixture://tower-impact/",
}

const STAGES = ["stock", "production", "sales", "ebitda"] as const
const PACTS = ["missing", "recorded"] as const

function ImpactSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_CHAIN)
  const persist = useMutation({
    mutationFn: () => persistImpactMark(impactWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_CHAIN })
      void cache.invalidateQueries({ queryKey: ["chain-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-tower-impact="chain-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Etap łańcucha (`stock` / `production` / `sales` / `ebitda`) plus status danych umowy. Status
        `missing` pokazuje stały tekst „brak danych umowy”. Nie ma kary, scoringu ani silnika. Marża
        zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Etap łańcucha (allowlista)
        <select
          aria-label="Etap łańcucha wieży"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.stageStamp}
          onChange={(change) => setDraft({ ...draft, stageStamp: change.target.value })}
          required
        >
          {STAGES.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Dane umowy (nie klauzula SLA)
        <select
          aria-label="Status danych umowy"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.pactStamp}
          onChange={(change) => setDraft({ ...draft, pactStamp: change.target.value })}
          required
        >
          {PACTS.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        source_ref (tenant:manual albo fixture://tower-impact/…)
        <input
          aria-label="source_ref skutku wieży"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz skutek wieży
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function ImpactRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["chain-marks", args.organizationId],
    queryFn: listImpactMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tower-impact="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.chain_stage} {row.contract_data_status}
            {row.contract_gap_label ? ` · ${row.contract_gap_label}` : ""}
          </li>
        ))}
      </ul>
    </>
  )
}

export function ImpactPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <ImpactSave organizationId={args.organizationId} />
      <ImpactRows organizationId={args.organizationId} />
    </div>
  )
}
