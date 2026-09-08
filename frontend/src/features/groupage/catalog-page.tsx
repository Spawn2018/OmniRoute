import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { fetchLocations, roadLocations } from "@/lib/locations-api"
import { getTenantContext } from "@/lib/tenant"
import { GroupageLinePanel } from "./line-panel"

export function GroupagePage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const listed = useQuery({
    queryKey: ["groupage-places", ctx.organizationId],
    queryFn: () => fetchLocations(""),
    enabled: ready,
    retry: false,
  })
  const hubs = roadLocations(listed.data ?? [])

  return (
    <section className="flex flex-col gap-3" data-groupage="run">
      <CatalogHeading
        title="Linie drobnicy"
        subtitle="D1 groupage_line · cutoff + transit_days + ISODOW · strefa lub adres · nie WMS"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.isError ? <CatalogError error={listed.error} /> : null}
      <dl className="grid grid-cols-2 gap-x-3 text-xs">
        {hubs.map((row) => (
          <div key={row.id} className="contents">
            <dt className="font-mono">{row.kind}</dt>
            <dd>
              {row.name}{" "}
              <Link className="underline" to="/locations">
                {row.id}
              </Link>
            </dd>
          </div>
        ))}
      </dl>
      {ready ? <GroupageLinePanel organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
