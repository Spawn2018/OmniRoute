import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listSkontoMarks, persistSkontoMark, skontoWrite } from "@/lib/cash-discounts-api"

type SkontoDraft = {
  invoiceStamp: string
  kindStamp: string
  originStamp: string
}

const EMPTY_PAPER: SkontoDraft = {
  invoiceStamp: "",
  kindStamp: "skonto",
  originStamp: "fixture://cash-discount/",
}

function SkontoSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_PAPER)
  const persist = useMutation({
    mutationFn: () => persistSkontoMark(skontoWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_PAPER })
      void cache.invalidateQueries({ queryKey: ["skonto-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-cash-discount="paper-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Rodzaj skonta przy fakturze sprzedaży. Kwota i CAMT zostają leftover. Marża zostaje na
        `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Faktura (sales_invoice_id)
        <input
          aria-label="Identyfikator faktury skonta"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.invoiceStamp}
          onChange={(change) => setDraft({ ...draft, invoiceStamp: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj skonta (snake)
        <input
          aria-label="Rodzaj skonta"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindStamp}
          onChange={(change) => setDraft({ ...draft, kindStamp: change.target.value })}
          required
        />
      </label>
      <p className="text-xs text-muted-foreground">
        source_ref: tenant:manual albo fixture://cash-discount/…
      </p>
      <input
        aria-label="source_ref skonta"
        className="h-9 max-w-lg rounded-md border bg-background px-2 font-mono text-xs"
        value={draft.originStamp}
        onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
        required
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz skonto
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function SkontoRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["skonto-marks", args.organizationId],
    queryFn: listSkontoMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-cash-discount="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.discount_kind}
          </li>
        ))}
      </ul>
    </>
  )
}

export function SkontoPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <SkontoSave organizationId={args.organizationId} />
      <SkontoRows organizationId={args.organizationId} />
    </div>
  )
}
