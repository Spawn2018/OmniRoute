import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  EMPTY_SURCHARGE_DRAFT,
  createPortSurcharge,
  fetchPortSurcharges,
  matchPortSurcharges,
  portSurchargeCreateBody,
  resolvePortSurcharge,
  type PortSurcharge,
} from "@/lib/port-surcharges-api"
import { getTenantContext } from "@/lib/tenant"

const columnHelper = createColumnHelper<PortSurcharge>()

const columns = [
  columnHelper.accessor("port_id", {
    id: "port_id",
    header: "Port",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("code", {
    id: "code",
    header: "Kod",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("title", {
    id: "title",
    header: "Tytuł",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("applies_when", {
    id: "applies_when",
    header: "Warunek",
    cell: (info) => info.getValue(),
  }),
  columnHelper.display({
    id: "amount",
    header: "Kwota",
    cell: (info) => (
      <Money amount={info.row.original.amount} currency={info.row.original.currency} />
    ),
  }),
  columnHelper.accessor("source_ref", {
    id: "source_ref",
    header: "Pochodzenie",
    cell: (info) => info.getValue(),
  }),
]

const COLUMN_LABELS = {
  port_id: "Port",
  code: "Kod extra",
  title: "Tytuł",
  applies_when: "Warunek",
  amount: "Kwota",
  source_ref: "source_ref",
}

export function PortSurchargeCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [draft, setDraft] = useState(EMPTY_SURCHARGE_DRAFT)
  const [lookupPortId, setLookupPortId] = useState("")
  const [lookupCode, setLookupCode] = useState("")
  const [resolved, setResolved] = useState<PortSurcharge | null>(null)
  const [matchPortId, setMatchPortId] = useState("")
  const [matchWhen, setMatchWhen] = useState("")
  const [matched, setMatched] = useState<PortSurcharge[]>([])
  const sessionReady = Boolean(ctx.organizationId && ctx.userId)

  const query = useQuery({
    queryKey: ["port-surcharges", ctx.organizationId],
    queryFn: fetchPortSurcharges,
    enabled: sessionReady,
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () => createPortSurcharge(portSurchargeCreateBody(draft)),
    onSuccess: () => {
      setDraft(EMPTY_SURCHARGE_DRAFT)
      void queryClient.invalidateQueries({ queryKey: ["port-surcharges", ctx.organizationId] })
    },
  })

  const matchMutation = useMutation({
    mutationFn: () => matchPortSurcharges(matchPortId.trim(), matchWhen.trim()),
    onSuccess: (rows) => {
      setMatched(rows)
    },
    onError: () => {
      setMatched([])
    },
  })

  const resolveMutation = useMutation({
    mutationFn: () => resolvePortSurcharge(lookupPortId.trim(), lookupCode.trim()),
    onSuccess: (row) => {
      setResolved(row)
    },
    onError: () => {
      setResolved(null)
    },
  })

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Opłaty portowe warunkowe"
        subtitle="port_surcharge M-18 · katalog extra · warunek to dane · nie marża charge"
      />
      {sessionReady ? null : <TenantSessionNotice />}
      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 lg:grid-cols-3"
        onSubmit={(event) => {
          event.preventDefault()
          if (sessionReady) createMutation.mutate()
        }}
      >
        <Input
          aria-label="Identyfikator portu extra"
          placeholder="port_id"
          value={draft.portId}
          onChange={(event) => setDraft({ ...draft, portId: event.target.value })}
          required
        />
        <Input
          aria-label="Kod extra"
          placeholder="thc"
          value={draft.code}
          onChange={(event) => setDraft({ ...draft, code: event.target.value })}
          required
        />
        <Input
          aria-label="Tytuł extra"
          placeholder="THC weekend"
          value={draft.title}
          onChange={(event) => setDraft({ ...draft, title: event.target.value })}
          required
        />
        <Input
          aria-label="Warunek extra"
          placeholder="kontener 40HC w weekend"
          value={draft.appliesWhen}
          onChange={(event) => setDraft({ ...draft, appliesWhen: event.target.value })}
          required
        />
        <Input
          aria-label="Kwota extra"
          placeholder="85.0000"
          inputMode="decimal"
          value={draft.amount}
          onChange={(event) => setDraft({ ...draft, amount: event.target.value })}
          required
        />
        <Input
          aria-label="Waluta extra"
          placeholder="EUR"
          maxLength={3}
          value={draft.currency}
          onChange={(event) => setDraft({ ...draft, currency: event.target.value })}
          required
        />
        <Button type="submit" disabled={createMutation.isPending || !sessionReady}>
          Dodaj extra
        </Button>
      </form>
      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}
      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-3"
        onSubmit={(event) => {
          event.preventDefault()
          resolveMutation.mutate()
        }}
      >
        <Input
          aria-label="Sprawdź port extra"
          placeholder="port_id"
          value={lookupPortId}
          onChange={(event) => setLookupPortId(event.target.value)}
        />
        <Input
          aria-label="Sprawdź kod extra"
          placeholder="thc"
          value={lookupCode}
          onChange={(event) => setLookupCode(event.target.value)}
        />
        <Button
          type="submit"
          variant="outline"
          disabled={resolveMutation.isPending || !lookupPortId || !lookupCode}
        >
          Rozwiąż
        </Button>
        {resolved ? (
          <div className="font-mono text-xs md:col-span-3">
            {resolved.code} · {resolved.title} · {resolved.amount} {resolved.currency}
          </div>
        ) : null}
      </form>
      {resolveMutation.isError ? <CatalogError error={resolveMutation.error} /> : null}
      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-3"
        onSubmit={(event) => {
          event.preventDefault()
          matchMutation.mutate()
        }}
      >
        <Input
          aria-label="Port do dopasowania extra"
          placeholder="port_id"
          value={matchPortId}
          onChange={(event) => setMatchPortId(event.target.value)}
        />
        <Input
          aria-label="Warunek applies_when"
          placeholder="kontener 40HC w weekend"
          value={matchWhen}
          onChange={(event) => setMatchWhen(event.target.value)}
        />
        <Button
          type="submit"
          variant="outline"
          disabled={matchMutation.isPending || !matchPortId || !matchWhen}
        >
          Dopasuj warunek
        </Button>
        <ul data-port-surcharge="matching" className="text-xs md:col-span-3">
          {matched.map((row) => (
            <li key={row.id}>
              {row.code} · {row.applies_when}{" "}
              <Money amount={row.amount} currency={row.currency} />
            </li>
          ))}
        </ul>
      </form>
      {matchMutation.isError ? <CatalogError error={matchMutation.error} /> : null}
      <CatalogLoadedTable
        tableKey={BUSINESS_LISTS.portSurcharges.tableKey}
        columns={columns}
        columnLabels={COLUMN_LABELS}
        data={query.data}
        loading={query.isLoading}
        error={query.error}
        globalFilterPlaceholder="Szukaj extra portowego…"
      />
    </div>
  )
}
