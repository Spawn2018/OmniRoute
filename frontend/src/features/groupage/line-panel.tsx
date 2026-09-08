import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { fetchGroupageLines, groupageLineWrite, saveGroupageLine } from "@/lib/groupage-lines-api"

type LineDraft = {
  code: string
  startPlace: string
  endPlace: string
  cutoff: string
  days: string
  dows: number[]
  originRef: string
}

const EMPTY: LineDraft = {
  code: "",
  startPlace: "",
  endPlace: "",
  cutoff: "16:00",
  days: "2",
  dows: [1, 2, 3, 4, 5],
  originRef: "fixture://groupage-line/",
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

function LineSlot(args: {
  caption: string
  hint: string
  value: string
  onValue: (next: string) => void
  clock?: boolean
}) {
  return (
    <p className="text-xs">
      <span className="block">{args.caption}</span>
      <input
        aria-label={args.hint}
        className="mt-1 h-9 w-full border px-1.5 font-mono text-[11px]"
        type={args.clock ? "time" : "text"}
        value={args.value}
        onChange={(ev) => args.onValue(ev.target.value)}
        required
      />
    </p>
  )
}

function LineFields(args: { draft: LineDraft; patch: (next: LineDraft) => void }) {
  const row = args.draft
  return (
    <fieldset className="grid grid-cols-2 gap-2">
      <legend className="col-span-2 text-xs">Linia drobnicy</legend>
      <LineSlot
        caption="Kod linii"
        hint="Kod linii drobnicy"
        value={row.code}
        onValue={(code) => args.patch({ ...row, code })}
      />
      <LineSlot
        caption="Cutoff lokalny"
        hint="Godzina odcięcia linii"
        clock
        value={row.cutoff}
        onValue={(cutoff) => args.patch({ ...row, cutoff })}
      />
      <LineSlot
        caption="Start (strefa lub adres)"
        hint="Identyfikator startu linii"
        value={row.startPlace}
        onValue={(startPlace) => args.patch({ ...row, startPlace })}
      />
      <LineSlot
        caption="Koniec (strefa lub adres)"
        hint="Identyfikator końca linii"
        value={row.endPlace}
        onValue={(endPlace) => args.patch({ ...row, endPlace })}
      />
      <LineSlot
        caption="Dni tranzytu"
        hint="Liczba dni tranzytu linii"
        value={row.days}
        onValue={(days) => args.patch({ ...row, days })}
      />
      <LineSlot
        caption="Źródło zapisu"
        hint="Źródło zapisu linii drobnicy"
        value={row.originRef}
        onValue={(originRef) => args.patch({ ...row, originRef })}
      />
      <div className="col-span-2 flex flex-wrap gap-1">
        {DOW_MARKS.map((item) => (
          <button
            key={item.dow}
            type="button"
            aria-pressed={row.dows.includes(item.dow)}
            className="border-input h-7 rounded-md border px-2 text-xs"
            onClick={() => args.patch({ ...row, dows: toggleDow(row.dows, item.dow) })}
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
    mutationFn: () =>
      saveGroupageLine(
        groupageLineWrite({
          code: draft.code,
          originId: draft.startPlace,
          destId: draft.endPlace,
          cutoff: draft.cutoff,
          days: draft.days,
          dows: draft.dows,
          sourceRef: draft.originRef,
        }),
      ),
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
