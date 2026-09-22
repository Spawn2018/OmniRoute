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
import { chargeCreateBody, createCharge, fetchChargeSellInPln, fetchCharges, fetchShipmentTreeMargins, type Charge, type ChargeSellInPln, type ShipmentTreeMargin } from "@/lib/charges-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<Charge>()

function moneyCell(amount: string, currency: string) {
  return <Money amount={amount} currency={currency} />
}

const columns = [
  helper.accessor("charge_code", { header: "Kod opłaty" }),
  helper.accessor("buy_amount", {
    header: "Kupno",
    cell: ({ row }) => moneyCell(row.original.buy_amount, row.original.buy_currency),
  }),
  helper.accessor("sell_amount", {
    header: "Sprzedaż",
    cell: ({ row }) => moneyCell(row.original.sell_amount, row.original.sell_currency),
  }),
  helper.accessor("margin_amount", {
    header: "Marża",
    cell: ({ row }) => moneyCell(row.original.margin_amount, row.original.margin_currency),
  }),
  helper.accessor("rate_line_id", {
    header: "Stawka kupna",
    cell: ({ getValue }) => getValue() ?? "—",
  }),
  helper.accessor("source_ref", {
    header: "Pochodzenie",
    cell: ({ getValue }) => getValue() ?? "—",
  }),
  helper.accessor("shipment_id", {
    header: "Zlecenie",
    cell: ({ getValue }) => getValue() ?? "—",
  }),
  helper.accessor("fx_rate_basis", {
    header: "Kurs data",
    cell: ({ getValue }) => getValue() ?? "—",
  }),
  helper.accessor("fx_rate_offset_days", {
    header: "Kurs offset",
    cell: ({ getValue }) => getValue() ?? "—",
  }),
  helper.accessor("fx_rate_table", {
    header: "Kurs tabela",
    cell: ({ getValue }) => getValue() ?? "—",
  }),
]

const treeHelper = createColumnHelper<ShipmentTreeMargin>()

const treeColumns = [
  treeHelper.accessor("shipment_id", { header: "Zlecenie główne" }),
  treeHelper.accessor("currency", { header: "Waluta" }),
  treeHelper.accessor("buy_amount", {
    header: "Kupno",
    cell: ({ row }) => moneyCell(row.original.buy_amount, row.original.currency),
  }),
  treeHelper.accessor("sell_amount", {
    header: "Sprzedaż",
    cell: ({ row }) => moneyCell(row.original.sell_amount, row.original.currency),
  }),
  treeHelper.accessor("margin_amount", {
    header: "Marża",
    cell: ({ row }) => moneyCell(row.original.margin_amount, row.original.currency),
  }),
  treeHelper.accessor("charge_count", { header: "Opłaty" }),
]

const TREE_LABELS = {
  shipment_id: "Zlecenie główne",
  currency: "Waluta",
  buy_amount: "Kupno",
  sell_amount: "Sprzedaż",
  margin_amount: "Marża",
  charge_count: "Opłaty",
}

const COLUMN_LABELS = {
  charge_code: "Kod opłaty",
  buy_amount: "Kupno",
  sell_amount: "Sprzedaż",
  margin_amount: "Marża",
  rate_line_id: "Stawka kupna",
  source_ref: "Pochodzenie",
  shipment_id: "Zlecenie",
  fx_rate_basis: "Kurs data",
  fx_rate_offset_days: "Kurs offset",
  fx_rate_table: "Kurs tabela",
}

type Draft = {
  chargeCode: string
  buyAmount: string
  sellAmount: string
  currency: string
  rateLineId: string
  sourceRef: string
  originUnlocode: string
  destinationUnlocode: string
  floorDecisionId: string
  shipmentId: string
  fxRateBasis: string
  fxRateOffsetDays: string
  fxRateTable: string
}

const EMPTY_DRAFT: Draft = {
  chargeCode: "",
  buyAmount: "",
  sellAmount: "",
  currency: "EUR",
  rateLineId: "",
  sourceRef: "",
  originUnlocode: "",
  destinationUnlocode: "",
  floorDecisionId: "",
  shipmentId: "",
  fxRateBasis: "",
  fxRateOffsetDays: "",
  fxRateTable: "",
}

function SellInPlnPanel({ signedIn }: { signedIn: boolean }) {
  const [chargeId, setChargeId] = useState("")
  const [onDate, setOnDate] = useState("2026-09-01")
  const [result, setResult] = useState<ChargeSellInPln | null>(null)
  const query = useQuery({
    queryKey: ["charge-sell-in-pln", chargeId, onDate],
    queryFn: () => fetchChargeSellInPln(chargeId.trim(), onDate.trim()),
    enabled: false,
    retry: false,
  })

  return (
    <aside className="space-y-2 rounded-md border border-border bg-card p-3" data-charge-sell-in-pln="panel">
      <p className="text-sm text-muted-foreground">
        Sprzedaż w PLN z kursu NBP w bazie — nie mnożenie w przeglądarce.
      </p>
      <div className="flex flex-col gap-2 md:flex-row md:flex-wrap">
        <Input
          aria-label="Identyfikator opłaty do PLN"
          placeholder="charge_id"
          value={chargeId}
          onChange={(event) => setChargeId(event.target.value)}
        />
        <Input
          aria-label="Data kursu NBP"
          type="date"
          value={onDate}
          onChange={(event) => setOnDate(event.target.value)}
        />
        <Button
          type="button"
          disabled={!signedIn || chargeId.trim() === "" || onDate.trim() === "" || query.isFetching}
          onClick={() => {
            void query.refetch().then((reply) => {
              if (reply.data !== undefined) {
                setResult(reply.data)
              }
            })
          }}
        >
          Policz sprzedaż w PLN
        </Button>
      </div>
      {query.isError ? <CatalogError error={query.error} /> : null}
      {result !== null ? (
        <p className="text-sm" data-sell-amount-pln={result.sell_amount_pln}>
          {result.sell_amount_pln} {result.currency} · data {result.on_date}
        </p>
      ) : null}
    </aside>
  )
}

