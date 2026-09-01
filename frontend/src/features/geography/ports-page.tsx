import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  ResolveTokenForm,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Money } from "@/components/money"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  EMPTY_SURCHARGE_DRAFT,
  createPortSurcharge,
  fetchPortSurcharges,
  portSurchargeCreateBody,
} from "@/lib/port-surcharges-api"
import {
  createPort,
  fetchPorts,
  portCreateBody,
  resolvePort,
  type Port,
} from "@/lib/ports-api"
import { getTenantContext } from "@/lib/tenant"

const columnHelper = createColumnHelper<Port>()

const columns = [
  columnHelper.accessor("unlocode", {
    id: "unlocode",
    header: "UN/LOCODE",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("name", {
    id: "name",
    header: "Nazwa",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("country_code", {
    id: "country_code",
    header: "Kraj",
    cell: (info) => <span className="font-mono text-xs">{info.getValue()}</span>,
  }),
  columnHelper.accessor("function_flags", {
    id: "function_flags",
    header: "Funkcje",
    cell: (info) => info.getValue().join(", ") || "—",
  }),
  columnHelper.accessor("aliases", {
    id: "aliases",
    header: "Aliasy",
    cell: (info) => info.getValue().join(", ") || "—",
  }),
  columnHelper.accessor("is_official", {
    id: "is_official",
    header: "Pochodzenie",
    cell: (info) => (info.getValue() ? "UN/LOCODE" : "własny"),
  }),
  columnHelper.accessor("wpi_number", {
    id: "wpi_number",
    header: "WPI",
    cell: (info) => info.getValue() ?? "—",
  }),
  columnHelper.accessor("harbor_size", {
    id: "harbor_size",
    header: "Wielkość",
    cell: (info) => info.getValue() ?? "—",
  }),
  columnHelper.accessor("harbor_type", {
    id: "harbor_type",
    header: "Typ",
    cell: (info) => info.getValue() ?? "—",
  }),
  columnHelper.accessor("shelter", {
    id: "shelter",
    header: "Schronienie",
    cell: (info) => info.getValue() ?? "—",
  }),
]

const COLUMN_LABELS = {
  unlocode: "UN/LOCODE",
  name: "Nazwa",
  country_code: "Kraj",
  function_flags: "Funkcje",
  aliases: "Aliasy",
  is_official: "Pochodzenie",
  wpi_number: "WPI",
  harbor_size: "Wielkość",
  harbor_type: "Typ",
  shelter: "Schronienie",
}

export function PortCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [search, setSearch] = useState("")
  const [unlocode, setUnlocode] = useState("")
  const [name, setName] = useState("")
  const [countryCode, setCountryCode] = useState("")
  const [aliasesText, setAliasesText] = useState("")
  const [resolved, setResolved] = useState<Port | null>(null)
  const [surchargeDraft, setSurchargeDraft] = useState(EMPTY_SURCHARGE_DRAFT)

  const query = useQuery({
    queryKey: ["ports", ctx.organizationId, search],
    queryFn: () => fetchPorts(search),
    enabled: Boolean(ctx.organizationId && ctx.userId),
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () => createPort(portCreateBody({ unlocode, name, countryCode, aliasesText })),
    onSuccess: () => {
      setUnlocode("")
      setName("")
      setCountryCode("")
      setAliasesText("")
      void queryClient.invalidateQueries({ queryKey: ["ports", ctx.organizationId] })
    },
  })

  const extrasQuery = useQuery({
    queryKey: ["port-surcharges", ctx.organizationId],
    queryFn: fetchPortSurcharges,
    enabled: Boolean(ctx.organizationId && ctx.userId && resolved),
    retry: false,
  })

  const extraMutation = useMutation({
    mutationFn: () =>
      createPortSurcharge(
        portSurchargeCreateBody({ ...surchargeDraft, portId: resolved?.id ?? "" }),
      ),
    onSuccess: () => {
      setSurchargeDraft(EMPTY_SURCHARGE_DRAFT)
      void queryClient.invalidateQueries({ queryKey: ["port-surcharges", ctx.organizationId] })
    },
  })

  const resolveMutation = useMutation({
    mutationFn: (token: string) => resolvePort(token),
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
        title="Katalog portów"
        subtitle="port M-05 · UN/LOCODE per tenant, nie luźna nazwa miejscowości"
      />

      {!ctx.organizationId || !ctx.userId ? <TenantSessionNotice /> : null}

      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-5"
        onSubmit={(event) => {
          event.preventDefault()
          createMutation.mutate()
        }}
      >
        <Input
          aria-label="Kod UN/LOCODE"
          placeholder="PLGDY"
          value={unlocode}
          onChange={(event) => setUnlocode(event.target.value)}
          required
        />
        <Input
          aria-label="Nazwa portu"
          placeholder="Gdynia"
          value={name}
          onChange={(event) => setName(event.target.value)}
          required
        />
        <Input
          aria-label="Kod kraju"
          placeholder="PL"
          value={countryCode}
          onChange={(event) => setCountryCode(event.target.value)}
          required
        />
        <Input
          aria-label="Aliasy portu"
          placeholder="Gdingen, Gdynia Port"
          value={aliasesText}
          onChange={(event) => setAliasesText(event.target.value)}
        />
        <Button type="submit" disabled={createMutation.isPending || !ctx.organizationId}>
          Dodaj port
        </Button>
      </form>

      {createMutation.isError ? <CatalogError error={createMutation.error} /> : null}

      <ResolveTokenForm
        label="Sprawdź token portu"
        placeholder="Gdingen"
        pending={resolveMutation.isPending}
        resolved={resolved === null ? null : `${resolved.unlocode} · ${resolved.name}`}
        onResolve={(token) => resolveMutation.mutate(token)}
      />

      {resolveMutation.isError ? <CatalogError error={resolveMutation.error} /> : null}

      {resolved ? (
        <fieldset className="space-y-2 rounded-md border border-border p-3">
          <legend className="text-sm font-medium">
            Extra portowe {resolved.unlocode}
          </legend>
          <form
            className="grid gap-2 md:grid-cols-3"
            onSubmit={(event) => {
              event.preventDefault()
              extraMutation.mutate()
            }}
          >
            <Input
              aria-label="Kod extra panelu"
              placeholder="thc"
              value={surchargeDraft.code}
              onChange={(event) =>
                setSurchargeDraft({ ...surchargeDraft, code: event.target.value })
              }
              required
            />
            <Input
              aria-label="Tytuł extra panelu"
              placeholder="THC weekend"
              value={surchargeDraft.title}
              onChange={(event) =>
                setSurchargeDraft({ ...surchargeDraft, title: event.target.value })
              }
              required
            />
            <Input
              aria-label="Warunek extra panelu"
              placeholder="kontener 40HC w weekend"
              value={surchargeDraft.appliesWhen}
              onChange={(event) =>
                setSurchargeDraft({ ...surchargeDraft, appliesWhen: event.target.value })
              }
              required
            />
            <Input
              aria-label="Kwota extra panelu"
              placeholder="85.0000"
              inputMode="decimal"
              value={surchargeDraft.amount}
              onChange={(event) =>
                setSurchargeDraft({ ...surchargeDraft, amount: event.target.value })
              }
              required
            />
            <Input
              aria-label="Waluta extra panelu"
              placeholder="EUR"
              maxLength={3}
              value={surchargeDraft.currency}
              onChange={(event) =>
                setSurchargeDraft({ ...surchargeDraft, currency: event.target.value })
              }
              required
            />
            <Button type="submit" disabled={extraMutation.isPending}>
              Dodaj extra
            </Button>
          </form>
          {extraMutation.isError ? <CatalogError error={extraMutation.error} /> : null}
          <ul className="text-xs">
            {extrasQuery.data
              ?.filter((row) => row.port_id === resolved.id)
              .map((row) => (
                <li key={row.id} className="flex items-center gap-2">
                  <span className="font-mono">{row.code}</span>
                  <span>{row.title}</span>
                  <Money amount={row.amount} currency={row.currency} />
                </li>
              ))}
          </ul>
        </fieldset>
      ) : null}

      <form
        className="flex gap-2 rounded-md border border-border bg-card p-3"
        onSubmit={(event) => {
          event.preventDefault()
          void query.refetch()
        }}
      >
        <Input
          aria-label="Szukaj portu w bazie"
          placeholder="szukaj po kodzie albo nazwie"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <Button type="submit" variant="outline">
          Szukaj
        </Button>
      </form>

      {query.isLoading ? <div className="text-sm text-muted-foreground">Ładowanie…</div> : null}

      {query.isError ? <CatalogError error={query.error} /> : null}

      {query.data ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.ports.tableKey}
          columns={columns}
          data={query.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Filtruj pobrane porty…"
        />
      ) : null}
    </div>
  )
}
