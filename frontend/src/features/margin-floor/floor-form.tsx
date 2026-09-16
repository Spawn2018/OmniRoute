import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createMarginFloor,
  makeMarginFloorPayload,
} from "@/lib/margin-floors-api"

export function MarginFloorComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [floorCode, setFloorCode] = useState("floor_gdn_ham")
  const [originUnlocode, setOriginUnlocode] = useState("PLGDN")
  const [destinationUnlocode, setDestinationUnlocode] = useState("DEHAM")
  const [floorAmount, setFloorAmount] = useState("120")
  const [floorCurrency, setFloorCurrency] = useState("EUR")
  const [ref, setRef] = useState("fixture://margin-floor/")
  const save = useMutation({
    mutationFn: () =>
      createMarginFloor(
        makeMarginFloorPayload({
          floorCode,
          originUnlocode,
          destinationUnlocode,
          floorAmount,
          floorCurrency,
          sourceRef: ref,
        }),
      ),
    onSuccess: () => {
      setRef("fixture://margin-floor/")
      void qc.invalidateQueries({
        queryKey: ["margin-floors", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-margin-floor="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        floor_code
        <input
          aria-label="floor_code podłoga"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setFloorCode(e.target.value)}
          required
          value={floorCode}
        />
      </label>
      <label className="text-xs">
        origin_unlocode
        <input
          aria-label="origin_unlocode"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm uppercase"
          maxLength={5}
          onChange={(e) => setOriginUnlocode(e.target.value)}
          required
          value={originUnlocode}
        />
      </label>
      <label className="text-xs">
        destination_unlocode
        <input
          aria-label="destination_unlocode"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm uppercase"
          maxLength={5}
          onChange={(e) => setDestinationUnlocode(e.target.value)}
          required
          value={destinationUnlocode}
        />
      </label>
      <label className="text-xs">
        floor_amount
        <input
          aria-label="floor_amount kwota"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setFloorAmount(e.target.value)}
          required
          value={floorAmount}
        />
      </label>
      <label className="text-xs">
        floor_currency
        <input
          aria-label="floor_currency waluta"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          maxLength={3}
          onChange={(e) => setFloorCurrency(e.target.value)}
          required
          value={floorCurrency}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref margin floor"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz podłogę marży
      </Button>
    </form>
  )
}
