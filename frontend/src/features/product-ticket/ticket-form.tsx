import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildProductTicketWrite,
  saveProductTicket,
} from "@/lib/product-tickets-api"

const KINDS = ["report", "triage", "owner_ok", "other"] as const

export function ProductTicketSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("bug_login_01")
  const [title, setTitle] = useState("")
  const [body, setBody] = useState("")
  const [kind, setKind] = useState<string>("report")
  const [origin, setOrigin] = useState("fixture://product-ticket/")
  const save = useMutation({
    mutationFn: () =>
      saveProductTicket(
        buildProductTicketWrite({
          code,
          title,
          body,
          kind,
          origin,
        }),
      ),
    onSuccess: () => {
      setCode("bug_login_01")
      setTitle("")
      setBody("")
      setKind("report")
      setOrigin("fixture://product-ticket/")
      void cache.invalidateQueries({
        queryKey: ["product-tickets", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-4 border-l-2 border-amber-700/40 pl-4"
      data-product-ticket="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        HITL wpis zgłoszenia błędu programu. Auto-naprawa i CAPA zostają poza
        tym katalogiem.
      </p>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://product-ticket/…)"
        ariaLabel="Pochodzenie ticketu produktu"
        value={origin}
        onChange={setOrigin}
      />
      <label className="flex flex-col gap-1 text-xs">
        <span>Kod ticketu (snake 2–32)</span>
        <input
          aria-label="Kod ticketu produktu"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Tytul</span>
        <input
          aria-label="Tytul ticketu produktu"
          className="h-9 rounded-none border bg-background px-2 font-mono"
          onChange={(change) => setTitle(change.target.value)}
          required
          value={title}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        <span>Tresc</span>
        <textarea
          aria-label="Tresc ticketu produktu"
          className="min-h-20 rounded-none border bg-background px-2 py-1 font-mono"
          onChange={(change) => setBody(change.target.value)}
          required
          value={body}
        />
      </label>
      <fieldset className="flex flex-col gap-2 text-xs">
        <legend>Rodzaj</legend>
        {KINDS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="product-ticket-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            <span>{token}</span>
          </label>
        ))}
      </fieldset>
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz ticket produktu
      </Button>
    </form>
  )
}
