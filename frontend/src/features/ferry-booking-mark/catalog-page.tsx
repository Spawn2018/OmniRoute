import { useQuery } from "@tanstack/react-query"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { loadFerryBookingMarks } from "@/lib/ferry-booking-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { FerryBookingMarkSave } from "./mark-form"

export function FerryBookingMarkDesk() {
  const tenant = getTenantContext()
  const organizationId = tenant.organizationId
  const deskOpen = Boolean(organizationId && tenant.userId)
  const listing = useQuery({
    enabled: deskOpen,
    queryFn: loadFerryBookingMarks,
    queryKey: ["ferry-booking-board", organizationId],
    retry: false,
  })
  const marks = listing.data ?? []

  return (
    <article className="space-y-6" data-ferry-booking-mark="desk">
      <CatalogHeading
        title="Rezerwacja promu"
        subtitle="BR4.0 ferry_booking_mark · katalog HITL · nie live bilet · nie solver art. 9"
      />
      {deskOpen ? null : <TenantSessionNotice />}
      {deskOpen ? <FerryBookingMarkSave organizationId={organizationId} /> : null}
      {listing.error ? <CatalogError error={listing.error} /> : null}
      {deskOpen && listing.error == null ? (
        <ul className="max-w-2xl space-y-3" data-ferry-booking-mark="catalog">
          {marks.map((mark) => (
            <li className="border-b pb-2" key={mark.id}>
              <p className="font-mono text-sm">{mark.mark_code}</p>
              <p className="text-sm">Stance: {mark.booking_kind}</p>
              <p className="font-mono text-xs text-muted-foreground">{mark.source_ref}</p>
            </li>
          ))}
        </ul>
      ) : null}
    </article>
  )
}
