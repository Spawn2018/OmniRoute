import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { kekMarkWrite, persistTenantContractKek } from "@/lib/tenant-contract-keks-api"

type KekMarkDraft = {
  markSlug: string
  wrapToken: string
  originRef: string
}

const EMPTY_MARK: KekMarkDraft = {
  markSlug: "desk_wrap_pl",
  wrapToken: "password",
  originRef: "fixture://kek/",
}

const WRAP_TOKENS = ["password", "kms"] as const

export function TenantContractKekSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_MARK)
  const persist = useMutation({
    mutationFn: () => persistTenantContractKek(kekMarkWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_MARK })
      void cache.invalidateQueries({ queryKey: ["kek-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-kek-mark="wrap-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Znacznik owijki: kod i token `password` albo `kms`. To nie jest klucz. Serwis nie
        woła KMS i nie przyjmuje hasła ani materiału.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kod znacznika KEK (snake 2–32)
        <input
          aria-label="Kod znacznika KEK"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.markSlug}
          onChange={(change) => setDraft({ ...draft, markSlug: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj owijki (token danych)
        <select
          aria-label="Rodzaj owijki"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.wrapToken}
          onChange={(change) => setDraft({ ...draft, wrapToken: change.target.value })}
        >
          {WRAP_TOKENS.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
      <label className="grid gap-1 text-xs">
        Pochodzenie (`tenant:manual` albo `fixture://kek/…`)
        <input
          aria-label="Pochodzenie znacznika KEK"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setDraft({ ...draft, originRef: change.target.value })}
          required
          value={draft.originRef}
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz znacznik KEK
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}
