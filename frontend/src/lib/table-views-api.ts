import { apiGet, apiSend } from "@/lib/api"
import type { TableViewConfig, TableViewRecord } from "@/components/data-table/types"

export async function listTableViews(tableKey: string): Promise<TableViewRecord[]> {
  const params = new URLSearchParams({ table_key: tableKey })
  return apiGet<TableViewRecord[]>(`/api/v1/tenancy/table-views?${params.toString()}`)
}

export async function createTableView(input: {
  table_key: string
  name: string
  config: TableViewConfig
}): Promise<TableViewRecord> {
  return apiSend<TableViewRecord>("/api/v1/tenancy/table-views", {
    method: "POST",
    body: input,
  })
}

export async function updateTableView(
  viewId: string,
  input: { name?: string; config?: TableViewConfig },
): Promise<TableViewRecord> {
  return apiSend<TableViewRecord>(`/api/v1/tenancy/table-views/${viewId}`, {
    method: "PATCH",
    body: input,
  })
}

export async function deleteTableView(viewId: string): Promise<void> {
  await apiSend<void>(`/api/v1/tenancy/table-views/${viewId}`, {
    method: "DELETE",
  })
}
