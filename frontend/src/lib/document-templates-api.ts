import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/document-templates"

export type SheetMark = {
  id: string
  organization_id: string
  template_kind: string
  language: string
  layout_ref: string
  branding_ref: string | null
  output_kind: string
  source_ref: string
}

export type SheetMarkWrite = {
  template_kind: string
  language: string
  layout_ref: string
  branding_ref?: string | null
  output_kind: string
  source_ref: string
}

export function sheetWrite(args: {
  kindToken: string
  tongueToken: string
  layoutToken: string
  brandToken: string
  exitToken: string
  originStamp: string
}): SheetMarkWrite {
  const branding = args.brandToken.trim()
  return {
    template_kind: args.kindToken.trim(),
    language: args.tongueToken.trim(),
    layout_ref: args.layoutToken.trim(),
    branding_ref: branding === "" ? null : branding,
    output_kind: args.exitToken.trim(),
    source_ref: args.originStamp.trim(),
  }
}

export async function listSheetMarks(): Promise<SheetMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(
      await readApiDetail(reply, "Błąd listy szablonów wydruku"),
      httpErrorStatus(reply),
    )
  }
  const payload: unknown = await reply.json()
  return payload as SheetMark[]
}

export async function persistSheetMark(payload: SheetMarkWrite): Promise<SheetMark> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "sheet-mark",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(
      await readApiDetail(reply, "Błąd zapisu szablonu wydruku"),
      httpErrorStatus(reply),
    )
  }
  const saved: unknown = await reply.json()
  return saved as SheetMark
}
