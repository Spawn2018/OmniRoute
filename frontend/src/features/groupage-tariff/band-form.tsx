import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { bandWrite, listWeightBands, persistWeightBand } from "@/lib/groupage-tariffs-api"

type BandDraft = {
  zoneToken: string
  bandToken: string
  massMark: string
  cashMark: string
  ccyMark: string
  originStamp: string
}

const EMPTY_BAND: BandDraft = {
  zoneToken: "",
  bandToken: "",
  massMark: "100.0000",
  cashMark: "85.5000",
  ccyMark: "EUR",
  originStamp: "fixture://groupage-tariff/",
}

function BandSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_BAND)
  const persist = useMutation({
    mutationFn: () => persistWeightBand(bandWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_BAND })
      void cache.invalidateQueries({ queryKey: ["weight-bands", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-tariff="band-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Próg `chargeable_weight` na strefie `postal_zone`. Kwota to Decimal z walutą. Matching zostaje
        w P1. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Identyfikator strefy taryfowej
        <input
          aria-label="Identyfikator strefy taryfowej"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.zoneToken}
          onChange={(change) => setDraft({ ...draft, zoneToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kod snake progu cennika
        <input
          aria-label="Kod snake progu cennika"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.bandToken}
          onChange={(change) => setDraft({ ...draft, bandToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Próg wagi płatnej
        <input
          aria-label="Próg wagi płatnej"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.massMark}
          onChange={(change) => setDraft({ ...draft, massMark: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kwota kupna progu
        <input
          aria-label="Kwota kupna progu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.cashMark}
          onChange={(change) => setDraft({ ...draft, cashMark: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Waluta ISO progu
        <input
          aria-label="Waluta ISO progu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.ccyMark}
          onChange={(change) => setDraft({ ...draft, ccyMark: change.target.value })}
          required
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://groupage-tariff/…)"
        ariaLabel="Pochodzenie zapisu cennika"
        value={draft.originStamp}
        onChange={(originStamp) => setDraft({ ...draft, originStamp })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz próg cennika drobnicy
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function BandRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["weight-bands", args.organizationId],
    queryFn: listWeightBands,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-tariff="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="flex flex-wrap items-baseline gap-2 font-mono">
            <span>{row.tariff_code}</span>
            <span>{row.chargeable_weight}</span>
            <Money amount={row.amount} currency={row.currency} />
            <Link className="underline" to="/locations">
              strefa
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}

export function WeightBandPanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <BandSave organizationId={args.organizationId} />
      <BandRows organizationId={args.organizationId} />
    </>
  )
}
