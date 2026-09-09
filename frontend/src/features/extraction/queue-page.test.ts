import { describe, expect, it } from "vitest"
import { extractionCreateBody } from "@/lib/extractions-api"

describe("extractionCreateBody", () => {
  it("sends document_base64 without input_text when a file is chosen", () => {
    expect(
      extractionCreateBody({
        sourceRef: "doc://x",
        inputText: "THC 1 EUR",
        documentBase64: "YQ==",
      }),
    ).toEqual({ source_ref: "doc://x", document_base64: "YQ==" })
  })

  it("sends input_text without document_base64 when there is no file", () => {
    expect(
      extractionCreateBody({
        sourceRef: "doc://x",
        inputText: "THC 1 EUR",
        documentBase64: null,
      }),
    ).toEqual({ source_ref: "doc://x", input_text: "THC 1 EUR" })
  })

  it("sends tender_rfp HITL fields without money math", () => {
    expect(
      extractionCreateBody({
        sourceRef: "doc://rfp",
        inputText: "RFP",
        documentBase64: null,
        draftKind: "tender_rfp",
        rfp: {
          tender_id: "11111111-1111-1111-1111-111111111111",
          intake_code: "scope",
        },
      }),
    ).toEqual({
      source_ref: "doc://rfp",
      input_text: "RFP",
      draft_kind: "tender_rfp",
      rfp: {
        tender_id: "11111111-1111-1111-1111-111111111111",
        intake_code: "scope",
      },
    })
  })
})
