import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createColumnHelper } from "@tanstack/react-table"
import { useState } from "react"
import {
  CatalogError,
  CatalogHeading,
  CatalogLoadedTable,
  TenantSessionNotice,
} from "@/components/catalog/catalog-parts"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { CalendarOverridePanel } from "@/features/organization-settings/calendar-panel"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import {
  fetchOrganizationSettings,
  organizationSettingUpsertBody,
  upsertOrganizationSetting,
  type OrganizationSetting,
} from "@/lib/organization-settings-api"
import { getTenantContext } from "@/lib/tenant"

const helper = createColumnHelper<OrganizationSetting>()

const columns = [
  helper.accessor("setting_key", { header: "Klucz" }),
  helper.accessor("setting_value", { header: "Wartość" }),
]

const COLUMN_LABELS = {
  setting_key: "Klucz",
  setting_value: "Wartość",
}

export function OrganizationSettingCatalogPage() {
  const ctx = getTenantContext()
  const queryClient = useQueryClient()
  const [currency, setCurrency] = useState("EUR")
  const [prefix, setPrefix] = useState("OR-Q")
  const [template, setTemplate] = useState("plain")
  const [defaultN, setDefaultN] = useState("3")
  const [laneWindow, setLaneWindow] = useState("90")
  const [fxBasis, setFxBasis] = useState("etd")
  const [fxOffset, setFxOffset] = useState("-1")
  const [fxTable, setFxTable] = useState("nbp_a")
  const [hitlMin, setHitlMin] = useState("0.70")
  const signedIn = Boolean(ctx.organizationId && ctx.userId)

  const query = useQuery({
    queryKey: ["organization-settings", ctx.organizationId],
    queryFn: fetchOrganizationSettings,
    enabled: signedIn,
    retry: false,
  })

  const saveMutation = useMutation({
    mutationFn: () =>
      upsertOrganizationSetting(
        organizationSettingUpsertBody({
          settingKey: "default_currency",
          settingValue: currency,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["organization-settings", ctx.organizationId],
      })
    },
  })

  const savePrefix = useMutation({
    mutationFn: () =>
      upsertOrganizationSetting(
        organizationSettingUpsertBody({
          settingKey: "quotation_number_prefix",
          settingValue: prefix,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["organization-settings", ctx.organizationId],
      })
    },
  })

  const saveDefaultN = useMutation({
    mutationFn: () =>
      upsertOrganizationSetting(
        organizationSettingUpsertBody({
          settingKey: "inquiry_default_n",
          settingValue: defaultN,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["organization-settings", ctx.organizationId],
      })
    },
  })
  const saveLaneWindow = useMutation({
    mutationFn: () =>
      upsertOrganizationSetting(
        organizationSettingUpsertBody({
          settingKey: "lane_scorecard_window_days",
          settingValue: laneWindow,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["organization-settings", ctx.organizationId],
      })
    },
  })
  const saveFxBasis = useMutation({
    mutationFn: () =>
      upsertOrganizationSetting(
        organizationSettingUpsertBody({
          settingKey: "fx_rate_basis",
          settingValue: fxBasis,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["organization-settings", ctx.organizationId],
      })
    },
  })
  const saveFxOffset = useMutation({
    mutationFn: () =>
      upsertOrganizationSetting(
        organizationSettingUpsertBody({
          settingKey: "fx_rate_offset_days",
          settingValue: fxOffset,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["organization-settings", ctx.organizationId],
      })
    },
  })
  const saveFxTable = useMutation({
    mutationFn: () =>
      upsertOrganizationSetting(
        organizationSettingUpsertBody({
          settingKey: "fx_rate_table",
          settingValue: fxTable,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["organization-settings", ctx.organizationId],
      })
    },
  })
  const saveHitlMin = useMutation({
    mutationFn: () =>
      upsertOrganizationSetting(
        organizationSettingUpsertBody({
          settingKey: "hitl_confidence_min",
          settingValue: hitlMin,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["organization-settings", ctx.organizationId],
      })
    },
  })
  const saveTemplate = useMutation({
    mutationFn: () =>
      upsertOrganizationSetting(
        organizationSettingUpsertBody({
          settingKey: "quotation_print_template",
          settingValue: template,
        }),
      ),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["organization-settings", ctx.organizationId],
      })
    },
  })

  return (
    <div className="space-y-3">
      <CatalogHeading
        title="Ustawienia tenanta"
        subtitle="organization_setting M-03 · konfiguracja w bazie · nie env · nie sekrety"
      />

      {signedIn ? null : <TenantSessionNotice />}

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          saveMutation.mutate()
        }}
      >
        <Input
          aria-label="Waluta domyślna ISO"
          placeholder="EUR"
          value={currency}
          onChange={(event) => setCurrency(event.target.value)}
          required
        />
        <Button type="submit" disabled={saveMutation.isPending || !signedIn}>
          Zapisz walutę domyślną
        </Button>
      </form>

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          savePrefix.mutate()
        }}
      >
        <Input
          aria-label="Prefiks numeru oferty"
          placeholder="OR-Q"
          value={prefix}
          onChange={(event) => setPrefix(event.target.value)}
          required
        />
        <Button type="submit" disabled={savePrefix.isPending || !signedIn}>
          Zapisz prefiks numeru
        </Button>
      </form>

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          saveTemplate.mutate()
        }}
      >
        <label className="flex flex-col gap-1 text-xs">
          quotation_print_template
          <select
            aria-label="Szablon oferty"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={template}
            onChange={(event) => setTemplate(event.target.value)}
          >
            <option value="plain">plain</option>
            <option value="letter">letter</option>
          </select>
        </label>
        <Button type="submit" disabled={saveTemplate.isPending || !signedIn}>
          Zapisz szablon oferty
        </Button>
      </form>

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          saveDefaultN.mutate()
        }}
      >
        <Input
          aria-label="Domyślna liczba zapytań"
          placeholder="3"
          value={defaultN}
          onChange={(event) => setDefaultN(event.target.value)}
          required
        />
        <Button type="submit" disabled={saveDefaultN.isPending || !signedIn}>
          Zapisz inquiry_default_n
        </Button>
      </form>

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          saveLaneWindow.mutate()
        }}
      >
        <Input
          aria-label="Okno dni karty lane"
          placeholder="90"
          value={laneWindow}
          onChange={(event) => setLaneWindow(event.target.value)}
          required
        />
        <Button type="submit" disabled={saveLaneWindow.isPending || !signedIn}>
          Zapisz lane_scorecard_window_days
        </Button>
      </form>

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          saveFxBasis.mutate()
        }}
      >
        <label className="flex flex-col gap-1 text-xs">
          fx_rate_basis
          <select
            aria-label="Polityka kursu fx_rate_basis"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={fxBasis}
            onChange={(event) => setFxBasis(event.target.value)}
          >
            <option value="etd">etd</option>
            <option value="loading_date">loading_date</option>
            <option value="unloading_date">unloading_date</option>
            <option value="invoice_date">invoice_date</option>
          </select>
        </label>
        <Button type="submit" disabled={saveFxBasis.isPending || !signedIn}>
          Zapisz fx_rate_basis
        </Button>
      </form>

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          saveFxOffset.mutate()
        }}
      >
        <Input
          aria-label="Offset dni fx_rate_offset_days"
          placeholder="-1"
          value={fxOffset}
          onChange={(event) => setFxOffset(event.target.value)}
          required
        />
        <Button type="submit" disabled={saveFxOffset.isPending || !signedIn}>
          Zapisz fx_rate_offset_days
        </Button>
      </form>

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          saveFxTable.mutate()
        }}
      >
        <label className="flex flex-col gap-1 text-xs">
          fx_rate_table
          <select
            aria-label="Tabela kursu fx_rate_table"
            className="h-8 rounded-md border border-border bg-card px-2 text-sm"
            value={fxTable}
            onChange={(event) => setFxTable(event.target.value)}
          >
            <option value="nbp_a">nbp_a</option>
            <option value="nbp_b">nbp_b</option>
          </select>
        </label>
        <Button type="submit" disabled={saveFxTable.isPending || !signedIn}>
          Zapisz fx_rate_table
        </Button>
      </form>

      <form
        className="flex flex-col gap-2 rounded-md border border-border bg-card p-3 md:flex-row md:flex-wrap"
        onSubmit={(event) => {
          event.preventDefault()
          saveHitlMin.mutate()
        }}
      >
        <Input
          aria-label="Próg pewności HITL hitl_confidence_min"
          placeholder="0.70"
          value={hitlMin}
          onChange={(event) => setHitlMin(event.target.value)}
          required
        />
        <Button type="submit" disabled={saveHitlMin.isPending || !signedIn}>
          Zapisz hitl_confidence_min
        </Button>
      </form>

      {saveMutation.isError ? <CatalogError error={saveMutation.error} /> : null}
      {savePrefix.isError ? <CatalogError error={savePrefix.error} /> : null}
      {saveTemplate.isError ? <CatalogError error={saveTemplate.error} /> : null}
      {saveDefaultN.isError ? <CatalogError error={saveDefaultN.error} /> : null}
      {saveLaneWindow.isError ? <CatalogError error={saveLaneWindow.error} /> : null}
      {saveFxBasis.isError ? <CatalogError error={saveFxBasis.error} /> : null}
      {saveFxOffset.isError ? <CatalogError error={saveFxOffset.error} /> : null}
      {saveFxTable.isError ? <CatalogError error={saveFxTable.error} /> : null}
      {saveHitlMin.isError ? <CatalogError error={saveHitlMin.error} /> : null}

      <CalendarOverridePanel canWrite={signedIn} />

      <CatalogLoadedTable
        loading={query.isLoading}
        error={query.error}
        data={query.data}
        tableKey={BUSINESS_LISTS.organizationSettings.tableKey}
        columns={columns}
        columnLabels={COLUMN_LABELS}
        globalFilterPlaceholder="Szukaj ustawienia…"
      />
    </div>
  )
}
