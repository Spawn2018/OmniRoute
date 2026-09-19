import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { fetchResourceDocuments, saveResourceDocument } from "@/lib/resource-documents-api"
import { getTenantContext } from "@/lib/tenant"

const KINDS = [
  { token: "licence", label: "licencja" },
  { token: "insurance", label: "ubezpieczenie" },
  { token: "other", label: "inne" },
] as const

export function ResourceDocumentPanel(args: { signedIn: boolean }) {
  const ctx = getTenantContext()
  const cache = useQueryClient()
  const [resourceId, setResourceId] = useState("")
  const [documentKind, setDocumentKind] = useState("licence")
  const [validUntil, setValidUntil] = useState("")
  const listed = useQuery({
    queryKey: ["resource-documents", ctx.organizationId],
    queryFn: () => fetchResourceDocuments(),
    enabled: args.signedIn,
    retry: false,
  })
  const persist = useMutation({
    mutationFn: () => saveResourceDocument({ resourceId, documentKind, validUntil }),
    onSuccess: () => {
      void cache.invalidateQueries({ queryKey: ["resource-documents", ctx.organizationId] })
    },
  })
  return (
    <section className="grid gap-2 rounded-md border border-border p-3" data-resource="document">
      <h2 className="text-sm font-medium">Ważność dokumentów floty</h2>
      <p className="text-xs text-muted-foreground">
        Data HITL na zasobie. Nie odliczanie. Nie dokument kontrahenta.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Identyfikator zasobu
        <Input
          aria-label="Identyfikator zasobu floty"
          placeholder="resource_id"
          value={resourceId}
          onChange={(event) => setResourceId(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj dokumentu
        <select
          aria-label="Rodzaj dokumentu floty"
          className="h-8 rounded-md border border-border bg-background px-2 text-sm"
          value={documentKind}
          onChange={(event) => setDocumentKind(event.target.value)}
        >
          {KINDS.map((entry) => (
            <option key={entry.token} value={entry.token}>
              {entry.label}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Ważne do
        <Input
          aria-label="Data ważności dokumentu"
          placeholder="valid_until"
          value={validUntil}
          onChange={(event) => setValidUntil(event.target.value)}
        />
      </label>
      <Button
        type="button"
        disabled={
          !args.signedIn || resourceId.trim() === "" || validUntil.trim() === "" || persist.isPending
        }
        onClick={() => persist.mutate()}
      >
        Zapisz ważność
      </Button>
      {persist.isError ? <p className="text-sm text-destructive">{(persist.error as Error).message}</p> : null}
      <ul className="space-y-1">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.document_kind} · {row.valid_until}
          </li>
        ))}
      </ul>
    </section>
  )
}
