import { describe, expect, it } from "vitest"
import { buildSlaWrite } from "@/lib/sla-clauses-api"

describe("sla-clause catalog write", () => {
  it("trims and lowercases metric", () => {
    expect(
      buildSlaWrite({
        contractId: " 11111111-1111-1111-1111-111111111111 ",
        code: " sla_otif_01 ",
        kind: " OTIF ",
        threshold: " OTIF >= 95% ",
        origin: " fixture://sla-clause/a ",
      }),
    ).toEqual({
      customer_contract_id: "11111111-1111-1111-1111-111111111111",
      clause_code: "sla_otif_01",
      metric_kind: "otif",
      threshold_label: "OTIF >= 95%",
      source_ref: "fixture://sla-clause/a",
    })
  })
})
