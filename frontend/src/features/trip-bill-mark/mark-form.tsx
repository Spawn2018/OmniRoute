import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildTripBillMarkWrite,
  saveTripBillMark,
} from "@/lib/trip-bill-marks-api"

export function TripBillMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("bill_ready_01")
  const [kind, setKind] = useState("ready")
  const [origin, setOrigin] = useState("fixture://trip-bill-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveTripBillMark(buildTripBillMarkWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("bill_ready_01")
      setKind("ready")
      setOrigin("fixture://trip-bill-mark/")
      void cache.invalidateQueries({
        queryKey: ["trip-bill-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-4 border-l-2 border-amber-700/40 pl-4"
      data-trip-bill-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL znacznika gotowości przejazdu do fakturowania (ready/held/billed/other).
        Widok SQL trips_to_bill i F1 KSeF live zostaja poza tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://trip-bill-mark/…)"
        ariaLabel="Pochodzenie znacznika gotowości do FV"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod znacznika (snake 2–32)</span>
        <input
          aria-label="Kod znacznika gotowości do FV"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Rodzaj gotowości</span>
        <select
          aria-label="Rodzaj gotowości ready held billed other"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          <option value="ready">ready — gotowy</option>
          <option value="held">held — wstrzymany</option>
          <option value="billed">billed — zafakturowany</option>
          <option value="other">other — pozostale</option>
        </select>
      </label>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik gotowości do FV
      </Button>
    </form>
  )
}
