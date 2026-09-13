import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { CatalogError, CatalogSourceRefField } from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import {
  createBenefitLedger,
  makeBenefitLedgerPayload,
} from "@/lib/benefit-ledgers-api"

export function BenefitLedgerComposer(props: { organizationId: string | null }) {
  const qc = useQueryClient()
  const [benefitCode, setBenefitCode] = useState("dock_save")
  const [methodLabel, setMethodLabel] = useState("porownanie z wczorajszym charge")
  const [hoursSaved, setHoursSaved] = useState("2.5")
  const [savedAmount, setSavedAmount] = useState("150")
  const [savedCurrency, setSavedCurrency] = useState("EUR")
  const [ref, setRef] = useState("fixture://benefit-ledger/")
  const save = useMutation({
    mutationFn: () =>
      createBenefitLedger(
        makeBenefitLedgerPayload({
          benefitCode,
          methodLabel,
          hoursSaved,
          savedAmount,
          savedCurrency,
          sourceRef: ref,
        }),
      ),
    onSuccess: () => {
      setRef("fixture://benefit-ledger/")
      void qc.invalidateQueries({
        queryKey: ["benefit-ledgers", props.organizationId],
      })
    },
  })

  return (
    <form
      className="flex flex-col gap-2 border border-sky-700/30 bg-sky-50/20 p-3 dark:bg-sky-950/10"
      data-benefit-ledger="composer"
      onSubmit={(event: FormEvent) => {
        event.preventDefault()
        if (props.organizationId) save.mutate()
      }}
    >
      <label className="text-xs">
        benefit_code
        <input
          aria-label="benefit_code ledger"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setBenefitCode(e.target.value)}
          required
          value={benefitCode}
        />
      </label>
      <label className="text-xs">
        method_label
        <input
          aria-label="method_label metoda punktu odniesienia"
          className="mt-1 h-9 w-full rounded border px-2 text-sm"
          onChange={(e) => setMethodLabel(e.target.value)}
          required
          value={methodLabel}
        />
      </label>
      <label className="text-xs">
        hours_saved
        <input
          aria-label="hours_saved godziny"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setHoursSaved(e.target.value)}
          required
          value={hoursSaved}
        />
      </label>
      <label className="text-xs">
        saved_amount
        <input
          aria-label="saved_amount kwota"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          onChange={(e) => setSavedAmount(e.target.value)}
          required
          value={savedAmount}
        />
      </label>
      <label className="text-xs">
        saved_currency
        <input
          aria-label="saved_currency waluta"
          className="mt-1 h-9 w-full rounded border px-2 font-mono text-sm"
          maxLength={3}
          onChange={(e) => setSavedCurrency(e.target.value)}
          required
          value={savedCurrency}
        />
      </label>
      <CatalogSourceRefField
        label="source_ref"
        ariaLabel="source_ref benefit"
        value={ref}
        onChange={setRef}
      />
      {save.error ? <CatalogError error={save.error} /> : null}
      <Button disabled={!props.organizationId || save.isPending} type="submit" variant="outline">
        Zapisz ledger oszczędności
      </Button>
    </form>
  )
}
