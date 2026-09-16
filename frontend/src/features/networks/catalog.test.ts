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
import { noReplyNoticeCreateBody } from "@/lib/operator-notices-api"
import { inquiryDefaultN } from "@/lib/organization-settings-api"
import { membersForCountry, membersListQuery, networkCreateBody, partyCountryMap } from "@/lib/networks-api"

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
    expect(page).toContain('data-network-member="country-filter"')
    expect(page).toContain('data-carrier-inquiry="silence"')
    expect(page).toContain('data-carrier-inquiry="overdue"')
    expect(page).toContain("noReplyNoticeCreateBody")
    expect(page).toContain("patchInquirySilence")
    expect(page).toContain("fetchNetworkMembers")
    expect(page).toContain("countryFilter")
    expect(page).toContain("fetchParties")
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
            no_reply_after: null,
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
            no_reply_after: null,
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


describe("O7 country filter helpers", () => {
  it("keeps NL parties and drops members without a party", () => {
    const mapped = partyCountryMap([
      { id: "p-nl", country_code: "NL" },
      { id: "p-pl", country_code: "PL" },
    ])
    const members = [
      { id: "m1", organization_id: "o", network_id: "n", member_code: "nl", legal_name: "Rotterdam", party_id: "p-nl", source_ref: "tenant:manual" },
      { id: "m2", organization_id: "o", network_id: "n", member_code: "pl", legal_name: "Gdynia", party_id: "p-pl", source_ref: "tenant:manual" },
      { id: "m3", organization_id: "o", network_id: "n", member_code: "x", legal_name: "Brak", party_id: null, source_ref: "tenant:manual" },
    ]
    expect(membersForCountry(members, mapped, "nl").map((row) => row.id)).toEqual(["m1"])
    expect(membersForCountry(members, mapped, "").map((row) => row.id)).toEqual(["m1", "m2", "m3"])
  })

  it("builds country_code query for API list", () => {
    expect(membersListQuery("")).toBe("")
    expect(membersListQuery(" nl ")).toBe("country_code=NL")
    expect(membersListQuery("12")).toBe("country_code=12")
  })
})

describe("N5 no_reply notice helper", () => {
  it("builds a no_reply notice from inquiry id", () => {
    expect(noReplyNoticeCreateBody("  i1  ")).toEqual({
      body: "brak odpowiedzi: i1",
      source_ref: "tenant:manual:inquiry:i1",
      kind: "no_reply",
    })
  })
})
