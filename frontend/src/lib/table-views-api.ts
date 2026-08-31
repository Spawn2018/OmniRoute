import {
  createTableViewApiV1TenancyTableViewsPost,
  deleteTableViewApiV1TenancyTableViewsViewIdDelete,
  listTableViewsApiV1TenancyTableViewsGet,
  updateTableViewApiV1TenancyTableViewsViewIdPatch,
} from "@/api/sdk.gen"
import type { TableViewConfig as ApiTableViewConfig, TableViewResponse } from "@/api/types.gen"
import type { TableViewConfig, TableViewRecord } from "@/components/data-table/types"
import { ApiError } from "@/lib/api"
import { requireTenantHeaders } from "@/lib/tenant"

function statusOf(response: Response | undefined): number {
  return response?.status ?? 500
}

function toRecord(view: TableViewResponse): TableViewRecord {
  const cfg = view.config as TableViewConfig
  return {
    id: view.id,
    organization_id: view.organization_id,
    user_id: view.user_id,
    table_key: view.table_key,
    name: view.name,
    config: {
      column_order: cfg.column_order ?? [],
      column_visibility: cfg.column_visibility ?? {},
      filters: (cfg.filters as Record<string, string>) ?? {},
      sorting: (cfg.sorting as TableViewConfig["sorting"]) ?? [],
      density: cfg.density === "comfortable" ? "comfortable" : "compact",
    },
  }
}

export async function listTableViews(tableKey: string): Promise<TableViewRecord[]> {
  const { data, error, response } = await listTableViewsApiV1TenancyTableViewsGet({
    headers: requireTenantHeaders(),
    query: { table_key: tableKey },
  })
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd listy widoków", statusOf(response))
  }
  return data.map(toRecord)
}

export async function createTableView(input: {
  table_key: string
  name: string
  config: TableViewConfig
}): Promise<TableViewRecord> {
  const { data, error, response } = await createTableViewApiV1TenancyTableViewsPost({
    headers: requireTenantHeaders(),
    body: {
      table_key: input.table_key,
      name: input.name,
      config: input.config as ApiTableViewConfig,
    },
  })
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd zapisu widoku", statusOf(response))
  }
  return toRecord(data)
}

export async function updateTableView(
  viewId: string,
  input: { name?: string; config?: TableViewConfig },
): Promise<TableViewRecord> {
  const { data, error, response } = await updateTableViewApiV1TenancyTableViewsViewIdPatch({
    headers: requireTenantHeaders(),
    path: { view_id: viewId },
    body: {
      name: input.name,
      config: input.config as ApiTableViewConfig | undefined,
    },
  })
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd aktualizacji widoku", statusOf(response))
  }
  return toRecord(data)
}

export async function deleteTableView(viewId: string): Promise<void> {
  const { error, response } = await deleteTableViewApiV1TenancyTableViewsViewIdDelete({
    headers: requireTenantHeaders(),
    path: { view_id: viewId },
  })
  if (error) {
    throw new ApiError(JSON.stringify(error) || "Błąd usuwania widoku", statusOf(response))
  }
}
