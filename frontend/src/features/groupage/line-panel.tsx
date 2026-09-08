import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { fetchGroupageLines, groupageLineWrite, saveGroupageLine } from "@/lib/groupage-lines-api"

type LineDraft = {
  code: string
  originId: string
  destId: string
  cutoff: string
  days: string
  dows: number[]
  sourceRef: string
}

const EMPTY: LineDraft = {
  code: "",
  originId: "",
  destId: "",
  cutoff: "16:00",
  days: "2",
  dows: [1, 2, 3, 4, 5],
  sourceRef: "fixture://groupage-line/",
}

const DOW_MARKS = [
  { dow: 1, mark: "Pn" },
  { dow: 2, mark: "Wt" },
  { dow: 3, mark: "Śr" },
  { dow: 4, mark: "Cz" },
  { dow: 5, mark: "Pt" },
  { dow: 6, mark: "So" },
  { dow: 7, mark: "Nd" },
] as const

function toggleDow(current: number[], dow: number): number[] {
  if (current.includes(dow)) {
    return current.filter((item) => item !== dow)
  }
  return [...current, dow].sort((left, right) => left - right)
}

function LineFields(args: { draft: LineDraft; patch: (next: LineDraft) => void }) {
  return (
    <fieldset className="grid grid-cols-2 gap-2">
      <legend className="col-span-2 text-xs">Linia drobnicy</legend>
      <label className="text-xs">
        Kod linii
        <input
          aria-label="Kod linii drobnicy"
          className="border-input mt-1 h-8 w-full rounded-md border px-2 font-mono text-xs"
          name="line_code"
          value={args.draft.code}
          onChange={(event) => args.patch({ ...args.draft, code: event.currentTarget.value })}
          required
        />
      </label>
      <label className="text-xs">
        Cutoff lokalny
        <input
          aria-label="Godzina odcięcia linii"
          className="border-input mt-1 h-8 w-full rounded-md border px-2 font-mono text-xs"
          name="cutoff_local"
          type="time"
          value={args.draft.cutoff}
          onChange={(event) => args.patch({ ...args.draft, cutoff: event.currentTarget.value })}
          required
        />
      </label>
      <label className="text-xs">
        Start (strefa lub adres)
        <input
          aria-label="Identyfikator startu linii"
          className="border-input mt-1 h-8 w-full rounded-md border px-2 font-mono text-xs"
          name="origin_location_id"
          value={args.draft.originId}
          onChange={(event) => args.patch({ ...args.draft, originId: event.currentTarget.value })}
          required
        />
      </label>
      <label className="text-xs">
        Koniec (strefa lub adres)
        <input
          aria-label="Identyfikator końca linii"
          className="border-input mt-1 h-8 w-full rounded-md border px-2 font-mono text-xs"
          name="destination_location_id"
          value={args.draft.destId}
          onChange={(event) => args.patch({ ...args.draft, destId: event.currentTarget.value })}
          required
        />
      </label>
      <label className="text-xs">
        Dni tranzytu
        <input
          aria-label="Liczba dni tranzytu linii"
          className="border-input mt-1 h-8 w-full rounded-md border px-2 font-mono text-xs"
          name="transit_days"
          inputMode="numeric"
          value={args.draft.days}
          onChange={(event) => args.patch({ ...args.draft, days: event.currentTarget.value })}
          required
        />
      </label>
      <label className="text-xs">
        Źródło zapisu
        <input
          aria-label="Źródło zapisu linii drobnicy"
          className="border-input mt-1 h-8 w-full rounded-md border px-2 font-mono text-xs"
          name="source_ref"
          value={args.draft.sourceRef}
          onChange={(event) =>
            args.patch({ ...args.draft, sourceRef: event.currentTarget.value })
          }
          required
        />
      </label>
      <div className="col-span-2 flex flex-wrap gap-1">
        {DOW_MARKS.map((item) => (
          <button
            key={item.dow}
            type="button"
            aria-pressed={args.draft.dows.includes(item.dow)}
            className="border-input h-7 rounded-md border px-2 text-xs"
            onClick={() => args.patch({ ...args.draft, dows: toggleDow(args.draft.dows, item.dow) })}
          >
            {item.mark}
          </button>
        ))}
      </div>
    </fieldset>
  )
}

function LineSaveForm(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY)
  const persist = useMutation({
    mutationFn: () => saveGroupageLine(groupageLineWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY })
      void cache.invalidateQueries({ queryKey: ["groupage-lines", args.organizationId] })
    },
  })
  return (
    <form
      className="grid gap-2"
      data-groupage="line-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Cutoff to godzina odcięcia, nie wyliczenie. ISODOW 1–7. Port UN/LOCODE odrzuca. Nie WMS.
      </p>
      <LineFields draft={draft} patch={setDraft} />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz linię drobnicy
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function LineRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["groupage-lines", args.organizationId],
    queryFn: fetchGroupageLines,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <table data-groupage="lines" className="w-full text-xs">
        <tbody>
          {(listed.data ?? []).map((row) => (
            <tr key={row.id}>
              <td className="pr-2 font-mono">{row.line_code}</td>
              <td>{row.cutoff_local}</td>
              <td>{row.transit_days} d</td>
              <td className="font-mono">{row.operating_dows.join(",")}</td>
              <td>
                <Link className="underline" to="/locations">
                  lokalizacja
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

export function GroupageLinePanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <LineSaveForm organizationId={args.organizationId} />
      <LineRows organizationId={args.organizationId} />
    </>
  )
}
