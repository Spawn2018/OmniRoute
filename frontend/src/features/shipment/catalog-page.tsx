import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Link } from "@tanstack/react-router"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { createShipment, fetchShipments } from "@/lib/shipments-api"
import { getTenantContext } from "@/lib/tenant"
import { BookingInstructionPanel } from "@/features/shipment/booking-instruction-panel"
import { FleetResourcePanel } from "@/features/shipment/fleet-resource-panel"
import { IsoContainerPanel } from "@/features/shipment/iso-container-panel"
import { TripRunPanel } from "@/features/shipment/trip-run-panel"
import { StopPointPanel } from "@/features/shipment/stop-panel"
import { ShipmentStakeholderPanel } from "@/features/shipment/shipment-stakeholder-panel"

function ShipmentCreateForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const [quotationId, setQuotationId] = useState("")
  const [sourceRef, setSourceRef] = useState("fixture://shipment/")
  const [hardNumber, setHardNumber] = useState("")
  const [parentId, setParentId] = useState("")
  const [relationKind, setRelationKind] = useState("")
  const [guideCode, setGuideCode] = useState("")
  const [plantLabel, setPlantLabel] = useState("")
  const [carrierLabel, setCarrierLabel] = useState("")
  const [isWaste, setIsWaste] = useState(false)
  const [etd, setEtd] = useState("")
  const [loadingDate, setLoadingDate] = useState("")
  const [unloadingDate, setUnloadingDate] = useState("")
  const [invoiceDate, setInvoiceDate] = useState("")
  const save = useMutation({
    mutationFn: () =>
      createShipment({
        quotation_id: quotationId.trim(),
        source_ref: sourceRef.trim(),
        shipment_ref: hardNumber.trim() === "" ? null : hardNumber.trim(),
        parent_shipment_id: parentId.trim() === "" ? null : parentId.trim(),
        relation_kind: relationKind.trim() === "" ? null : relationKind.trim(),
        guide_code: guideCode.trim() === "" ? null : guideCode.trim(),
        plant_label: plantLabel.trim() === "" ? null : plantLabel.trim(),
        carrier_label: carrierLabel.trim() === "" ? null : carrierLabel.trim(),
        is_waste: isWaste,
        etd: etd.trim() === "" ? null : etd.trim(),
        loading_date: loadingDate.trim() === "" ? null : loadingDate.trim(),
        unloading_date: unloadingDate.trim() === "" ? null : unloadingDate.trim(),
        invoice_date: invoiceDate.trim() === "" ? null : invoiceDate.trim(),
      }),
    onSuccess: () => {
      setQuotationId("")
      setHardNumber("")
      setParentId("")
      setRelationKind("")
      setGuideCode("")
      setPlantLabel("")
      setCarrierLabel("")
      setIsWaste(false)
      setEtd("")
      setLoadingDate("")
      setUnloadingDate("")
      setInvoiceDate("")
      void client.invalidateQueries({ queryKey: ["shipments", args.organizationId] })
    },
  })
  return (
    <form
      className="flex flex-wrap items-end gap-2 rounded-md border border-border bg-card p-3"
      onSubmit={(event) => {
        event.preventDefault()
        save.mutate()
      }}
    >
      <Input aria-label="Identyfikator wyceny" placeholder="quotation_id" value={quotationId} onChange={(event) => setQuotationId(event.target.value)} required />
      <Input aria-label="Pochodzenie zapisu zlecenia" placeholder="source_ref" value={sourceRef} onChange={(event) => setSourceRef(event.target.value)} required />
      <Input
        aria-label="Numer zlecenia shipment_ref"
        placeholder="omni://shipment/… albo puste"
        value={hardNumber}
        onChange={(event) => setHardNumber(event.target.value)}
      />
      <Input
        aria-label="Zlecenie główne parent_shipment_id"
        placeholder="parent_shipment_id albo puste"
        value={parentId}
        onChange={(event) => setParentId(event.target.value)}
      />
      <Input
        aria-label="Rodzaj relacji relation_kind"
        placeholder="drayage / oncarriage / leg_subcontract / other"
        value={relationKind}
        onChange={(event) => setRelationKind(event.target.value)}
      />
      <Input
        aria-label="Kod przewodnika guide_code"
        placeholder="guide_code albo puste"
        value={guideCode}
        onChange={(event) => setGuideCode(event.target.value)}
      />
      <Input
        aria-label="Etykieta zakładu plant_label"
        placeholder="plant_label albo puste"
        value={plantLabel}
        onChange={(event) => setPlantLabel(event.target.value)}
      />
      <Input
        aria-label="Etykieta przewoźnika carrier_label"
        placeholder="carrier_label albo puste"
        value={carrierLabel}
        onChange={(event) => setCarrierLabel(event.target.value)}
      />
      <label className="flex items-center gap-2 text-xs">
        <input
          aria-label="Flaga odpadu is_waste"
          checked={isWaste}
          onChange={(event) => setIsWaste(event.target.checked)}
          type="checkbox"
        />
        is_waste (HITL · nie MOS)
      </label>
      <Input
        aria-label="Data ETD etd"
        placeholder="etd YYYY-MM-DD albo puste"
        value={etd}
        onChange={(event) => setEtd(event.target.value)}
      />
      <Input
        aria-label="Data załadunku loading_date"
        placeholder="loading_date YYYY-MM-DD albo puste"
        value={loadingDate}
        onChange={(event) => setLoadingDate(event.target.value)}
      />
      <Input
        aria-label="Data wyładunku unloading_date"
        placeholder="unloading_date YYYY-MM-DD albo puste"
        value={unloadingDate}
        onChange={(event) => setUnloadingDate(event.target.value)}
      />
      <Input
        aria-label="Data faktury invoice_date"
        placeholder="invoice_date YYYY-MM-DD albo puste"
        value={invoiceDate}
        onChange={(event) => setInvoiceDate(event.target.value)}
      />
      <Button type="submit" disabled={save.isPending || !args.organizationId}>
        Zapisz zlecenie
      </Button>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

export function ShipmentPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  const shipments = useQuery({
    queryKey: ["shipments", ctx.organizationId],
    queryFn: fetchShipments,
    enabled: ready,
    retry: false,
  })

  return (
    <div className="flex flex-col gap-4" data-shipment="board">
      <CatalogHeading
        title="Zlecenia"
        subtitle="shipment M-35 · tabela z wyceny · opcjonalny rodzic · nie tracking"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {shipments.isError ? <CatalogError error={shipments.error} /> : null}
      <ShipmentCreateForm organizationId={ctx.organizationId} />
      {ready ? <ShipmentStakeholderPanel rows={shipments.data ?? []} signedIn={ready} /> : null}
      {ready ? <BookingInstructionPanel signedIn={ready} /> : null}
      {ready ? <StopPointPanel canWrite={ready} /> : null}
      {ready ? <FleetResourcePanel signedIn={ready} /> : null}
      {ready ? <TripRunPanel signedIn={ready} /> : null}
      {ready ? <IsoContainerPanel signedIn={ready} /> : null}
      {(shipments.data ?? []).map((row) => (
        <p key={row.id} className="text-xs">
          {row.status} {row.source_ref} {row.shipment_ref ?? "bez numeru"}{" "}
          {row.parent_shipment_id ?? "bez rodzica"} {row.relation_kind ?? ""}{" "}
          {row.is_waste ? "odpad" : "bez odpadu"}{" "}
          {row.etd ?? "bez etd"} {row.loading_date ?? "bez załadunku"}{" "}
          {row.unloading_date ?? "bez wyładunku"} {row.invoice_date ?? "bez FV"}{" "}
          <Link className="underline" to="/quotations">
            wycena
          </Link>
        </p>
      ))}
    </div>
  )
}
