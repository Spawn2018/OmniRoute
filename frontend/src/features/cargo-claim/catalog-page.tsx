import { Link } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent } from "react"
import {
  CatalogError,
  CatalogHeading,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { listCargoClaims, saveCargoClaim } from "@/lib/cargo-claims-api"
import { getTenantContext } from "@/lib/tenant"

const KINDS = ["damage", "shortage", "other"] as const
const OSD = ["overage", "shortage", "damage", "loss"] as const
const WINDOWS = ["notice_7", "notice_21"] as const

function readClaimForm(form: HTMLFormElement) {
  const box = new FormData(form)
  const text = (key: string) => String(box.get(key) ?? "").trim()
  return {
    shipment_id: text("shipment_id"),
    claim_kind: text("claim_kind"),
    damage_code: text("damage_code"),
    cmr_notice_window: text("cmr_notice_window"),
    notice_due_at: text("notice_due_at"),
    suit_due_at: text("suit_due_at"),
    source_ref: text("source_ref"),
  }
}

function ClaimSaveForm(args: { organizationId: string | null }) {
  const client = useQueryClient()
  const save = useMutation({
    mutationFn: saveCargoClaim,
    onSuccess: () => {
      void client.invalidateQueries({ queryKey: ["cargo-claims", args.organizationId] })
    },
  })
  return (
    <form
      data-cargo-claim="leg-form"
      onSubmit={(event: FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        const form = event.currentTarget
        save.mutate(readClaimForm(form), { onSuccess: () => form.reset() })
      }}
    >
      <fieldset className="flex flex-wrap gap-3">
        <legend className="text-xs">Nowa reklamacja</legend>
        <input className="w-56 border px-1 text-xs" name="shipment_id" required />
        <select className="border px-1 text-xs" defaultValue="damage" name="claim_kind">
          {KINDS.map((kind) => (
            <option key={kind} value={kind}>
              {kind}
            </option>
          ))}
        </select>
        <select className="border px-1 text-xs" defaultValue="damage" name="damage_code">
          {OSD.map((code) => (
            <option key={code} value={code}>
              {code}
            </option>
          ))}
        </select>
        <select className="border px-1 text-xs" defaultValue="notice_7" name="cmr_notice_window">
          {WINDOWS.map((window) => (
            <option key={window} value={window}>
              {window}
            </option>
          ))}
        </select>
        <input className="border px-1 text-xs" name="notice_due_at" required type="date" />
        <input className="border px-1 text-xs" name="suit_due_at" required type="date" />
        <input className="w-56 border px-1 text-xs" defaultValue="fixture://cargo-claim/" name="source_ref" required />
        <Button type="submit" disabled={save.isPending || !args.organizationId}>
          Zapisz reklamację
        </Button>
      </fieldset>
      {save.isError ? <CatalogError error={save.error} /> : null}
    </form>
  )
}

function ClaimRows(args: { organizationId: string | null }) {
  const rows = useQuery({
    queryKey: ["cargo-claims", args.organizationId],
    queryFn: listCargoClaims,
    enabled: Boolean(args.organizationId),
    retry: false,
  })
  return (
    <>
      {rows.isError ? <CatalogError error={rows.error} /> : null}
      <ul data-cargo-claim="rows">
        {(rows.data ?? []).map((row) => (
          <li key={row.id} className="text-xs">
            {row.claim_kind} {row.damage_code} {row.cmr_notice_window} {row.notice_due_at}{" "}
            {row.suit_due_at} {row.shipment_id}{" "}
            <Link className="underline" to="/shipments">
              zlecenie
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}

export function CargoClaimPage() {
  const ctx = getTenantContext()
  const ready = Boolean(ctx.organizationId && ctx.userId)
  return (
    <section className="flex flex-col gap-3" data-cargo-claim="board">
      <CatalogHeading
        title="Reklamacje ładunku"
        subtitle="cargo_claim M-55 · OS&D + terminy CMR · nie kwota · nie silnik 7/21/365"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {ready ? <ClaimSaveForm organizationId={ctx.organizationId} /> : null}
      {ready ? <ClaimRows organizationId={ctx.organizationId} /> : null}
    </section>
  )
}
