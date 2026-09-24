import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  ResolveTokenForm,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  createDangerousGood,
  dangerousGoodCreateBody,
  fetchDangerousGoods,
  resolveDangerousGood,
  type DangerousGood,
} from "@/lib/dangerous-goods-api"
import { getTenantContext } from "@/lib/tenant"

const TUNNELS = ["A", "B", "C", "D", "E"] as const
const GROUPS = ["none", ...Array.from({ length: 18 }, (_, index) => `sg${index + 1}`)]
const PACKING = ["I", "II", "III"] as const

const helper = createColumnHelper<DangerousGood>()

const columns = [
  helper.accessor("un_number", {
    header: "Numer UN",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  helper.accessor("imdg_class", {
    header: "Klasa IMDG",
    cell: (info) => info.getValue(),
  }),
  helper.accessor("adr_tunnel_code", { header: "Tunel ADR" }),
  helper.accessor("segregation_group", { header: "Grupa SG" }),
  helper.accessor("packing_group", { header: "Grupa pakowania" }),
  helper.accessor("marine_pollutant", {
    header: "MP",
    cell: (info) => (info.getValue() ? "tak" : "nie"),
  }),
  helper.accessor("limited_quantity", {
    header: "LQ",
    cell: (info) => (info.getValue() ? "tak" : "nie"),
  }),
  helper.accessor("name", { header: "Nazwa ładunku" }),
  helper.accessor("aliases", {
    header: "Aliasy UN",
    cell: (info) => info.getValue().join(" · ") || "brak",
  }),
  helper.accessor("source_ref", { header: "Źródło" }),
]

const COLUMN_LABELS = {
  un_number: "Numer UN",
  imdg_class: "Klasa IMDG",
  adr_tunnel_code: "Tunel ADR",
  segregation_group: "Grupa SG",
  packing_group: "Grupa pakowania",
  marine_pollutant: "Zanieczyszczenie morza",
  limited_quantity: "Limited quantity",
  name: "Nazwa ładunku",
  aliases: "Aliasy UN",
  source_ref: "Źródło",
}

export function DangerousGoodCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [unNumber, setUnNumber] = useState("")
  const [imdgClass, setImdgClass] = useState("")
  const [name, setName] = useState("")
  const [aliasesText, setAliasesText] = useState("")
  const [tunnelCode, setTunnelCode] = useState("D")
  const [segregationGroup, setSegregationGroup] = useState("none")
  const [packingGroup, setPackingGroup] = useState("II")
  const [marinePollutant, setMarinePollutant] = useState(false)
  const [limitedQuantity, setLimitedQuantity] = useState(false)
  const [resolved, setResolved] = useState<DangerousGood | null>(null)
  const sessionReady = Boolean(ctx.organizationId && ctx.userId)

  const query = useQuery({
    queryKey: ["dangerous-goods", ctx.organizationId],
    queryFn: fetchDangerousGoods,
    enabled: sessionReady,
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () =>
      createDangerousGood(
        dangerousGoodCreateBody({
          unNumber,
          imdgClass,
          name,
          aliasesText,
          tunnelCode,
          segregationGroup,
          packingGroup,
          marinePollutant,
          limitedQuantity,
        }),
      ),
    onSuccess: () => {
      setUnNumber("")
      setImdgClass("")
      setName("")
      setAliasesText("")
      setTunnelCode("D")
      setSegregationGroup("none")
      setPackingGroup("II")
      setMarinePollutant(false)
      setLimitedQuantity(false)
      void queryClient.invalidateQueries({ queryKey: ["dangerous-goods", ctx.organizationId] })
    },
  })

  const resolveMutation = useMutation({
    mutationFn: resolveDangerousGood,
    onSuccess: setResolved,
    onError: () => setResolved(null),
  })

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Katalog towarów niebezpiecznych"
        subtitle="dangerous_good M-52 · UN + IMDG + tunel ADR + SG + packing + MP + LQ · nie klasa z modelu"
      />

      {sessionReady ? null : <TenantSessionNotice />}

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 lg:grid lg:grid-cols-10"
        onSubmit={(event) => {
          event.preventDefault()
          if (!sessionReady) return
          createMutation.mutate()
        }}
      >
        <Input
          aria-label="Numer UN"
          placeholder="1203"
          maxLength={6}
          value={unNumber}
          onChange={(event) => setUnNumber(event.target.value)}
          required
        />
        <Input
          aria-label="Klasa IMDG"
          placeholder="3"
          maxLength={3}
          value={imdgClass}
          onChange={(event) => setImdgClass(event.target.value)}
          required
        />
        <select
          aria-label="Tunel ADR"
          className="h-8 rounded-md border border-input bg-background px-2 text-xs"
          value={tunnelCode}
          onChange={(event) => setTunnelCode(event.target.value)}
        >
          {TUNNELS.map((code) => (
            <option key={code} value={code}>
              {code}
            </option>
          ))}
        </select>
        <select
          aria-label="Grupa SG"
          className="h-8 rounded-md border border-input bg-background px-2 text-xs"
          value={segregationGroup}
          onChange={(event) => setSegregationGroup(event.target.value)}
        >
          {GROUPS.map((group) => (
            <option key={group} value={group}>
              {group}
            </option>
          ))}
        </select>
        <select
          aria-label="Grupa pakowania"
          className="h-8 rounded-md border border-input bg-background px-2 text-xs"
          value={packingGroup}
          onChange={(event) => setPackingGroup(event.target.value)}
        >
          {PACKING.map((group) => (
            <option key={group} value={group}>
              {group}
            </option>
          ))}
        </select>
        <label className="flex h-8 items-center gap-2 text-xs">
          <input
            type="checkbox"
            aria-label="Zanieczyszczenie morza"
            checked={marinePollutant}
            onChange={(event) => setMarinePollutant(event.target.checked)}
          />
          MP
        </label>
        <label className="flex h-8 items-center gap-2 text-xs">
          <input
            type="checkbox"
            aria-label="Limited quantity"
            checked={limitedQuantity}
            onChange={(event) => setLimitedQuantity(event.target.checked)}
          />
          LQ
        </label>
        <Input
          aria-label="Nazwa ładunku"
          placeholder="Benzyna"
          value={name}
          onChange={(event) => setName(event.target.value)}
          required
        />
        <Input
          aria-label="Aliasy UN"
          placeholder="1213"
          value={aliasesText}
          onChange={(event) => setAliasesText(event.target.value)}
        />
        <Button type="submit" disabled={createMutation.isPending || !sessionReady}>
          Dodaj towar
        </Button>
      </form>

      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}

      <ResolveTokenForm
        label="Sprawdź numer UN"
        placeholder="1203 albo alias"
        pending={resolveMutation.isPending}
        resolved={
          resolved === null
            ? null
            : `UN${resolved.un_number} · klasa ${resolved.imdg_class} · PG ${resolved.packing_group} · MP ${resolved.marine_pollutant ? "tak" : "nie"} · LQ ${resolved.limited_quantity ? "tak" : "nie"} · tunel ${resolved.adr_tunnel_code} · ${resolved.name}`
        }
        onResolve={(token) => resolveMutation.mutate(token)}
      />

      {resolveMutation.isError ? <CatalogError error={resolveMutation.error} /> : null}

      <CatalogLoadedTable
        data={query.data}
        columns={columns}
        columnLabels={COLUMN_LABELS}
        tableKey={BUSINESS_LISTS.dangerousGoods.tableKey}
        globalFilterPlaceholder="Szukaj numeru UN albo klasy…"
        loading={query.isLoading}
        error={query.error}
      />
    </div>
  )
}
