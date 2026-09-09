import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { levyWrite, listLevyMarks, persistLevyMark } from "@/lib/local-charges-api"

type LevyDraft = {
  kindToken: string
  cashMark: string
  ccyMark: string
  originStamp: string
  portToken: string
  isoToken: string
}

const EMPTY_LEVY: LevyDraft = {
  kindToken: "thc",
  cashMark: "80.0000",
  ccyMark: "EUR",
  originStamp: "fixture://local-charge/",
  portToken: "",
  isoToken: "",
}

function LevySave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_LEVY)
  const persist = useMutation({
    mutationFn: () => persistLevyMark(levyWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_LEVY })
      void cache.invalidateQueries({ queryKey: ["levy-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-local-charge="levy-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Dopłata THC/ISPS/seal/amendment jako dana Decimal. Opcjonalny UN/LOCODE i typ ISO,
        nie FK katalogu. Warning braków zostaje leftover. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj dopłaty lokalnej
        <select
          aria-label="Rodzaj dopłaty lokalnej"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindToken}
          onChange={(change) => setDraft({ ...draft, kindToken: change.target.value })}
        >
          <option value="thc">thc</option>
          <option value="isps">isps</option>
          <option value="seal">seal</option>
          <option value="amendment">amendment</option>
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Kwota dopłaty
        <input
          aria-label="Kwota dopłaty"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.cashMark}
          onChange={(change) => setDraft({ ...draft, cashMark: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Waluta ISO dopłaty
        <input
          aria-label="Waluta ISO dopłaty"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.ccyMark}
          onChange={(change) => setDraft({ ...draft, ccyMark: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Port UN/LOCODE (opcjonalnie)
        <input
          aria-label="Port UN/LOCODE dopłaty"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.portToken}
          onChange={(change) => setDraft({ ...draft, portToken: change.target.value })}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Typ ISO kontenera (opcjonalnie)
        <input
          aria-label="Typ ISO kontenera dopłaty"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.isoToken}
          onChange={(change) => setDraft({ ...draft, isoToken: change.target.value })}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Pochodzenie zapisu dopłaty lokalnej
        <input
          aria-label="Pochodzenie zapisu dopłaty lokalnej"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz dopłatę lokalną
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function LevyRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["levy-marks", args.organizationId],
    queryFn: listLevyMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-local-charge="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="flex flex-wrap items-baseline gap-2 font-mono">
            <span>{row.charge_kind}</span>
            {row.port_unlocode ? <span>{row.port_unlocode}</span> : null}
            {row.iso_size_type ? <span>{row.iso_size_type}</span> : null}
            <Money amount={row.amount} currency={row.currency} />
          </li>
        ))}
      </ul>
    </>
  )
}

export function LevyKindPanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <LevySave organizationId={args.organizationId} />
      <LevyRows organizationId={args.organizationId} />
    </>
  )
}
