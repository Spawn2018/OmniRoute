import { useQuery } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { CatalogError, CatalogHeading, TenantSessionNotice } from "@/components/catalog/catalog-parts"
import { DataTableShell } from "@/components/data-table/data-table-shell"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { fetchExtractionPromptMarks, type ExtractionPromptMarkRow } from "@/lib/extraction-prompt-marks-api"
import { getTenantContext } from "@/lib/tenant"
import { ExtractionPromptMarkSave } from "./mark-form"

const promptHelper = createColumnHelper<ExtractionPromptMarkRow>()

const PROMPT_TABLE = [
  promptHelper.accessor("mark_code", { header: "Kod" }),
  promptHelper.accessor("prompt_kind", { header: "Rodzaj" }),
  promptHelper.accessor("source_ref", { header: "Źródło" }),
]

export function ExtractionPromptMarkDesk() {
  const tenant = getTenantContext()
  const org = tenant.organizationId
  const canLoad = Boolean(org && tenant.userId)
  const query = useQuery({
    enabled: canLoad,
    queryFn: fetchExtractionPromptMarks,
    queryKey: ["extraction-prompt-marks", org],
    retry: false,
  })

  return (
    <section className="flex flex-col gap-4" data-extraction-prompt-mark="desk">
      <CatalogHeading
        title="Prompt ekstrakcji"
        subtitle="AI3.1 extraction_prompt_mark · HITL · nie Instructor · nie bajty promptu"
      />
      {canLoad ? null : <TenantSessionNotice />}
      {canLoad ? <ExtractionPromptMarkSave organizationId={org} /> : null}
      {query.error ? <CatalogError error={query.error} /> : null}
      {canLoad && query.error == null ? (
        <DataTableShell
          columnLabels={{
            mark_code: "Kod",
            prompt_kind: "Rodzaj",
            source_ref: "Źródło",
          }}
          columns={PROMPT_TABLE}
          data={query.data ?? []}
          globalFilterPlaceholder="Filtr prompt…"
          tableKey={BUSINESS_LISTS.extractionPromptMark.tableKey}
        />
      ) : null}
    </section>
  )
}
