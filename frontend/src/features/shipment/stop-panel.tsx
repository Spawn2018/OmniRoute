import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { fetchStops, saveStop, stopWrite } from "@/lib/stops-api"
import { getTenantContext } from "@/lib/tenant"

export function StopPointPanel(args: { canWrite: boolean }) {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [shipmentId, setShipmentId] = useState("")
  const [locationId, setLocationId] = useState("")
  const [sequenceNo, setSequenceNo] = useState("1")
  const [timeZone, setTimeZone] = useState("Europe/Warsaw")
  const [stopKind, setStopKind] = useState("loading")
  const [status, setStatus] = useState("pending")
  const [etaPhysical, setEtaPhysical] = useState("2026-09-09T12:00:00+00:00")
  const [etaLegal, setEtaLegal] = useState("2026-09-09T12:00:00+00:00")
  const [groupCode, setGroupCode] = useState("")
  const [groupId, setGroupId] = useState("")
  const [driverNotes, setDriverNotes] = useState("")
  const [weightKg, setWeightKg] = useState("")
  const [quantityHitl, setQuantityHitl] = useState("")
  const [packagingCode, setPackagingCode] = useState("")
  const [sealIn, setSealIn] = useState("")
  const [sealOut, setSealOut] = useState("")
  const [appointmentRef, setAppointmentRef] = useState("")
  const [appointmentStatus, setAppointmentStatus] = useState("")
  const [noShowAt, setNoShowAt] = useState("")
  const [waitingFreeMinutes, setWaitingFreeMinutes] = useState("")
  const [waitingStartedAt, setWaitingStartedAt] = useState("")
  const [podQuality, setPodQuality] = useState("")
  const listQuery = useQuery({
    queryKey: ["stops", ctx.organizationId, shipmentId],
    queryFn: () => fetchStops(shipmentId),
    enabled: args.canWrite && shipmentId !== "",
    retry: false,
  })
  const save = useMutation({
    mutationFn: () =>
      saveStop(
        stopWrite({
          shipmentId,
          locationId,
          stopKind,
          sequenceNo: Number.parseInt(sequenceNo, 10),
          timeZone,
          status,
          etaPhysical,
          etaLegal,
          groupCode,
          groupId,
          driverNotes,
          weightKg,
          quantityHitl,
          packagingCode,
          sealIn,
          sealOut,
          appointmentRef,
          appointmentStatus,
          noShowAt,
          waitingFreeMinutes,
          waitingStartedAt,
          podQuality,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["stops", ctx.organizationId, shipmentId],
      })
    },
  })
  const rows = listQuery.data ?? []
  return (
    <aside className="space-y-2 rounded-md border border-border bg-card p-3" data-stop="point">
      <p className="text-sm font-medium">Punkt załadunku i wyładunku</p>
      <p className="text-xs text-muted-foreground">
        Miejsce ze słownika lokalizacji. Strefa IANA. Dwa ETA HITL. Opcjonalny kod grupy.
        Opcjonalny identyfikator grupy punktów (`stop_group_id`). Opcjonalna waga HITL. Opcjonalna ilość HITL. Opcjonalny kod opakowania HITL. Opcjonalna plomba
        wjazdu i wyjazdu HITL.         Opcjonalny numer awizacji HITL. Opcjonalny status awizacji HITL.
        Opcjonalna chwila niestawiennictwa HITL. Opcjonalne minuty wolnego oczekiwania
        HITL. Opcjonalny początek oczekiwania HITL. Opcjonalna jakość POD HITL.
        Nie mapa. Nie GPS. Nie pogoda. Nie odliczanie. Nie kamera.
      </p>
      <Input
        aria-label="Identyfikator zlecenia punktu"
        placeholder="shipment_id"
        value={shipmentId}
        onChange={(event) => setShipmentId(event.target.value)}
      />
      <Input
        aria-label="Identyfikator lokalizacji punktu"
        placeholder="location_id"
        value={locationId}
        onChange={(event) => setLocationId(event.target.value)}
      />
      <Input
        aria-label="Numer kolejny punktu"
        placeholder="1"
        value={sequenceNo}
        onChange={(event) => setSequenceNo(event.target.value)}
      />
      <Input
        aria-label="Strefa czasowa IANA"
        placeholder="Europe/Warsaw"
        value={timeZone}
        onChange={(event) => setTimeZone(event.target.value)}
      />
      <Input
        aria-label="ETA fizyczne ISO"
        placeholder="2026-09-09T12:00:00+00:00"
        value={etaPhysical}
        onChange={(event) => setEtaPhysical(event.target.value)}
      />
      <Input
        aria-label="ETA prawne ISO"
        placeholder="2026-09-09T12:00:00+00:00"
        value={etaLegal}
        onChange={(event) => setEtaLegal(event.target.value)}
      />
      <Input
        aria-label="Kod grupy punktów"
        placeholder="stop_group_code"
        value={groupCode}
        onChange={(event) => setGroupCode(event.target.value)}
      />
      <Input
        aria-label="Identyfikator grupy punktów"
        placeholder="stop_group_id"
        value={groupId}
        onChange={(event) => setGroupId(event.target.value)}
      />
      <Input
        aria-label="Notatka dla kierowcy"
        placeholder="notes_for_driver"
        value={driverNotes}
        onChange={(event) => setDriverNotes(event.target.value)}
      />
      <Input
        aria-label="Waga punktu w kilogramach"
        placeholder="weight_kg"
        value={weightKg}
        onChange={(event) => setWeightKg(event.target.value)}
      />
      <Input
        aria-label="Ilość na punkcie"
        placeholder="quantity"
        value={quantityHitl}
        onChange={(event) => setQuantityHitl(event.target.value)}
      />
      <Input
        aria-label="Kod opakowania punktu"
        placeholder="packaging_code"
        value={packagingCode}
        onChange={(event) => setPackagingCode(event.target.value)}
      />
      <Input
        aria-label="Plomba wjazdu"
        placeholder="seal_in"
        value={sealIn}
        onChange={(event) => setSealIn(event.target.value)}
      />
      <Input
        aria-label="Plomba wyjazdu"
        placeholder="seal_out"
        value={sealOut}
        onChange={(event) => setSealOut(event.target.value)}
      />
      <Input
        aria-label="Numer awizacji"
        placeholder="appointment_ref"
        value={appointmentRef}
        onChange={(event) => setAppointmentRef(event.target.value)}
      />
      <Input
        aria-label="Status awizacji"
        placeholder="appointment_status"
        value={appointmentStatus}
        onChange={(event) => setAppointmentStatus(event.target.value)}
      />
      <Input
        aria-label="Niestawiennictwo ISO"
        placeholder="no_show_at"
        value={noShowAt}
        onChange={(event) => setNoShowAt(event.target.value)}
      />
      <Input
        aria-label="Minuty wolnego oczekiwania"
        placeholder="waiting_free_minutes"
        value={waitingFreeMinutes}
        onChange={(event) => setWaitingFreeMinutes(event.target.value)}
      />
      <Input
        aria-label="Początek oczekiwania ISO"
        placeholder="waiting_started_at"
        value={waitingStartedAt}
        onChange={(event) => setWaitingStartedAt(event.target.value)}
      />
      <Input
        aria-label="Jakość POD"
        placeholder="pod_quality"
        value={podQuality}
        onChange={(event) => setPodQuality(event.target.value)}
      />
      <fieldset className="space-y-1 text-xs">
        <legend>Rodzaj punktu</legend>
        {(["loading", "unloading", "customs", "ferry", "terminal", "depot", "other"] as const).map(
          (token) => (
            <label key={token} className="mr-3 inline-flex items-center gap-1">
              <input
                checked={stopKind === token}
                name="stop-kind"
                type="radio"
                value={token}
                onChange={() => setStopKind(token)}
              />
              {token}
            </label>
          ),
        )}
      </fieldset>
      <fieldset className="space-y-1 text-xs">
        <legend>Status punktu</legend>
        {(["pending", "at_stop", "completed", "failed"] as const).map((token) => (
          <label key={token} className="mr-3 inline-flex items-center gap-1">
            <input
              checked={status === token}
              name="stop-status"
              type="radio"
              value={token}
              onChange={() => setStatus(token)}
            />
            {token}
          </label>
        ))}
      </fieldset>
      <Button
        type="button"
        disabled={!args.canWrite || shipmentId === "" || locationId === "" || save.isPending}
        onClick={() => save.mutate()}
      >
        Zapisz punkt
      </Button>
      {save.isError ? <p className="text-sm text-destructive">{(save.error as Error).message}</p> : null}
      <ul className="space-y-1">
        {rows.map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.sequence_no} {row.stop_kind} {row.status} {row.stop_group_code ?? ""}{" "}
            {row.notes_for_driver ?? ""} {row.weight_kg ?? ""} {row.quantity ?? ""}{" "}
            {row.packaging_code ?? ""} {row.seal_in ?? ""} {row.seal_out ?? ""}{" "}
            {row.appointment_ref ?? ""} {row.appointment_status ?? ""}{" "}
            {row.no_show_at ?? ""} {row.waiting_free_minutes ?? ""}{" "}
            {row.waiting_started_at ?? ""} {row.pod_quality ?? ""} {row.eta_physical}{" "}
            {row.eta_legal}
          </li>
        ))}
      </ul>
    </aside>
  )
}
