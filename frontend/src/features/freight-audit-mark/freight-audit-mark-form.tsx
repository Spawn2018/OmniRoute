import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { buildFreightAuditWrite, saveFreightAuditMark } from "@/lib/freight-audit-marks-api"

const KINDS = ["expected_vs_invoice", "expected_vs_charge"] as const

export function FreightAuditMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("audit_inv_01")
  const [kind, setKind] = useState<string>("expected_vs_invoice")
  const [origin, setOrigin] = useState("fixture://freight-audit-mark/")
  const save = useMutation({
    mutationFn: () =>
      saveFreightAuditMark(buildFreightAuditWrite({ code, kind, origin })),
    onSuccess: () => {
      setCode("audit_inv_01")
      setKind("expected_vs_invoice")
      setOrigin("fixture://freight-audit-mark/")
      void cache.invalidateQueries({
        queryKey: ["freight-audit-marks", args.organizationId],
      })
    },
  })
  return (
    <form
      className="grid max-w-xl gap-3"
      data-freight-audit-mark="write"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Rodzaj audytu frachtu jako katalog. Bez porównania do charge i bez drugiej marży.
      </p>
      <label className="grid gap-1 text-xs">
        Kod
        <input
          aria-label="Kod znacznika audytu frachtu"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <label className="grid gap-1 text-xs">
        Rodzaj audytu
        <select
          aria-label="Rodzaj audytu frachtu"
          className="h-9 rounded-md border bg-background px-2"
          onChange={(change) => setKind(change.target.value)}
          value={kind}
        >
          {KINDS.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://freight-audit-mark/…)"
        ariaLabel="Pochodzenie audytu frachtu"
        value={origin}
        onChange={setOrigin}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz znacznik audytu frachtu
      </Button>
    </form>
  )
}
