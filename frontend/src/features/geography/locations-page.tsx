import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  addZoneMember,
  createZone,
  fetchLocations,
  fetchZoneMembers,
  resolvePostalCode,
  zoneCreateBody,
  zoneMemberCreateBody,
  type Location,
} from "@/lib/locations-api"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { getTenantContext } from "@/lib/tenant"

const KIND_LABELS: Record<string, string> = {
  postal_zone: "strefa pocztowa",
  unlocode: "port",
  address: "adres",
}

const columnHelper = createColumnHelper<Location>()

const columns = [
  columnHelper.accessor("code", {
    id: "code",
    header: "Kod",
    cell: (info) => <span className="font-mono text-xs">{info.getValue() ?? "—"}</span>,
  }),
  columnHelper.accessor("name", {
    id: "name",
    header: "Nazwa",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("kind", {
    id: "kind",
    header: "Rodzaj",
    cell: (info) => KIND_LABELS[info.getValue()] ?? info.getValue(),
  }),
  columnHelper.accessor("country_code", {
    id: "country_code",
    header: "Kraj",
    cell: (info) => <span className="font-mono text-xs">{info.getValue() ?? "—"}</span>,
  }),
  columnHelper.accessor("source_ref", {
    id: "source_ref",
    header: "Pochodzenie",
    cell: (info) => info.getValue(),
  }),
]

const COLUMN_LABELS = {
  code: "Kod",
  name: "Nazwa",
  kind: "Rodzaj",
  country_code: "Kraj",
  source_ref: "Pochodzenie",
}

export function LocationCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [search, setSearch] = useState("")
  const [zoneCode, setZoneCode] = useState("")
  const [zoneName, setZoneName] = useState("")
  const [selectedZoneId, setSelectedZoneId] = useState("")
  const [memberCountry, setMemberCountry] = useState("")
  const [postalFrom, setPostalFrom] = useState("")
  const [postalTo, setPostalTo] = useState("")
  const [resolveCountry, setResolveCountry] = useState("")
  const [resolveCode, setResolveCode] = useState("")
  const [resolved, setResolved] = useState<Location | null>(null)

  const sessionReady = Boolean(ctx.organizationId && ctx.userId)

  const locationsQuery = useQuery({
    queryKey: ["locations", ctx.organizationId, search],
    queryFn: () => fetchLocations(search),
    enabled: sessionReady,
    retry: false,
  })

  const membersQuery = useQuery({
    queryKey: ["location-zone-members", ctx.organizationId, selectedZoneId],
    queryFn: () => fetchZoneMembers(selectedZoneId),
    enabled: sessionReady && selectedZoneId !== "",
    retry: false,
  })

  const zones = (locationsQuery.data ?? []).filter((row) => row.kind === "postal_zone")

  const createZoneMutation = useMutation({
    mutationFn: () => createZone(zoneCreateBody({ code: zoneCode, name: zoneName })),
    onSuccess: () => {
      setZoneCode("")
      setZoneName("")
      void queryClient.invalidateQueries({ queryKey: ["locations", ctx.organizationId] })
    },
  })

  const addMemberMutation = useMutation({
    mutationFn: () =>
      addZoneMember(
        selectedZoneId,
        zoneMemberCreateBody({
          countryCode: memberCountry,
          postalFrom,
          postalTo,
        }),
      ),
    onSuccess: () => {
      setPostalFrom("")
      setPostalTo("")
      void queryClient.invalidateQueries({
        queryKey: ["location-zone-members", ctx.organizationId, selectedZoneId],
      })
    },
  })

  const resolveMutation = useMutation({
    mutationFn: () => resolvePostalCode(resolveCountry, resolveCode),
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
        title="Lokalizacje i strefy taryfowe"
        subtitle="location M-05 · strefa to zakresy kodów pocztowych tenanta, nie cudzy podział"
      />

      {sessionReady ? null : <TenantSessionNotice />}

      <form
        className="grid gap-2 rounded-md border border-border bg-card p-3 md:grid-cols-3"
        onSubmit={(event) => {
          event.preventDefault()
          createZoneMutation.mutate()
        }}
      >
        <Input
          aria-label="Kod strefy"
          placeholder="TROJMIASTO"
          value={zoneCode}
          onChange={(event) => setZoneCode(event.target.value)}
          required
        />
        <Input
          aria-label="Nazwa strefy"
          placeholder="Trójmiasto"
          value={zoneName}
          onChange={(event) => setZoneName(event.target.value)}
          required
        />
        <Button type="submit" disabled={createZoneMutation.isPending || !sessionReady}>
          Dodaj strefę
        </Button>
      </form>

      {createZoneMutation.isError ? <CatalogError error={createZoneMutation.error} /> : null}

      <section className="space-y-2 rounded-md border border-border bg-card p-3">
        <div className="text-sm font-medium">Zakresy pocztowe strefy</div>
        <form
          className="grid gap-2 md:grid-cols-5"
          onSubmit={(event) => {
            event.preventDefault()
            addMemberMutation.mutate()
          }}
        >
          <select
            aria-label="Strefa taryfowa"
            className="h-8 rounded-md border border-input bg-background px-2 text-xs"
            value={selectedZoneId}
            onChange={(event) => setSelectedZoneId(event.target.value)}
            required
          >
            <option value="">wybierz strefę</option>
            {zones.map((zone) => (
              <option key={zone.id} value={zone.id}>
                {zone.code} · {zone.name}
              </option>
            ))}
          </select>
          <Input
            aria-label="Kraj zakresu"
            placeholder="PL"
            value={memberCountry}
            onChange={(event) => setMemberCountry(event.target.value)}
            required
          />
          <Input
            aria-label="Kod pocztowy od"
            placeholder="81-000"
            value={postalFrom}
            onChange={(event) => setPostalFrom(event.target.value)}
            required
          />
          <Input
            aria-label="Kod pocztowy do"
            placeholder="81-999"
            value={postalTo}
            onChange={(event) => setPostalTo(event.target.value)}
            required
          />
          <Button
            type="submit"
            variant="outline"
            disabled={addMemberMutation.isPending || selectedZoneId === ""}
          >
            Dodaj zakres
          </Button>
        </form>

        {addMemberMutation.isError ? <CatalogError error={addMemberMutation.error} /> : null}

        {membersQuery.data && membersQuery.data.length > 0 ? (
          <ul className="space-y-px font-mono text-xs">
            {membersQuery.data.map((member) => (
              <li key={member.id}>
                {member.country_code} {member.postal_from}–{member.postal_to}
              </li>
            ))}
          </ul>
        ) : null}

        {membersQuery.isError ? <CatalogError error={membersQuery.error} /> : null}
      </section>

      <form
        className="flex gap-2 rounded-md border border-border bg-card p-3"
        onSubmit={(event) => {
          event.preventDefault()
          resolveMutation.mutate()
        }}
      >
        <Input
          aria-label="Kraj kodu pocztowego"
          placeholder="PL"
          value={resolveCountry}
          onChange={(event) => setResolveCountry(event.target.value)}
        />
        <Input
          aria-label="Kod pocztowy do rozwiązania"
          placeholder="81-198"
          value={resolveCode}
          onChange={(event) => setResolveCode(event.target.value)}
        />
        <Button
          type="submit"
          variant="outline"
          disabled={resolveMutation.isPending || !resolveCountry || !resolveCode}
        >
          Rozwiąż
        </Button>
        {resolved ? (
          <div className="self-center font-mono text-xs">
            {resolved.code} · {resolved.name}
          </div>
        ) : null}
      </form>

      {resolveMutation.isError ? <CatalogError error={resolveMutation.error} /> : null}

      <form
        className="flex gap-2 rounded-md border border-border bg-card p-3"
        onSubmit={(event) => {
          event.preventDefault()
          void locationsQuery.refetch()
        }}
      >
        <Input
          aria-label="Szukaj lokalizacji w bazie"
          placeholder="szukaj po kodzie albo nazwie"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <Button type="submit" variant="outline">
          Szukaj
        </Button>
      </form>

      {locationsQuery.isLoading ? (
        <div className="text-sm text-muted-foreground">Ładowanie…</div>
      ) : null}

      {locationsQuery.isError ? <CatalogError error={locationsQuery.error} /> : null}

      {locationsQuery.data ? (
        <DataTableShell
          tableKey={BUSINESS_LISTS.locations.tableKey}
          columns={columns}
          data={locationsQuery.data}
          columnLabels={COLUMN_LABELS}
          globalFilterPlaceholder="Filtruj pobrane lokalizacje…"
        />
      ) : null}
    </div>
  )
}
