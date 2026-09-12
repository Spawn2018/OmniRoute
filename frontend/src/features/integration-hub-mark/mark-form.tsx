import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createIntegrationHubMark,
  makeIntegrationHubPayload,
} from "@/lib/integration-hub-marks-api"

const HUB_KINDS = [
  { key: "rest", tip: "REST" },
  { key: "soap", tip: "SOAP" },
  { key: "edi", tip: "EDI" },
  { key: "sftp", tip: "SFTP" },
  { key: "other", tip: "inny" },
] as const

export function HubProtocolComposer(props: { organizationId: string | null }) {
  const client = useQueryClient()
  const [code, setCode] = useState("hub_rest_01")
  const [kind, setKind] = useState("rest")
  const [ref, setRef] = useState("fixture://integration-hub-mark/")
  const save = useMutation({
    mutationFn: () =>
      createIntegrationHubMark(makeIntegrationHubPayload(code, kind, ref)),
    onSuccess: () => {
      setCode("hub_rest_01")
      setKind("rest")
      setRef("fixture://integration-hub-mark/")
      void client.invalidateQueries({
        queryKey: ["integration-hub-marks", props.organizationId],
      })
    },
  })

  return (
    <aside className="rounded-md border bg-muted/20 p-4" data-hub="protocol-composer">
      <h2 className="text-sm font-semibold tracking-tight">Protokół hubu (HITL)</h2>
      <p className="mb-4 text-xs text-muted-foreground">
        Znacznik abstrakcji protokołu. Bez live HTTP i bez Selenium.
      </p>
      <form
        className="flex flex-col gap-3"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          if (props.organizationId) save.mutate()
        }}
      >
        <label className="text-xs">
          mark_code
          <input
            aria-label="mark_code hub"
            className="mt-1 h-9 w-full rounded-md border bg-background px-2 font-mono text-sm"
            onChange={(e) => setCode(e.target.value)}
            required
            value={code}
          />
        </label>
        <label className="text-xs">
          hub_kind
          <select
            aria-label="hub_kind"
            className="mt-1 h-9 w-full rounded-md border bg-background px-2 text-sm"
            onChange={(e) => setKind(e.target.value)}
            value={kind}
          >
            {HUB_KINDS.map((row) => (
              <option key={row.key} value={row.key}>
                {row.key} — {row.tip}
              </option>
            ))}
          </select>
        </label>
        <CatalogSourceRefField
          label="source_ref"
          ariaLabel="source_ref hub"
          value={ref}
          onChange={setRef}
        />
        {save.error ? <CatalogError error={save.error} /> : null}
        <Button disabled={!props.organizationId || save.isPending} type="submit">
          Zapisz protokół hubu
        </Button>
      </form>
    </aside>
  )
}
