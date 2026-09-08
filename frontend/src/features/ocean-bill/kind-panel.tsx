import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { ladingWrite, listHouseMarks, persistHouseMark } from "@/lib/ocean-bills-api"

const KINDS = ["hbl", "mbl"] as const

type LadingDraft = {
  consignmentToken: string
  houseToken: string
  kindToken: string
  originStamp: string
}

const EMPTY_LADING: LadingDraft = {
  consignmentToken: "",
  houseToken: "",
  kindToken: "hbl",
  originStamp: "fixture://ocean-bill/",
}

function KindSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_LADING)
  const persist = useMutation({
    mutationFn: () => persistHouseMark(ladingWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_LADING })
      void cache.invalidateQueries({ queryKey: ["house-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-ocean-bill="kind-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Numer HBL albo MBL na zleceniu. To nie PDF i nie booking armatora. Konsolidacja
        wielu house zostaje leftover D6b.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Identyfikator zlecenia konosamentu
        <input
          aria-label="Identyfikator zlecenia konosamentu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.consignmentToken}
          onChange={(change) => setDraft({ ...draft, consignmentToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Numer listu HBL/MBL
        <input
          aria-label="Numer listu HBL/MBL"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.houseToken}
          onChange={(change) => setDraft({ ...draft, houseToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj listu
        <select
          aria-label="Rodzaj listu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindToken}
          onChange={(change) => setDraft({ ...draft, kindToken: change.target.value })}
        >
          {KINDS.map((kind) => (
            <option key={kind} value={kind}>
              {kind}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Pochodzenie zapisu konosamentu
        <input
          aria-label="Pochodzenie zapisu konosamentu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz konosament
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function KindRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["house-marks", args.organizationId],
    queryFn: listHouseMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-ocean-bill="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="flex flex-wrap gap-2 font-mono">
            <span>{row.bill_kind}</span>
            <span>{row.bill_no}</span>
            <Link className="underline" to="/shipments">
              zlecenie
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}

export function HouseKindPanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <KindSave organizationId={args.organizationId} />
      <KindRows organizationId={args.organizationId} />
    </>
  )
}
