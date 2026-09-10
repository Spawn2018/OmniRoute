import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/task-templates"

export type BlueprintStamp = {
  id: string
  organization_id: string
  template_code: string
  applies_when: string
  source_ref: string
}

export type BlueprintStampWrite = {
  template_code: string
  applies_when: string
  source_ref: string
}

export function blueprintWrite(draft: {
  codeToken: string
  whenNote: string
  originStamp: string
}): BlueprintStampWrite {
  return {
    template_code: draft.codeToken.trim(),
    applies_when: draft.whenNote.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listTaskTemplates(): Promise<BlueprintStamp[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(
      await readApiDetail(listed, "Błąd listy szablonów zadania"),
      httpErrorStatus(listed),
    )
  }
  return (await listed.json()) as BlueprintStamp[]
}

export async function persistTaskTemplate(
  payload: BlueprintStampWrite,
): Promise<BlueprintStamp> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status !== 201) {
    throw new ApiError(
      await readApiDetail(posted, "Błąd zapisu szablonu zadania"),
      httpErrorStatus(posted),
    )
  }
  return (await posted.json()) as BlueprintStamp
}
