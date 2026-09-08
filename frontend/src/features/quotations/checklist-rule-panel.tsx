import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  documentChecklistRuleBody,
  fetchDocumentChecklistRules,
  saveDocumentChecklistRule,
} from "@/lib/document-checklist-rules-api"
import { getTenantContext } from "@/lib/tenant"

const INCOTERMS = ["EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"]
const KINDS = [
  "commercial_invoice",
  "packing_list",
  "bill_of_lading",
  "export_declaration",
] as const

export function ChecklistRulePanel(args: { signedIn: boolean }) {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [incoterm, setIncoterm] = useState("FOB")
  const [tradeSide, setTradeSide] = useState("export")
  const [mode, setMode] = useState("ocean")
  const [documentKind, setDocumentKind] = useState("bill_of_lading")
  const [blocksDispatch, setBlocksDispatch] = useState(true)
  const listQuery = useQuery({
    queryKey: ["document-checklist-rules", ctx.organizationId, incoterm, tradeSide, mode],
    queryFn: () => fetchDocumentChecklistRules({ incoterm, tradeSide, mode }),
    enabled: args.signedIn,
    retry: false,
  })
  const mutation = useMutation({
    mutationFn: () =>
      saveDocumentChecklistRule(
        documentChecklistRuleBody({
          incoterm,
          tradeSide,
          mode,
          documentKind,
          blocksDispatch,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["document-checklist-rules", ctx.organizationId, incoterm, tradeSide, mode],
      })
    },
  })
  return (
    <section className="space-y-2 rounded-md border border-border bg-card p-3" data-checklist-rule="job">
      <p className="text-sm font-medium">Checklista dokumentów</p>
      <p className="text-xs text-muted-foreground">
        Reguła po trójce. Flaga blocks_dispatch jest daną — nie blokuje wysyłki w tym plasterze.
      </p>
      <div className="flex flex-col gap-2 md:flex-row md:flex-wrap">
        <label className="flex flex-col gap-1 text-xs">
          incoterm
          <select
            aria-label="Incoterm checklisty"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={incoterm}
            onChange={(event) => setIncoterm(event.target.value)}
          >
            {INCOTERMS.map((code) => (
              <option key={code} value={code}>
                {code}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          trade_side
          <select
            aria-label="Strona handlu checklisty"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={tradeSide}
            onChange={(event) => setTradeSide(event.target.value)}
          >
            <option value="import">import</option>
            <option value="export">export</option>
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          mode
          <select
            aria-label="Mode checklisty"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={mode}
            onChange={(event) => setMode(event.target.value)}
          >
            <option value="ocean">ocean</option>
            <option value="road">road</option>
            <option value="rail">rail</option>
            <option value="air">air</option>
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          document_kind
          <select
            aria-label="Rodzaj dokumentu checklisty"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={documentKind}
            onChange={(event) => setDocumentKind(event.target.value)}
          >
            {KINDS.map((kind) => (
              <option key={kind} value={kind}>
                {kind}
              </option>
            ))}
          </select>
        </label>
        <label className="flex items-center gap-2 text-xs">
          <input
            type="checkbox"
            aria-label="blocks_dispatch"
            checked={blocksDispatch}
            onChange={(event) => setBlocksDispatch(event.target.checked)}
          />
          blocks_dispatch
        </label>
        <Button type="button" disabled={!args.signedIn || mutation.isPending} onClick={() => mutation.mutate()}>
          Zapisz regułę
        </Button>
      </div>
      {mutation.isError ? (
        <p className="text-sm text-destructive">{(mutation.error as Error).message}</p>
      ) : null}
      {(listQuery.data ?? []).map((row) => (
        <p key={row.id} className="font-mono text-xs">
          {row.document_kind} blocks_dispatch={String(row.blocks_dispatch)}
        </p>
      ))}
    </section>
  )
}
