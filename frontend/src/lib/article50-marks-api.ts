import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type Article50MarkRow = {
  id: string
  organization_id: string
  mark_code: string
  label_kind: string
  source_ref: string
}

export type Article50MarkPayload = {
  mark_code: string
  label_kind: string
  source_ref: string
}

const PATH = "/api/v1/article50-marks"

export function buildArticle50MarkWrite(args: {
  code: string
  kind: string
  origin: string
}): Article50MarkPayload {
  return {
    mark_code: args.code.trim(),
    label_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchArticle50Marks(): Promise<Article50MarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu art. 50"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as Article50MarkRow[]
}

export async function saveArticle50Mark(
  payload: Article50MarkPayload,
): Promise<Article50MarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "article50-mark-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika art. 50"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as Article50MarkRow
}
