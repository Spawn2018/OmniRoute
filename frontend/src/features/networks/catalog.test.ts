import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import {
  carrierInquiryBatchBody,
  inquiryIdsForMembers,
  topRankedMemberIds,
} from "@/lib/carrier-inquiries-api"
import { mailDraftBatchBody } from "@/lib/mail-drafts-api"
import { inquiryDefaultN } from "@/lib/organization-settings-api"
import { networkCreateBody } from "@/lib/networks-api"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("networkCreateBody", () => {
  it("splits aliases and blanks optional text", () => {
    expect(
      networkCreateBody({
        code: " WCA ",
        name: " WCA Worldwide ",
        aliasesText: " wca_ww , , ",
        website: "  ",
        regionScope: " PL ",
        isGlobal: true,
      }),
    ).toEqual({
      code: "WCA",
      name: "WCA Worldwide",
      aliases: ["wca_ww"],
      website: null,
      region_scope: "PL",
      is_global: true,
    })
  })
})

describe("networks catalog surface for 9.0", () => {
  it("ships /networks on DataTableShell with create and resolve", () => {
    const page = readFileSync(path.join(srcRoot, "features/networks/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/networks.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/networks")
    expect(nav).toContain("/networks")
    expect(lists).toContain("networks")
    expect(ops).toContain("/networks")
    expect(page).toContain("CatalogLoadedTable")
    expect(page).toContain("createNetwork")
    expect(page).toContain("resolveNetwork")
    expect(page).toContain("source_ref")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("rate_line")
    expect(page).toContain("createNetworkMember")
    expect(page).toContain('data-network-member="catalog"')
    expect(page).toContain("createCarrierInquiry")
    expect(page).toContain("createCarrierInquiryBatch")
    expect(page).toContain("createMailDraftBatch")
    expect(page).toContain("fetchCarrierInquiryRanking")
    expect(page).toContain("inquiry_default_n")
    expect(page).toContain("Zapisz szkice")
    expect(page).toContain('data-carrier-inquiry="catalog"')
    expect(page).toContain('data-carrier-inquiry="batch"')
    expect(page).toContain('data-mail-draft="batch"')
    expect(page).not.toContain("cheerio")
    expect(page).not.toContain("httpx")
  })
})

describe("carrierInquiryBatchBody", () => {
  it("drops blank ports and empty member ids", () => {
    expect(
      carrierInquiryBatchBody({
        memberIds: [" a ", "", "b"],
        status: " queued ",
        originPortId: "  ",
        destinationPortId: " dest ",
      }),
    ).toEqual({
      network_member_ids: ["a", "b"],
      status: "queued",
      destination_port_id: "dest",
    })
  })
})

describe("O4 ranking and draft batch helpers", () => {
  it("picks top N members and their inquiry ids", () => {
    expect(
      topRankedMemberIds(
        [
          { network_member_id: "a", answered_count: 3 },
          { network_member_id: "b", answered_count: 1 },
          { network_member_id: "c", answered_count: 0 },
        ],
        2,
      ),
    ).toEqual(["a", "b"])
    expect(
      inquiryIdsForMembers(
        [
          {
            id: "i1",
            organization_id: "o",
            network_member_id: "a",
            source_ref: "tenant:manual",
            status: "answered",
            origin_port_id: null,
            destination_port_id: null,
            quoted_amount: "10.0000",
            quoted_currency: "USD",
            quoted_transit_days: null,
          },
          {
            id: "i2",
            organization_id: "o",
            network_member_id: "c",
            source_ref: "tenant:manual",
            status: "draft",
            origin_port_id: null,
            destination_port_id: null,
            quoted_amount: null,
            quoted_currency: null,
            quoted_transit_days: null,
          },
        ],
        ["a"],
      ),
    ).toEqual(["i1"])
  })

  it("reads inquiry_default_n and builds a draft batch", () => {
    expect(
      inquiryDefaultN([{ id: "1", organization_id: "o", setting_key: "inquiry_default_n", setting_value: "5" }]),
    ).toBe(5)
    expect(inquiryDefaultN([])).toBe(3)
    expect(
      mailDraftBatchBody({
        subjectIds: [" a ", "", "b"],
        body: " RFQ ",
        sourceRef: " tenant:manual ",
        subjectKind: " carrier_inquiry ",
      }),
    ).toEqual({
      subject_ids: ["a", "b"],
      body: "RFQ",
      source_ref: "tenant:manual",
      subject_kind: "carrier_inquiry",
    })
  })
})
