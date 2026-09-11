import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { idpConnectorWrite, persistIdpConnector } from "@/lib/idp-connectors-api"

type Auth0FixtureDraft = {
  markCode: string
  providerToken: string
  hostLabel: string
  originHint: string
}

const EMPTY_AUTH0: Auth0FixtureDraft = {
  markCode: "auth0_eu_desk",
  providerToken: "auth0",
  hostLabel: "",
  originHint: "fixture://auth0/",
}

export function IdpConnectorSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_AUTH0)
  const persist = useMutation({
    mutationFn: () => persistIdpConnector(idpConnectorWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_AUTH0 })
      void cache.invalidateQueries({ queryKey: ["idp-connectors", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-idp-connector="auth0-fixture-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Katalog fixture Auth0: kod i token `auth0`. To nie jest logowanie — JWT hello i
        hasło zostają na `/session`. Serwis nie woła JWKS ani Auth0.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Kod konektora IdP (snake 2–32)
        <input
          aria-label="Kod konektora IdP"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.markCode}
          onChange={(change) => setDraft({ ...draft, markCode: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Dostawca (auth0)
        <input
          aria-label="Token dostawcy IdP"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.providerToken}
          onChange={(change) => setDraft({ ...draft, providerToken: change.target.value })}
          required
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Domena publiczna (opcjonalny host, bez https)
        <input
          aria-label="Domena publiczna IdP"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.hostLabel}
          onChange={(change) => setDraft({ ...draft, hostLabel: change.target.value })}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://auth0/…)"
        ariaLabel="Pochodzenie konektora IdP"
        value={draft.originHint}
        onChange={(originHint) => setDraft({ ...draft, originHint })}
      />
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz konektor Auth0
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}
