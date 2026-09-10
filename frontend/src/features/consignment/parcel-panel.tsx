import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listParcels, parcelWrite, persistParcel } from "@/lib/consignments-api"

type ParcelDraft = {
  shipmentToken: string
  parcelRef: string
  originStamp: string
}

const EMPTY_PARCEL: ParcelDraft = {
  shipmentToken: "",
  parcelRef: "",
  originStamp: "fixture://consignment/",
}

function DraftField(args: {
  label: string
  value: string
  onValue: (next: string) => void
}) {
  return (
    <label className="grid gap-1 text-xs">
      <span>{args.label}</span>
      <input
        aria-label={args.label}
        className="h-9 rounded-md border bg-background px-2 font-mono"
        value={args.value}
        onChange={(change) => args.onValue(change.target.value)}
        required
      />
    </label>
  )
}

function ParcelDraftFields(args: {
  draft: ParcelDraft
  put: (next: ParcelDraft) => void
}) {
  return (
    <>
      <DraftField
        label="Identyfikator zlecenia"
        value={args.draft.shipmentToken}
        onValue={(shipmentToken) => args.put({ ...args.draft, shipmentToken })}
      />
      <DraftField
        label="Numer przesyłki"
        value={args.draft.parcelRef}
        onValue={(parcelRef) => args.put({ ...args.draft, parcelRef })}
      />
      <DraftField
        label="Pochodzenie zapisu przesyłki"
        value={args.draft.originStamp}
        onValue={(originStamp) => args.put({ ...args.draft, originStamp })}
      />
    </>
  )
}

function ParcelSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_PARCEL)
  const persist = useMutation({
    mutationFn: () => persistParcel(parcelWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_PARCEL })
      void cache.invalidateQueries({ queryKey: ["consignments", args.organizationId] })
    },
  })
  return (
    <form
      className="flex max-w-sm flex-col gap-3"
      data-consignment="parcel-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Przesyłka na zleceniu. Kilka wierszy na jedno zlecenie jest dozwolone. To nie
        paczka QR i nie unique FTL.
      </p>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
      <ParcelDraftFields draft={draft} put={setDraft} />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz przesyłkę
      </Button>
    </form>
  )
}

function ConsignmentMarks(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["consignments", args.organizationId],
    queryFn: listParcels,
    enabled: args.organizationId !== null,
    retry: false,
  })
  const marks = listed.data ?? []
  return (
    <div data-consignment="rows" className="flex flex-col gap-1 text-xs">
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      {marks.map((row) => (
        <p key={row.id} className="flex flex-wrap gap-2 font-mono">
          <span>{row.consignment_ref}</span>
          <Link className="underline" to="/shipments">
            zlecenie
          </Link>
        </p>
      ))}
    </div>
  )
}

export function ParcelMarkPanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <ParcelSave organizationId={args.organizationId} />
      <ConsignmentMarks organizationId={args.organizationId} />
    </>
  )
}