export function ChargeCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [draft, setDraft] = useState<Draft>(EMPTY_DRAFT)
  const signedIn = Boolean(ctx.organizationId && ctx.userId)

  const query = useQuery({
    queryKey: ["charges", ctx.organizationId],
    queryFn: fetchCharges,
    enabled: signedIn,
    retry: false,
  })

  const treeQuery = useQuery({
    queryKey: ["shipment-tree-margin", ctx.organizationId],
    queryFn: fetchShipmentTreeMargins,
    enabled: signedIn,
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () => createCharge(chargeCreateBody(draft)),
    onSuccess: () => {
      setDraft({ ...EMPTY_DRAFT, currency: draft.currency })
      void queryClient.invalidateQueries({ queryKey: ["charges", ctx.organizationId] })
    },
  })

  const setField = (field: keyof Draft) => (event: { target: { value: string } }) => {
    setDraft((current) => ({ ...current, [field]: event.target.value }))
  }

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Opłaty"
        subtitle="charge M-08 · buy i sell na jednym wierszu · marża w kodzie · UN opcjonalnie pod margin_floor · opcjonalne zlecenie · opcjonalny kurs · marża drzewa z SQL · sprzedaż w PLN liczy baza (kurs NBP) · nie accept HITL"
      />

      {signedIn ? null : <TenantSessionNotice />}

      <SellInPlnPanel signedIn={signedIn} />

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          createMutation.mutate()
        }}
      >
        <Input aria-label="Kod opłaty" placeholder="THC" value={draft.chargeCode} onChange={setField("chargeCode")} required />
        <Input aria-label="Kwota kupna" placeholder="10.5000" value={draft.buyAmount} onChange={setField("buyAmount")} required />
        <Input aria-label="Kwota sprzedaży" placeholder="14.0000" value={draft.sellAmount} onChange={setField("sellAmount")} required />
        <Input aria-label="Waluta ISO" placeholder="EUR" value={draft.currency} onChange={setField("currency")} required />
        <Input aria-label="UN/LOCODE origin" placeholder="PLGDY (opcjonalnie)" value={draft.originUnlocode} onChange={setField("originUnlocode")} />
        <Input aria-label="UN/LOCODE destination" placeholder="DEHAM (opcjonalnie)" value={draft.destinationUnlocode} onChange={setField("destinationUnlocode")} />
        <Input aria-label="Identyfikator decyzji podłogi" placeholder="floor_decision_id po S11" value={draft.floorDecisionId} onChange={setField("floorDecisionId")} />
        <Input aria-label="Identyfikator stawki kupna" placeholder="rate_line (opcjonalnie)" value={draft.rateLineId} onChange={setField("rateLineId")} />
        <Input aria-label="Zlecenie" placeholder="shipment_id (opcjonalnie)" value={draft.shipmentId} onChange={setField("shipmentId")} />
        <Input aria-label="Kurs data" placeholder="etd / loading_date…" value={draft.fxRateBasis} onChange={setField("fxRateBasis")} />
        <Input aria-label="Kurs offset" placeholder="0 albo -1" value={draft.fxRateOffsetDays} onChange={setField("fxRateOffsetDays")} />
        <Input aria-label="Kurs tabela" placeholder="nbp_a / nbp_b" value={draft.fxRateTable} onChange={setField("fxRateTable")} />
        <Input aria-label="Pochodzenie" placeholder="tenant:manual albo fixture://charge/…" value={draft.sourceRef} onChange={setField("sourceRef")} required />
        <Button type="submit" disabled={createMutation.isPending || !signedIn}>
          Dodaj opłatę
        </Button>
      </form>

      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}

      <CatalogLoadedTable
        loading={query.isLoading}
        error={query.error}
        data={query.data}
        tableKey={BUSINESS_LISTS.charges.tableKey}
        columns={columns}
        columnLabels={COLUMN_LABELS}
        globalFilterPlaceholder="Szukaj opłaty…"
      />

      <h2 className="text-sm font-medium">Marża drzewa</h2>
      <CatalogLoadedTable
        loading={treeQuery.isLoading}
        error={treeQuery.error}
        data={treeQuery.data}
        tableKey="shipment_tree_margin"
        columns={treeColumns}
        columnLabels={TREE_LABELS}
        globalFilterPlaceholder="Szukaj zlecenia…"
      />
    </div>
  )
}
