import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchHandoverNotes,
  type HandoverNoteRow,
} from "@/lib/handover-notes-api"
import { getTenantContext } from "@/lib/tenant"
import { HandoverNoteSave } from "./note-form"

const helper = createColumnHelper<HandoverNoteRow>()

const COLUMNS = [
  helper.accessor("note_code", { header: "Oznaczenie" }),
  helper.accessor("situation", { header: "Sytuacja" }),
  helper.accessor("recommendation", { header: "Rekomendacja" }),
  helper.accessor("source_ref", { header: "Zrodlo" }),
]

export function HandoverNoteDesk() {
  const ctx = getTenantContext()
  const orgId = ctx.organizationId
  const ready = Boolean(orgId && ctx.userId)
  const listed = useQuery({
    enabled: ready,
    queryFn: fetchHandoverNotes,
    queryKey: ["handover-notes", orgId],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-6" data-handover-note="board">
      <CatalogHeading
        title="Notatka przekazania SBAR"
        subtitle="N11 handover_note · HITL S/B/A/R tekst · nie auto z tablicy"
      />
      {!ready ? <TenantSessionNotice /> : null}
      {listed.error ? <CatalogError error={listed.error} /> : null}
      {ready ? <HandoverNoteSave organizationId={orgId} /> : null}
      {ready && !listed.error ? (
        <DataTableShell
          columnLabels={{
            note_code: "Oznaczenie",
            situation: "Sytuacja",
            recommendation: "Rekomendacja",
            source_ref: "Zrodlo",
          }}
          columns={COLUMNS}
          data={listed.data ?? []}
          globalFilterPlaceholder="Filtruj notatki SBAR…"
          tableKey={BUSINESS_LISTS.handoverNote.tableKey}
        />
      ) : null}
    </section>
  )
}
