import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
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
        Etap łańcucha plus status danych umowy. Status `missing` pokazuje stały tekst
        „brak danych umowy”. Nie ma kary, scoringu ani silnika. Marża zostaje na `/charges`.
      </p>
      <fieldset className="grid gap-1 text-xs">
        <legend>Etap łańcucha (allowlista)</legend>
        {STAGES.map((token) => (
          <label key={token} className="flex items-center gap-2 font-mono">
            <input
              type="radio"
              name="chain-stage"
              aria-label={`Etap ${token}`}
              checked={draft.stageStamp === token}
              onChange={() => setDraft({ ...draft, stageStamp: token })}
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <fieldset className="grid gap-1 text-xs">
        <legend>Dane umowy (nie klauzula SLA)</legend>
        {PACTS.map((token) => (
          <label key={token} className="flex items-center gap-2 font-mono">
            <input
              type="radio"
              name="contract-pact"
              aria-label={`Umowa ${token}`}
              checked={draft.pactStamp === token}
              onChange={() => setDraft({ ...draft, pactStamp: token })}
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://tower-impact/…)"
        ariaLabel="source_ref skutku wieży"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
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
  const rows = listed.data ?? []
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tower-impact="rows" className="flex flex-col gap-1 text-xs">
        {rows.map((row) => {
          const gap = row.contract_gap_label ? ` · ${row.contract_gap_label}` : ""
          return (
            <li key={row.id} className="font-mono">
              {row.chain_stage} {row.contract_data_status}
              {gap}
            </li>
          )
        })}
      </ul>
    </>
  )
}

export function ImpactPanel(args: { organizationId: string | null }) {
  return (
    <div className="flex flex-col gap-8 md:flex-row">
      <ImpactSave organizationId={args.organizationId} />
      <ImpactRows organizationId={args.organizationId} />
    </div>
  )
}
