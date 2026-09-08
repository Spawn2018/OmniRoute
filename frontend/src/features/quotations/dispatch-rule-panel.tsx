import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  documentDispatchRuleBody,
  fetchDocumentDispatchRules,
  saveDocumentDispatchRule,
} from "@/lib/document-dispatch-rules-api"
import { getTenantContext } from "@/lib/tenant"

const INCOTERM_CSV = "EXW,FCA,CPT,CIP,DAP,DPU,DDP,FAS,FOB,CFR,CIF"
const KIND_CSV = "commercial_invoice,packing_list,bill_of_lading,export_declaration"
const ROLE_CSV = "shipper,consignee,origin_agent,dest_agent,ocean_carrier,omni_customs,client_customs"

function radios(csv: string, current: string, caption: string, onPick: (token: string) => void) {
  return (
    <fieldset className="space-y-1 text-xs">
      <legend>{caption}</legend>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {csv.split(",").map((token) => (
          <label key={`${caption}-${token}`} className="inline-flex items-center gap-1">
            <input
              type="radio"
              name={caption}
              value={token}
              checked={current === token}
              onChange={() => onPick(token)}
            />
            {token}
          </label>
        ))}
      </div>
    </fieldset>
  )
}

function useDispatchCatalog(signedIn: boolean) {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [incoterm, setIncoterm] = useState("DAP")
  const [tradeSide, setTradeSide] = useState("import")
  const [documentKind, setDocumentKind] = useState("commercial_invoice")
  const [recipientRole, setRecipientRole] = useState("omni_customs")
  const listQuery = useQuery({
    queryKey: ["document-dispatch-rules", ctx.organizationId, incoterm, tradeSide],
    queryFn: () => fetchDocumentDispatchRules({ incoterm, tradeSide }),
    enabled: signedIn,
    retry: false,
  })
  const mutation = useMutation({
    mutationFn: () =>
      saveDocumentDispatchRule(
        documentDispatchRuleBody({ incoterm, tradeSide, documentKind, recipientRole }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["document-dispatch-rules", ctx.organizationId, incoterm, tradeSide],
      })
    },
  })
  return { incoterm, setIncoterm, tradeSide, setTradeSide, documentKind, setDocumentKind, recipientRole, setRecipientRole, mutation, rows: listQuery.data ?? [] }
}

export function DispatchRulePanel(args: { signedIn: boolean }) {
  const job = useDispatchCatalog(args.signedIn)
  return (
    <section className="space-y-2 rounded-md border border-border bg-card p-3" data-dispatch-rule="catalog">
      <p className="text-sm font-medium">Adresat dokumentów odprawy</p>
      <p className="text-xs text-muted-foreground">
        Trójka incoterm × strona × rodzaj idzie na rolę ze zlecenia. Nie send. Nie Selenium.
      </p>
      {radios(INCOTERM_CSV, job.incoterm, "incoterm adresata", job.setIncoterm)}
      {radios("import,export", job.tradeSide, "strona handlu adresata", job.setTradeSide)}
      {radios(KIND_CSV, job.documentKind, "rodzaj dokumentu adresata", job.setDocumentKind)}
      {radios(ROLE_CSV, job.recipientRole, "rola adresata", job.setRecipientRole)}
      <Button type="button" disabled={!args.signedIn || job.mutation.isPending} onClick={() => job.mutation.mutate()}>
        Zapisz adresata
      </Button>
      {job.mutation.isError ? (
        <p className="text-sm text-destructive">{(job.mutation.error as Error).message}</p>
      ) : null}
      <ul className="space-y-1">
        {job.rows.map((row) => (
          <li key={row.id} className="font-mono text-xs">
            {row.document_kind} → {row.recipient_role}
          </li>
        ))}
      </ul>
    </section>
  )
}
