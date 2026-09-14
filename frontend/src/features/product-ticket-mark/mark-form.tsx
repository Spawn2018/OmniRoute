import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildProductTicketMarkWrite,
  saveProductTicketMark,
} from "@/lib/product-ticket-marks-api"

const KINDS = ["report", "triage", "owner_ok", "other"] as const

export function ProductTicketMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("pt_report_01")
  const [kind, setKind] = useState<string>("report")
  const [origin, setOrigin] = useState("fixture://product-ticket/")
  const save = useMutation({
    mutationFn: () =>
      saveProductTicketMark(
        buildProductTicketMarkWrite({ code, kind, origin }),
      ),
    onSuccess: () => {
      setCode("pt_report_01")
      setKind("report")
      setOrigin("fixture://product-ticket/")
      void cache.invalidateQueries({
        queryKey: ["product-ticket-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="grid max-w-xl gap-3"
      data-product-ticket-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL stancji ticketu produktu (report/triage/owner_ok). CAPA, auto-naprawa i operator_notice zostają poza tym katalogiem.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod znacznika ticketu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>Rodzaj ticketu</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2 font-mono">
            <input
              checked={kind === token}
              name="product-ticket-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://product-ticket/…)"
        ariaLabel="Pochodzenie znacznika ticketu"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik ticketu
      </Button>
    </form>
  )
}
