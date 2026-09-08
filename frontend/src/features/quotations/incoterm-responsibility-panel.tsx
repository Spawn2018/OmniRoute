import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  fetchIncotermResponsibilities,
  incotermResponsibilityBody,
  saveIncotermResponsibility,
  seedOmniIncotermResponsibilities,
} from "@/lib/incoterm-responsibilities-api"
import { getTenantContext } from "@/lib/tenant"

const INCOTERMS = ["EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"]
const ROLES = ["seller", "buyer", "omni_customs", "origin_agent", "client_customs"] as const
const SCOPES = ["precarriage", "ocean", "oncarriage", "contact_exchange", "none"] as const

function TokenSelect(args: {
  caption: string
  value: string
  options: readonly string[]
  onPick: (token: string) => void
}) {
  return (
    <label className="flex flex-col gap-1 text-xs">
      {args.caption}
      <select
        aria-label={args.caption}
        className="h-8 rounded-md border border-border bg-card px-2 text-sm"
        value={args.value}
        onChange={(event) => args.onPick(event.target.value)}
      >
        {args.options.map((token) => (
          <option key={token} value={token}>
            {token}
          </option>
        ))}
      </select>
    </label>
  )
}

export function IncotermResponsibilityPanel(args: { signedIn: boolean }) {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [incoterm, setIncoterm] = useState("DDP")
  const [tradeSide, setTradeSide] = useState("import")
  const [exportRole, setExportRole] = useState("seller")
  const [importRole, setImportRole] = useState("seller")
  const [booker, setBooker] = useState("seller")
  const [scope, setScope] = useState<string[]>(["ocean", "oncarriage"])
  const listQuery = useQuery({
    queryKey: ["incoterm-responsibilities", ctx.organizationId, incoterm, tradeSide],
    queryFn: () => fetchIncotermResponsibilities({ incoterm, tradeSide }),
    enabled: args.signedIn,
    retry: false,
  })
  const saveMutation = useMutation({
    mutationFn: () =>
      saveIncotermResponsibility(
        incotermResponsibilityBody({
          incoterm,
          tradeSide,
          exportClearanceRole: exportRole,
          importClearanceRole: importRole,
          mainCarriageBooker: booker,
          bookingScope: scope,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["incoterm-responsibilities", ctx.organizationId, incoterm, tradeSide],
      })
    },
  })
  const seedMutation = useMutation({
    mutationFn: () => seedOmniIncotermResponsibilities(),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["incoterm-responsibilities", ctx.organizationId],
      })
    },
  })
  const busy = !args.signedIn || saveMutation.isPending || seedMutation.isPending
  return (
    <section className="space-y-2 rounded-md border border-border bg-card p-3" data-incoterm-responsibility="job">
      <p className="text-sm font-medium">Macierz obowiązków Incoterms</p>
      <p className="text-xs text-muted-foreground">
        Para incoterm × strona. Seed Omni nie cytuje tabeli izby. Override = nowy wiersz.
      </p>
      <div className="flex flex-col gap-2 md:flex-row md:flex-wrap">
        <TokenSelect caption="incoterm" value={incoterm} options={INCOTERMS} onPick={setIncoterm} />
        <TokenSelect
          caption="trade_side"
          value={tradeSide}
          options={["import", "export"]}
          onPick={setTradeSide}
        />
        <TokenSelect caption="export_clearance_role" value={exportRole} options={ROLES} onPick={setExportRole} />
        <TokenSelect caption="import_clearance_role" value={importRole} options={ROLES} onPick={setImportRole} />
        <TokenSelect caption="main_carriage_booker" value={booker} options={["seller", "buyer"]} onPick={setBooker} />
        <Button type="button" disabled={busy} onClick={() => saveMutation.mutate()}>
          Zapisz override
        </Button>
        <Button type="button" disabled={busy} onClick={() => seedMutation.mutate()}>
          Seed Omni 11×2
        </Button>
      </div>
      <fieldset className="flex flex-wrap gap-2 text-xs">
        <legend>booking_scope</legend>
        {SCOPES.map((token) => (
          <label key={token} className="flex items-center gap-1">
            <input
              type="checkbox"
              aria-label={token}
              checked={scope.includes(token)}
              onChange={(event) => {
                if (event.target.checked) {
                  setScope([...scope, token])
                  return
                }
                setScope(scope.filter((kept) => kept !== token))
              }}
            />
            {token}
          </label>
        ))}
      </fieldset>
      {saveMutation.isError ? (
        <p className="text-sm text-destructive">{(saveMutation.error as Error).message}</p>
      ) : null}
      {seedMutation.isError ? (
        <p className="text-sm text-destructive">{(seedMutation.error as Error).message}</p>
      ) : null}
      {(listQuery.data ?? []).map((row) => (
        <p key={row.id} className="font-mono text-xs">
          {row.incoterm} {row.trade_side} import={row.import_clearance_role} booker={row.main_carriage_booker}{" "}
          {row.booking_scope.join(",")}
        </p>
      ))}
    </section>
  )
}
