import { describe, expect, it } from "vitest"
import { factoringConnectorWrite } from "@/lib/factoring-connectors-api"

describe("factoringConnectorWrite", () => {
  it("trims connector fields", () => {
    expect(
      factoringConnectorWrite({
        codeStamp: " smeo_trade ",
        kindStamp: " smeo ",
        originStamp: " fixture://smeo/1 ",
      }),
    ).toEqual({
      connector_code: "smeo_trade",
      system_kind: "smeo",
      source_ref: "fixture://smeo/1",
    })
  })
})
