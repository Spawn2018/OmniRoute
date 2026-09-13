import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { createFerryBookingMark, makeFerryBookingMarkPayload } from "@/lib/ferry-booking-marks-api"

const BOOKING_KINDS = ["booking", "window", "sailing", "other"] as const

export function FerryBookingMarkSave({ organizationId }: { organizationId: string | null }) {
  const queryClient = useQueryClient()
  const [code, setCode] = useState("fbk_book_01")
  const [kind, setKind] = useState("booking")
  const [origin, setOrigin] = useState("fixture://ferry-booking-mark/")
  const write = useMutation({
    mutationFn: () => createFerryBookingMark(makeFerryBookingMarkPayload(code, kind, origin)),
    onSuccess: () => {
      setCode("fbk_book_01")
      setKind("booking")
      setOrigin("fixture://ferry-booking-mark/")
      void queryClient.invalidateQueries({ queryKey: ["ferry-booking-board", organizationId] })
    },
  })

  function onSave(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (organizationId) write.mutate()
  }

  return (
    <form className="flex max-w-lg flex-col gap-4" data-ferry-booking-mark="compose" onSubmit={onSave}>
      <p className="text-sm text-muted-foreground">
        Rezerwację promu zapisujesz jako stance katalogu. Bilet z portalu nie wchodzi do tego wiersza.
      </p>
      <label className="flex flex-col gap-1 text-sm">
        Kod rezerwacji (snake 2–32)
        <input
          aria-label="Kod znacznika rezerwacji promu"
          className="h-9 rounded border px-2 font-mono"
          onChange={(event) => setCode(event.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-sm">
        Rodzaj rezerwacji
        <select
          aria-label="Rodzaj rezerwacji promu"
          className="h-9 rounded border bg-background px-2"
          onChange={(event) => setKind(event.target.value)}
          value={kind}
        >
          {BOOKING_KINDS.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://ferry-booking-mark/…)"
        ariaLabel="Pochodzenie znacznika rezerwacji promu"
        value={origin}
        onChange={setOrigin}
      />
      {write.error ? <CatalogError error={write.error} /> : null}
      <button
        className="h-9 rounded border px-3 text-sm"
        disabled={!organizationId || write.isPending}
        type="submit"
      >
        Dodaj stance rezerwacji
      </button>
    </form>
  )
}
