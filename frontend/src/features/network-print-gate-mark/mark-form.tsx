import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  buildNetworkPrintGateMarkWrite,
  saveNetworkPrintGateMark,
} from "@/lib/network-print-gate-marks-api"

const GATE_OPTIONS = ["block_409", "warn_only", "record_only", "other"] as const

export function NetworkPrintGateMarkSave(args: { organizationId: string | null }) {
  const cache = useQueryClient()
  const [code, setCode] = useState("gate_block_01")
  const [kind, setKind] = useState<string>("block_409")
  const [ref, setRef] = useState("fixture://network-print-gate/")
  const save = useMutation({
    mutationFn: () =>
      saveNetworkPrintGateMark(buildNetworkPrintGateMarkWrite(code, kind, ref)),
    onSuccess: () => {
      setCode("gate_block_01")
      setKind("block_409")
      setRef("fixture://network-print-gate/")
      void cache.invalidateQueries({
        queryKey: ["network-print-gate-marks", args.organizationId],
      })
    },
  })

  return (
    <form
      className="flex max-w-lg flex-col gap-3"
      data-network-print-gate-mark="form"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (args.organizationId) save.mutate()
      }}
    >
      <p className="text-xs text-muted-foreground">
        Stance bramy wydruku sieci jako dana HITL — nie live 409 i nie PDF.
      </p>
      <label className="grid gap-1 text-xs">
        Kod (snake 2–32)
        <input
          aria-label="Kod bramy wydruku sieci"
          className="h-9 rounded-md border bg-background px-2 font-mono"
          onChange={(change) => setCode(change.target.value)}
          required
          value={code}
        />
      </label>
      <fieldset className="grid gap-2 text-xs">
        <legend>gate_kind</legend>
        {GATE_OPTIONS.map((token) => (
          <label key={token} className="flex items-center gap-2">
            <input
              checked={kind === token}
              name="network-print-gate-kind"
              onChange={() => setKind(token)}
              type="radio"
              value={token}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <CatalogSourceRefField
        label="source_ref (tenant:manual albo fixture://network-print-gate/…)"
        ariaLabel="Pochodzenie bramy wydruku sieci"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!args.organizationId || save.isPending} type="submit">
        Zapisz bramę wydruku sieci
      </Button>
    </form>
  )
}
