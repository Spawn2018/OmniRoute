import { useEffect, useMemo, useState, type ReactNode } from "react"
import { subscribeOperatorAction } from "@/lib/operator-actions"
import {
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  useReactTable,
  type ColumnDef,
  type ColumnFiltersState,
  type ColumnOrderState,
  type VisibilityState,
} from "@tanstack/react-table"
import { useVirtualizer } from "@tanstack/react-virtual"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { ColumnEditor } from "@/components/data-table/column-editor"
import {
  DEFAULT_TABLE_VIEW_CONFIG,
  mergeColumnOrder,
  type TableDensity,
  type TableViewConfig,
} from "@/components/data-table/types"
import { ViewManager } from "@/components/data-table/view-manager"
import { Input } from "@/components/ui/input"
import { track } from "@/lib/analytics"
import { createTableView, listTableViews, updateTableView } from "@/lib/table-views-api"
import { cn } from "@/lib/utils"

type DataTableShellProps<TData> = {
  tableKey: string
  // TanStack ColumnDef: wariancja TValue — `any` tylko na granicy API tabeli.
  columns: ColumnDef<TData, any>[]
  data: TData[]
  columnLabels: Record<string, string>
  globalFilterPlaceholder?: string
  toolbarExtra?: ReactNode
}

export function DataTableShell<TData>({
  tableKey,
  columns,
  data,
  columnLabels,
  globalFilterPlaceholder = "Filtruj…",
  toolbarExtra,
}: DataTableShellProps<TData>) {
  const queryClient = useQueryClient()
  const allColumnIds = useMemo(
    () => columns.map((column) => String(column.id ?? ("accessorKey" in column ? column.accessorKey : ""))).filter(Boolean),
    [columns],
  )

  const [columnOrder, setColumnOrder] = useState<ColumnOrderState>(allColumnIds)
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({})
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
  const [globalFilter, setGlobalFilter] = useState("")
  const [density, setDensity] = useState<TableDensity>("compact")
  const [panelOpen, setPanelOpen] = useState(false)
  const [activeViewId, setActiveViewId] = useState<string | null>(null)
  const [draftName, setDraftName] = useState("")

  const viewsQuery = useQuery({
    queryKey: ["table-views", tableKey],
    queryFn: () => listTableViews(tableKey),
  })

  const table = useReactTable({
    data,
    columns,
    state: {
      columnOrder,
      columnVisibility,
      columnFilters,
      globalFilter,
    },
    onColumnOrderChange: setColumnOrder,
    onColumnVisibilityChange: setColumnVisibility,
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  })

  const rows = table.getRowModel().rows
  const [scrollEl, setScrollEl] = useState<HTMLDivElement | null>(null)
  const virtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => scrollEl,
    estimateSize: () => (density === "compact" ? 32 : 40),
    overscan: 12,
  })

  function currentConfig(): TableViewConfig {
    const filters: Record<string, string> = {}
    for (const filter of columnFilters) {
      filters[filter.id] = String(filter.value ?? "")
    }
    if (globalFilter) {
      filters.__global = globalFilter
    }
    return {
      column_order: columnOrder.length > 0 ? columnOrder : allColumnIds,
      column_visibility: Object.fromEntries(
        allColumnIds.map((id) => [id, columnVisibility[id] !== false]),
      ),
      filters,
      sorting: [],
      density,
    }
  }

  function applyConfig(config: TableViewConfig) {
    setColumnOrder(mergeColumnOrder(config.column_order, allColumnIds))
    setColumnVisibility(config.column_visibility)
    setDensity(config.density === "comfortable" ? "comfortable" : "compact")
    const nextFilters: ColumnFiltersState = []
    let nextGlobal = ""
    for (const [key, value] of Object.entries(config.filters ?? {})) {
      if (key === "__global") {
        nextGlobal = value
        continue
      }
      nextFilters.push({ id: key, value })
    }
    setColumnFilters(nextFilters)
    setGlobalFilter(nextGlobal)
  }

  const saveMutation = useMutation({
    mutationFn: async (name: string) => {
      const trimmed = name.trim() || "operator"
      const config = currentConfig()
      const existing = viewsQuery.data?.find((view) => view.name === trimmed)
      if (existing) {
        return updateTableView(existing.id, { config })
      }
      return createTableView({
        table_key: tableKey,
        name: trimmed,
        config,
      })
    },
    onSuccess: async (saved) => {
      track("table_view_saved", { table_key: tableKey, view_id: saved.id })
      setActiveViewId(saved.id)
      await queryClient.invalidateQueries({ queryKey: ["table-views", tableKey] })
    },
  })

  useEffect(() => {
    return subscribeOperatorAction((id) => {
      if (id !== "save-view") {
        return
      }
      setPanelOpen(true)
      const name = draftName.trim() || "operator"
      setDraftName(name)
      saveMutation.mutate(name)
    })
  }, [draftName, saveMutation])

  const rowHeight = density === "compact" ? "py-1" : "py-2"

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-2">
        <Input
          value={globalFilter}
          onChange={(e) => {
            setGlobalFilter(e.target.value)
            track("filter_used", { table_key: tableKey, filter: "global" })
          }}
          placeholder={globalFilterPlaceholder}
          className="h-8 max-w-xs"
        />
        <label className="flex items-center gap-1 text-xs text-muted-foreground">
          Gęstość
          <select
            aria-label="Gęstość tabeli"
            data-table-density={density}
            className="h-8 rounded-md border border-input bg-card px-2 text-sm text-foreground"
            value={density}
            onChange={(e) => setDensity(e.target.value as TableDensity)}
          >
            <option value="compact">Zwarta</option>
            <option value="comfortable">Wygodna</option>
          </select>
        </label>
        <button
          type="button"
          className="h-8 rounded-md border border-border px-2 text-xs hover:bg-muted"
          onClick={() => setPanelOpen((open) => !open)}
        >
          {panelOpen ? "Ukryj kolumny" : "Kolumny / widoki"}
        </button>
        {toolbarExtra}
      </div>

      {panelOpen ? (
        <div className="grid gap-4 rounded-md border border-border bg-card p-3 md:grid-cols-2">
          <ColumnEditor
            columnIds={mergeColumnOrder(columnOrder, allColumnIds)}
            labels={columnLabels}
            visibility={Object.fromEntries(
              allColumnIds.map((id) => [id, columnVisibility[id] !== false]),
            )}
            onVisibilityChange={(columnId, visible) => {
              setColumnVisibility((prev) => ({ ...prev, [columnId]: visible }))
            }}
            onOrderChange={setColumnOrder}
          />
          <ViewManager
            views={viewsQuery.data ?? []}
            activeViewId={activeViewId}
            draftName={draftName}
            onDraftNameChange={setDraftName}
            onSelectView={(viewId) => {
              const view = viewsQuery.data?.find((item) => item.id === viewId)
              if (!view) {
                return
              }
              applyConfig({ ...DEFAULT_TABLE_VIEW_CONFIG, ...view.config })
              setActiveViewId(view.id)
              setDraftName(view.name)
              track("table_view_applied", { table_key: tableKey, view_id: view.id })
            }}
            onSave={() => saveMutation.mutate(draftName)}
            onReset={() => {
              applyConfig(DEFAULT_TABLE_VIEW_CONFIG)
              setColumnOrder(allColumnIds)
              setActiveViewId(null)
            }}
            busy={saveMutation.isPending}
          />
        </div>
      ) : null}

      <div
        ref={setScrollEl}
        className="max-h-[28rem] overflow-auto rounded-md border border-border bg-card"
      >
        <table className="w-full min-w-[480px] border-collapse text-sm">
          <thead className="sticky top-0 z-10 bg-muted">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id} className="border-b border-border text-left text-xs text-muted-foreground">
                {headerGroup.headers.map((header) => (
                  <th key={header.id} className="px-3 py-1.5 font-medium">
                    {header.isPlaceholder
                      ? null
                      : flexRender(header.column.columnDef.header, header.getContext())}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody style={{ height: `${virtualizer.getTotalSize()}px`, position: "relative" }}>
            {virtualizer.getVirtualItems().map((virtualRow) => {
              const row = rows[virtualRow.index]
              return (
                <tr
                  key={row.id}
                  className="absolute left-0 w-full border-b border-border hover:bg-muted/60"
                  style={{ transform: `translateY(${virtualRow.start}px)` }}
                >
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className={cn("px-3", rowHeight)}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              )
            })}
          </tbody>
        </table>
        {rows.length === 0 ? (
          <div className="px-3 py-8 text-center text-sm text-muted-foreground">Brak wierszy</div>
        ) : null}
      </div>
    </div>
  )
}
