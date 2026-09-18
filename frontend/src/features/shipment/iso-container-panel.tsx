import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { containerWrite, fetchContainers, optionalHours, optionalToken, saveContainer } from "@/lib/containers-api"
import { getTenantContext } from "@/lib/tenant"

export function IsoContainerPanel(args: { signedIn: boolean }) {
  const ctx = getTenantContext()
  const cache = useQueryClient()
  const [number, setNumber] = useState("")
  const [sizeType, setSizeType] = useState("22G1")
  const [shipment, setShipment] = useState("")
  const [seal, setSeal] = useState("")
  const [seal2, setSeal2] = useState("")
  const [seal3, setSeal3] = useState("")
  const [vessel, setVessel] = useState("")
  const [voyage, setVoyage] = useState("")
  const [note, setNote] = useState("")
  const [goods, setGoods] = useState("")
  const [pack, setPack] = useState("")
  const [mark, setMark] = useState("")
  const [mark2, setMark2] = useState("")
  const [mark3, setMark3] = useState("")
  const [mark4, setMark4] = useState("")
  const [mark5, setMark5] = useState("")
  const [cold, setCold] = useState(false)
  const [dock, setDock] = useState("")
  const [yard, setYard] = useState("")
  const [bill, setBill] = useState("")
  const [idle, setIdle] = useState("")
  const [dwell, setDwell] = useState("")
  const [demurrage, setDemurrage] = useState("")
  const [detention, setDetention] = useState("")
  const [mixed, setMixed] = useState("")
  const [cut, setCut] = useState("")
  const [ams, setAms] = useState("")
  const [cy, setCy] = useState("")
  const [cfs, setCfs] = useState("")
  const [mass, setMass] = useState("")
  const [tare, setTare] = useState("")
  const [pin, setPin] = useState("")
  const [payload, setPayload] = useState("")
  const [teu, setTeu] = useState("")
  const [pieces, setPieces] = useState("")
  const [weigh, setWeigh] = useState("")
  const [vgm, setVgm] = useState("")
  const [survey, setSurvey] = useState("")
  const [book, setBook] = useState("")
  const [carrier, setCarrier] = useState("")
  const [leg, setLeg] = useState("")
  const listed = useQuery({
    queryKey: ["containers", ctx.organizationId, sizeType],
    queryFn: () => fetchContainers(sizeType),
    enabled: args.signedIn,
    retry: false,
  })
  const persist = useMutation({
    mutationFn: () =>
      saveContainer({
        ...containerWrite({
          number,
          sizeType,
          shipment,
          seal,
          seal2,
          seal3,
          vessel,
          voyage,
          note,
          goods,
          pack,
          mark,
          mark2,
          mark3,
          mark4,
          mark5,
          cold,
        }),
        pickup_terminal: optionalToken(dock),
        return_terminal: optionalToken(yard),
        bl_kind: optionalToken(bill),
        free_time_origin_h: optionalHours(idle),
        free_time_dest_h: optionalHours(dwell),
        demurrage_free_days: optionalHours(demurrage),
        detention_free_days: optionalHours(detention),
        mixed_dd_days: optionalHours(mixed),
        si_cutoff_at: optionalToken(cut),
        ams_cutoff_at: optionalToken(ams),
        cy_cutoff_at: optionalToken(cy),
        cfs_cutoff_at: optionalToken(cfs),
        vgm_kg: optionalToken(mass),
        tare_kg: optionalToken(tare),
        pin_code: optionalToken(pin),
        payload_kg: optionalToken(payload),
        teu: optionalToken(teu),
        quantity: optionalHours(pieces),
        vgm_method: optionalToken(weigh),
        vgm_cutoff_at: optionalToken(vgm),
        last_survey_at: optionalToken(survey),
        booking_no: optionalToken(book),
        carrier_party_id: optionalToken(carrier),
        shipment_leg_id: optionalToken(leg),
      }),
    onSuccess: () => {
      void cache.invalidateQueries({ queryKey: ["containers", ctx.organizationId, sizeType] })
    },
  })
  const blocked = !args.signedIn || number.trim() === "" || persist.isPending
  return (
    <section className="grid gap-2 rounded-md border border-border p-3" data-container="iso">
      <h2 className="text-sm font-medium">Kontener ISO</h2>
      <p className="text-xs text-muted-foreground">
        Numer z cyfrą kontrolną i typ 4 znaków. Opcjonalne plomby, statek, rejs, uwaga, ładunek, opakowanie, referencje, flaga chłodniczego, terminale pobrania oraz zwrotu, rodzaj listu, godziny wolnego czasu na origin oraz destination, dni demurrage HITL, dni detention HITL, dni mixed D&D HITL, cutoff SI, cutoff AMS, cutoff CY, cutoff CFS, VGM (kg Decimal, metoda SOLAS, cutoff), tara HITL (kg Decimal), ładowność HITL (kg Decimal), TEU HITL (Decimal, nie z typu ISO), ilość HITL (sztuki, nie punkt), czas ostatniego przeglądu, numer bookingu, PIN odbioru HITL (tekst), UUID armatora oraz UUID odcinka. Nie odliczanie. Nie HBL. Nie temperatura. Nie kalkulator kg. Nie live terminal. Nie ciphertext. Nie S21. Nie live HTTP.
      </p>
      <label className="flex flex-col gap-1 text-xs">
        Numer ISO 6346
        <Input
          aria-label="Numer kontenera ISO"
          placeholder="container_no"
          value={number}
          onChange={(event) => setNumber(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Typ ISO (iso_size_type)
        <Input
          aria-label="Typ ISO kontenera"
          placeholder="iso_size_type"
          value={sizeType}
          onChange={(event) => setSizeType(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Zlecenie (opcjonalnie)
        <Input
          aria-label="Identyfikator zlecenia kontenera"
          placeholder="shipment_id"
          value={shipment}
          onChange={(event) => setShipment(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Pierwsza plomba (opcjonalnie)
        <Input
          aria-label="Pierwsza plomba kontenera"
          placeholder="seal_no_1"
          value={seal}
          onChange={(event) => setSeal(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Druga plomba (opcjonalnie)
        <Input
          aria-label="Druga plomba kontenera"
          placeholder="seal_no_2"
          value={seal2}
          onChange={(event) => setSeal2(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Trzecia plomba (opcjonalnie)
        <Input
          aria-label="Trzecia plomba kontenera"
          placeholder="seal_no_3"
          value={seal3}
          onChange={(event) => setSeal3(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Statek (opcjonalnie)
        <Input
          aria-label="Nazwa statku kontenera"
          placeholder="vessel_name"
          value={vessel}
          onChange={(event) => setVessel(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Rejs (opcjonalnie)
        <Input
          aria-label="Numer rejsu kontenera"
          placeholder="voyage_no"
          value={voyage}
          onChange={(event) => setVoyage(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Uwaga (opcjonalnie)
        <Input
          aria-label="Uwaga kontenera"
          placeholder="remarks"
          value={note}
          onChange={(event) => setNote(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Ładunek (opcjonalnie)
        <Input
          aria-label="Opis ładunku kontenera"
          placeholder="cargo_description"
          value={goods}
          onChange={(event) => setGoods(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Opakowanie (opcjonalnie)
        <Input
          aria-label="Kod opakowania kontenera"
          placeholder="packaging_code"
          value={pack}
          onChange={(event) => setPack(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Referencja 1 (opcjonalnie)
        <Input
          aria-label="Referencja 1 kontenera"
          placeholder="ref_1"
          value={mark}
          onChange={(event) => setMark(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Referencja 2 (opcjonalnie)
        <Input
          aria-label="Referencja 2 kontenera"
          placeholder="ref_2"
          value={mark2}
          onChange={(event) => setMark2(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Referencja 3 (opcjonalnie)
        <Input
          aria-label="Referencja 3 kontenera"
          placeholder="ref_3"
          value={mark3}
          onChange={(event) => setMark3(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Referencja 4 (opcjonalnie)
        <Input
          aria-label="Referencja 4 kontenera"
          placeholder="ref_4"
          value={mark4}
          onChange={(event) => setMark4(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Referencja 5 (opcjonalnie)
        <Input
          aria-label="Referencja 5 kontenera"
          placeholder="ref_5"
          value={mark5}
          onChange={(event) => setMark5(event.target.value)}
        />
      </label>
      <label className="flex items-center gap-2 text-xs">
        <input
          type="checkbox"
          aria-label="Chłodniczy kontener"
          checked={cold}
          onChange={(event) => setCold(event.target.checked)}
        />
        Chłodniczy (reefer)
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Terminal pobrania (opcjonalnie)
        <Input
          aria-label="Terminal pobrania kontenera"
          placeholder="pickup_terminal"
          value={dock}
          onChange={(event) => setDock(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Terminal zwrotu (opcjonalnie)
        <Input
          aria-label="Terminal zwrotu kontenera"
          placeholder="return_terminal"
          value={yard}
          onChange={(event) => setYard(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Rodzaj listu (opcjonalnie)
        <Input
          aria-label="Rodzaj listu kontenera"
          placeholder="bl_kind"
          value={bill}
          onChange={(event) => setBill(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Godziny wolnego czasu origin (opcjonalnie)
        <Input
          aria-label="Godziny wolnego czasu origin kontenera"
          placeholder="free_time_origin_h"
          value={idle}
          onChange={(event) => setIdle(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Godziny wolnego czasu destination (opcjonalnie)
        <Input
          aria-label="Godziny wolnego czasu destination kontenera"
          placeholder="free_time_dest_h"
          value={dwell}
          onChange={(event) => setDwell(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Dni demurrage HITL (opcjonalnie)
        <Input
          aria-label="Dni demurrage HITL kontenera"
          placeholder="demurrage_free_days"
          value={demurrage}
          onChange={(event) => setDemurrage(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Dni detention HITL (opcjonalnie)
        <Input
          aria-label="Dni detention HITL kontenera"
          placeholder="detention_free_days"
          value={detention}
          onChange={(event) => setDetention(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Dni mixed D&D HITL (opcjonalnie)
        <Input
          aria-label="Dni mixed D and D HITL kontenera"
          placeholder="mixed_dd_days"
          value={mixed}
          onChange={(event) => setMixed(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Cutoff SI (opcjonalnie)
        <Input
          aria-label="Cutoff SI kontenera"
          placeholder="si_cutoff_at"
          value={cut}
          onChange={(event) => setCut(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Cutoff AMS (opcjonalnie)
        <Input
          aria-label="Cutoff AMS kontenera"
          placeholder="ams_cutoff_at"
          value={ams}
          onChange={(event) => setAms(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Cutoff CY (opcjonalnie)
        <Input
          aria-label="Cutoff CY kontenera"
          placeholder="cy_cutoff_at"
          value={cy}
          onChange={(event) => setCy(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Cutoff CFS (opcjonalnie)
        <Input
          aria-label="Cutoff CFS kontenera"
          placeholder="cfs_cutoff_at"
          value={cfs}
          onChange={(event) => setCfs(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        VGM kg (opcjonalnie)
        <Input
          aria-label="VGM kg kontenera"
          placeholder="vgm_kg"
          value={mass}
          onChange={(event) => setMass(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Tara kg HITL (opcjonalnie)
        <Input
          aria-label="Tara kg kontenera"
          placeholder="tare_kg"
          value={tare}
          onChange={(event) => setTare(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Ładowność kg HITL (opcjonalnie)
        <Input
          aria-label="Ładowność kg kontenera"
          placeholder="payload_kg"
          value={payload}
          onChange={(event) => setPayload(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        TEU HITL (opcjonalnie)
        <Input
          aria-label="TEU kontenera"
          placeholder="teu"
          value={teu}
          onChange={(event) => setTeu(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Ilość HITL (opcjonalnie)
        <Input
          aria-label="Ilość kontenera"
          placeholder="quantity"
          value={pieces}
          onChange={(event) => setPieces(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        PIN odbioru (opcjonalnie)
        <Input
          aria-label="PIN odbioru kontenera"
          placeholder="pin_code"
          value={pin}
          onChange={(event) => setPin(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Metoda VGM (opcjonalnie)
        <Input
          aria-label="Metoda VGM kontenera"
          placeholder="vgm_method"
          value={weigh}
          onChange={(event) => setWeigh(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Cutoff VGM (opcjonalnie)
        <Input
          aria-label="Cutoff VGM kontenera"
          placeholder="vgm_cutoff_at"
          value={vgm}
          onChange={(event) => setVgm(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Ostatni przegląd (opcjonalnie)
        <Input
          aria-label="Ostatni przegląd kontenera"
          placeholder="last_survey_at"
          value={survey}
          onChange={(event) => setSurvey(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Numer bookingu (opcjonalnie)
        <Input
          aria-label="Numer bookingu kontenera"
          placeholder="booking_no"
          value={book}
          onChange={(event) => setBook(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Armator (opcjonalnie)
        <Input
          aria-label="UUID armatora kontenera"
          placeholder="carrier_party_id"
          value={carrier}
          onChange={(event) => setCarrier(event.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-xs">
        Odcinek (opcjonalnie)
        <Input
          aria-label="UUID odcinka kontenera"
          placeholder="shipment_leg_id"
          value={leg}
          onChange={(event) => setLeg(event.target.value)}
        />
      </label>
      <Button type="button" disabled={blocked} onClick={() => persist.mutate()}>
        Zapisz kontener
      </Button>
      {persist.isError ? (
        <p className="text-sm text-destructive">{(persist.error as Error).message}</p>
      ) : null}
      <ul className="space-y-1">
        {(listed.data ?? []).map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.container_no} · {row.iso_size_type}
            {row.seal_no_1 !== null ? ` · ${row.seal_no_1}` : ""}
            {row.seal_no_2 !== null ? ` · ${row.seal_no_2}` : ""}
            {row.seal_no_3 !== null ? ` · ${row.seal_no_3}` : ""}
            {row.vessel_name !== null ? ` · ${row.vessel_name}` : ""}
            {row.voyage_no !== null ? ` · ${row.voyage_no}` : ""}
            {row.remarks !== null ? ` · ${row.remarks}` : ""}
            {row.cargo_description !== null ? ` · ${row.cargo_description}` : ""}
            {row.packaging_code !== null ? ` · ${row.packaging_code}` : ""}
            {row.ref_1 !== null ? ` · ${row.ref_1}` : ""}
            {row.ref_2 !== null ? ` · ${row.ref_2}` : ""}
            {row.ref_3 !== null ? ` · ${row.ref_3}` : ""}
            {row.ref_4 !== null ? ` · ${row.ref_4}` : ""}
            {row.ref_5 !== null ? ` · ${row.ref_5}` : ""}
            {row.reefer ? " · chłodniczy" : ""}
            {row.pickup_terminal !== null ? ` · ${row.pickup_terminal}` : ""}
            {row.return_terminal !== null ? ` · ${row.return_terminal}` : ""}
            {row.bl_kind !== null ? ` · ${row.bl_kind}` : ""}
            {row.free_time_origin_h !== null ? ` · ${String(row.free_time_origin_h)}h` : ""}
            {row.free_time_dest_h !== null ? ` · ${String(row.free_time_dest_h)}h dest` : ""}
            {row.si_cutoff_at !== null ? ` · SI ${row.si_cutoff_at}` : ""}
            {row.ams_cutoff_at !== null ? ` · AMS ${row.ams_cutoff_at}` : ""}
            {row.cy_cutoff_at !== null ? ` · CY ${row.cy_cutoff_at}` : ""}
            {row.cfs_cutoff_at !== null ? ` · CFS ${row.cfs_cutoff_at}` : ""}
            {row.vgm_kg !== null ? ` · VGM ${row.vgm_kg}` : ""}
            {row.tare_kg !== null ? ` · tara ${row.tare_kg}` : ""}
            {row.payload_kg !== null ? ` · ładowność ${row.payload_kg}` : ""}
            {row.teu !== null ? ` · TEU ${row.teu}` : ""}
            {row.quantity !== null ? ` · ${String(row.quantity)} szt.` : ""}
            {row.pin_code !== null ? ` · PIN ${row.pin_code}` : ""}
            {row.vgm_method !== null ? ` · ${row.vgm_method}` : ""}
            {row.vgm_cutoff_at !== null ? ` · VGM ${row.vgm_cutoff_at}` : ""}
            {row.last_survey_at !== null ? ` · przegląd ${row.last_survey_at}` : ""}
            {row.booking_no !== null ? ` · ${row.booking_no}` : ""}
            {row.carrier_party_id !== null ? ` · ${row.carrier_party_id}` : ""}
            {row.shipment_leg_id !== null ? ` · ${row.shipment_leg_id}` : ""}
          </li>
        ))}
      </ul>
    </section>
  )
}
