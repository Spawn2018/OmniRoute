import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listParcels, parcelWrite, persistParcel } from "@/lib/shipment-packages-api"

type ScanDraft = {
  orderKey: string
  haltRef: string
  parcelToken: string
  stageMark: string
  scanMark: string
  originNote: string
}

const BLANK: ScanDraft = {
  orderKey: "",
  haltRef: "",
  parcelToken: "",
  stageMark: "at_stop",
  scanMark: "omni://shipment-package/",
  originNote: "fixture://shipment-package/",
}

function ScanCell(args: {
  heading: string
  spoken: string
  filled: string
  put: (next: string) => void
}) {
  return (
    <div className="flex flex-col gap-0.5">
      <span className="text-xs">{args.heading}</span>
      <input
        aria-label={args.spoken}
        className="h-8 rounded-sm border px-2 font-mono text-xs"
        value={args.filled}
        onChange={(change) => args.put(change.target.value)}
        required
      />
    </div>
  )
}

function ScanFields(args: { draft: ScanDraft; put: (next: ScanDraft) => void }) {
  const row = args.draft
  return (
    <fieldset className="grid grid-cols-2 gap-2">
      <legend className="col-span-2 text-xs">Skan paczki</legend>
      <ScanCell
        heading="Zlecenie"
        spoken="Identyfikator zlecenia paczki"
        filled={row.orderKey}
        put={(orderKey) => args.put({ ...row, orderKey })}
      />
      <ScanCell
        heading="Punkt trasy"
        spoken="Identyfikator stopu paczki"
        filled={row.haltRef}
        put={(haltRef) => args.put({ ...row, haltRef })}
      />
      <ScanCell
        heading="Kod paczki"
        spoken="Kod snake paczki"
        filled={row.parcelToken}
        put={(parcelToken) => args.put({ ...row, parcelToken })}
      />
      <ScanCell
        heading="Status"
        spoken="Status poziomu paczki"
        filled={row.stageMark}
        put={(stageMark) => args.put({ ...row, stageMark })}
      />
      <ScanCell
        heading="Token skanu"
        spoken="Token QR Omni paczki"
        filled={row.scanMark}
        put={(scanMark) => args.put({ ...row, scanMark })}
      />
      <ScanCell
        heading="Pochodzenie"
        spoken="Pochodzenie zapisu paczki"
        filled={row.originNote}
        put={(originNote) => args.put({ ...row, originNote })}
      />
    </fieldset>
  )
}

function ScanSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(BLANK)
  const persist = useMutation({
    mutationFn: () => persistParcel(parcelWrite(draft)),
    onSuccess: () => {
      setDraft({ ...BLANK })
      void cache.invalidateQueries({ queryKey: ["parcels", args.organizationId] })
    },
  })
  return (
    <form
      className="grid gap-2"
      data-parcel="scan-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Token `omni://shipment-package/kod` albo `fixture://omni-qr/kod`. Inny kod kreskowy odpada. Stop musi być z tego zlecenia.
      </p>
      <ScanFields draft={draft} put={setDraft} />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz skan paczki
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function ParcelRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["parcels", args.organizationId],
    queryFn: listParcels,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <table data-parcel="rows" className="w-full text-xs">
        <tbody>
          {(listed.data ?? []).map((row) => (
            <tr key={row.id}>
              <td className="pr-2 font-mono">{row.package_code}</td>
              <td>{row.package_status}</td>
              <td className="font-mono">{row.scan_token}</td>
              <td>
                <Link className="underline" to="/shipments">
                  zlecenie
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

export function ParcelScanPanel(args: { organizationId: string | null }) {
  if (!args.organizationId) return null
  return (
    <>
      <ScanSave organizationId={args.organizationId} />
      <ParcelRows organizationId={args.organizationId} />
    </>
  )
}
