import { useQuery } from "@tanstack/react-query"
import { fetchTrips } from "@/lib/trips-api"

export default function PlanningTripOverlay() {
  const listed = useQuery({
    queryKey: ["planning-trip-labels"],
    queryFn: () => fetchTrips(""),
    retry: false,
  })
  const marks = listed.data ?? []
  return (
    <section className="mt-3 text-sm" data-planning="map">
      <p>Chunk mapy poza paczką początkową. Kafelki OSM tu nie wchodzą.</p>
      {listed.isError ? (
        <p className="text-destructive">{String(listed.error)}</p>
      ) : null}
      <ol data-planning="trip-labels" className="mt-2 list-decimal pl-5 font-mono text-xs">
        {marks.map((row) => (
          <li key={row.id}>
            {row.trip_no}
            {row.route_label ? ` ${row.route_label}` : ""}
          </li>
        ))}
      </ol>
    </section>
  )
}
