import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tasks"

export type TaskStamp = {
  id: string
  organization_id: string
  task_code: string
  template_code: string
  status_kind: string
  source_ref: string
}

export type TaskStampWrite = {
  task_code: string
  template_code: string
  status_kind: string
  source_ref: string
}

export function taskWrite(draft: {
  codeToken: string
  templateToken: string
  statusToken: string
  originStamp: string
}): TaskStampWrite {
  return {
    task_code: draft.codeToken.trim(),
    template_code: draft.templateToken.trim(),
    status_kind: draft.statusToken.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listTasks(): Promise<TaskStamp[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(
      await readApiDetail(listed, "Błąd listy zadań"),
      httpErrorStatus(listed),
    )
  }
  return (await listed.json()) as TaskStamp[]
}

export async function persistTask(payload: TaskStampWrite): Promise<TaskStamp> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status !== 201) {
    throw new ApiError(
      await readApiDetail(posted, "Błąd zapisu zadania"),
      httpErrorStatus(posted),
    )
  }
  return (await posted.json()) as TaskStamp
}
