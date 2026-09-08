import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { bundleWrite, listBundleSlots, persistBundleSlot } from "@/lib/charge-templates-api"

type BundleDraft = {
  packToken: string
  feeToken: string
  fromStamp: string
  untilStamp: string
  originStamp: string
}

const EMPTY_BUNDLE: BundleDraft = {
  packToken: "spot_thc",
  feeToken: "THC",
  fromStamp: "2026-01-01",
  untilStamp: "2026-12-31",
  originStamp: "fixture://charge-template/",
}

function BundleSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_BUNDLE)
  const persist = useMutation({
    mutationFn: () => persistBundleSlot(bundleWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_BUNDLE })
      void cache.invalidateQueries({ queryKey: ["bundle-slots", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-charge-template="bundle-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Kolekcja kodów opłat i daty ważności jako dane. Nakładanie GiST zostaje leftover. Marża
        zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kod snake szablonu
        <input
          aria-label="Kod snake szablonu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.packToken}
          onChange={(change) => setDraft({ ...draft, packToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Token kodu opłaty
        <input
          aria-label="Token kodu opłaty"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.feeToken}
          onChange={(change) => setDraft({ ...draft, feeToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Ważne od
        <input
          aria-label="Ważne od"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          type="date"
          value={draft.fromStamp}
          onChange={(change) => setDraft({ ...draft, fromStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Ważne do
        <input
          aria-label="Ważne do"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          type="date"
          value={draft.untilStamp}
          onChange={(change) => setDraft({ ...draft, untilStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Pochodzenie zapisu szablonu opłat
        <input
          aria-label="Pochodzenie zapisu szablonu opłat"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz szablon opłat
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function BundleRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["bundle-slots", args.organizationId],
    queryFn: listBundleSlots,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-charge-template="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="flex flex-wrap items-baseline gap-2 font-mono">
            <span>{row.template_code}</span>
            <span>{row.charge_code}</span>
            <span>
              {row.valid_from}–{row.valid_until}
            </span>
          </li>
        ))}
      </ul>
    </>
  )
}

export function BundleSlotPanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <BundleSave organizationId={args.organizationId} />
      <BundleRows organizationId={args.organizationId} />
    </>
  )
}
