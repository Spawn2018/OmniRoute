import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { connectorWrite, listConnectorMarks, persistConnectorMark } from "@/lib/telematics-connectors-api"

type HubDraft = {
  kindStamp: string
  providerStamp: string
  originStamp: string
}

const EMPTY_HUB: HubDraft = {
  kindStamp: "external_api",
  providerStamp: "gbox",
  originStamp: "fixture://telematics-connector/",
}

const KINDS = ["omni_telematic", "external_api"] as const
const PROVIDERS = ["gbox", "ikol", "flotis", "wialon", "other"] as const

function ConnectorSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_HUB)
  const persist = useMutation({
    mutationFn: () => persistConnectorMark(connectorWrite(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_HUB })
      void cache.invalidateQueries({ queryKey: ["hub-marks", args.organizationId] })
    },
  })
  return (
    <form
      className="grid max-w-lg gap-3"
      data-telematics-connector="hub-form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) persist.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Reżim obserwacji (`omni_telematic` albo `external_api`) plus kod dostawcy. Poll, ciphertext i
        trzy dni robocze zostają leftover. Marża zostaje na `/charges`.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Reżim obserwacji (allowlista)
        <select
          aria-label="Reżim obserwacji GPS"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.kindStamp}
          onChange={(change) => setDraft({ ...draft, kindStamp: change.target.value })}
          required
        >
          {KINDS.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Dostawca katalogu (nie live API)
        <select
          aria-label="Dostawca konektora GPS"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.providerStamp}
          onChange={(change) => setDraft({ ...draft, providerStamp: change.target.value })}
          required
        >
          {PROVIDERS.map((token) => (
            <option key={token} value={token}>
              {token}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-1 text-xs">
        source_ref (tenant:manual albo fixture://telematics-connector/…)
        <input
          aria-label="source_ref konektora GPS"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          value={draft.originStamp}
          onChange={(change) => setDraft({ ...draft, originStamp: change.target.value })}
          required
        />
      </label>
      <Button type="submit" disabled={persist.isPending || !args.organizationId}>
        Zapisz konektor GPS
      </Button>
      {persist.isError ? <CatalogError error={persist.error} /> : null}
    </form>
  )
}

function ConnectorRows(args: { organizationId: string | null }) {
  const listed = useQuery({
    queryKey: ["hub-marks", args.organizationId],
    queryFn: listConnectorMarks,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <ul data-telematics-connector="rows" className="flex flex-col gap-1 text-xs">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono">
            {row.observation_kind} {row.provider_code}
          </li>
        ))}
      </ul>
    </>
  )
}

export function ConnectorPanel(args: { organizationId: string | null }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <ConnectorSave organizationId={args.organizationId} />
      <ConnectorRows organizationId={args.organizationId} />
    </div>
  )
}
