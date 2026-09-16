import { readFileSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { groupInboundMessages } from "@/lib/mail-groups"

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")

describe("mail-integration surface for 25.0", () => {
  it("ships /mail as read-only known addresses without IMAP", () => {
    const page = readFileSync(path.join(srcRoot, "features/mail-integration/catalog-page.tsx"), "utf8")
    const route = readFileSync(path.join(srcRoot, "routes/mail.tsx"), "utf8")
    const nav = readFileSync(path.join(srcRoot, "components/layout/sidebar.tsx"), "utf8")
    const lists = readFileSync(path.join(srcRoot, "lib/business-lists.ts"), "utf8")
    const ops = readFileSync(path.join(srcRoot, "features/ops/ops-index.ts"), "utf8")
    expect(route).toContain("/mail")
    expect(nav).toContain("/mail")
    expect(lists).toContain("mailIntegration")
    expect(ops).toContain("/mail")
    expect(page).toContain('data-mail-integration="board"')
    expect(page).toContain("fetchEmailDomains")
    expect(page).toContain("fetchContacts")
    expect(page).toContain("resolvePartyEmail")
    expect(page).not.toContain("createContact")
    expect(page).not.toContain("createEmailDomain")
    expect(page).not.toContain("emailengine")
    expect(page).not.toContain("smtp")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).toContain('data-mail-client="mailto"')
    expect(page).toContain("mailto:")
    expect(page).not.toContain("office.js")
    expect(page).not.toContain("manifest.xml")
    expect(page).not.toContain("graph.microsoft")
  })

  it("ships inbound_message fixture list and write on the same /mail board", () => {
    const page = readFileSync(path.join(srcRoot, "features/mail-integration/catalog-page.tsx"), "utf8")
    const api = readFileSync(path.join(srcRoot, "lib/inbound-messages-api.ts"), "utf8")
    expect(page).toContain('data-inbound-message="fixture"')
    expect(page).toContain("CatalogLoadedTable")
    expect(page).toContain("createInboundMessage")
    expect(page).toContain("fetchInboundMessages")
    expect(page).toContain("resolveInboundMessageEmail")
    expect(page).toContain("extractInboundMessage")
    expect(page).toContain("Extract HITL")
    expect(page).toContain("createCustomerRfq")
    expect(page).toContain("Utwórz RFQ")
    expect(page).toContain("Wycena")
    expect(page).toContain("Podpnij HS")
    expect(page).toContain("patchCustomerRfqCommodity")
    expect(page).toContain("Podpnij UN")
    expect(page).toContain("patchCustomerRfqDangerous")
    expect(page).toContain("fetchDangerousGoods")
    expect(page).toContain('data-customer-rfq="un"')
    expect(page).toContain("/quotations?rfq=")
    expect(page).toContain("party_id")
    expect(api).toContain("/api/v1/inbound-messages")
    expect(api).toContain("resolve-email")
    expect(api).toContain("/extract")
    expect(api).not.toContain("graph.microsoft")
    expect(api).toContain("/ingest-graph")
    expect(page).toContain("ingestGraphInboundMessage")
    expect(page).toContain("Ingest Graph")
    expect(page).toContain('data-inbound-message="graph-ingest"')
    expect(api).toContain("/ingest-imap")
    expect(page).toContain("ingestMailboxInboundMessage")
    expect(page).toContain("Ingest skrzynka")
    expect(page).toContain('data-inbound-message="mailbox-ingest"')
    expect(page).toContain('aria-label="Message-ID"')
    expect(page).toContain('aria-label="In-Reply-To"')
    expect(api).toContain("rfc822_message_id")
    expect(api).toContain("in_reply_to")
    const rfqApi = readFileSync(path.join(srcRoot, "lib/customer-rfqs-api.ts"), "utf8")
    expect(rfqApi).toContain("/api/v1/customer-rfqs")
    expect(rfqApi).not.toContain("amount")
  })
})

describe("O8 mail group_by", () => {
  it("groups by party country and defaults to party", () => {
    const page = readFileSync(path.join(srcRoot, "features/mail-integration/catalog-page.tsx"), "utf8")
    expect(page).toContain('data-mail="groups"')
    expect(page).toContain("groupInboundMessages")
    expect(page).toContain("Grupowanie wiadomości")
    const rows = [
      {
        id: "m1",
        organization_id: "o",
        source_ref: "fixture://1",
        from_address: "a@x.test",
        subject: "A",
        body_text: "x",
        status: "stored",
        party_id: "p-nl",
        external_id: null,
        rfc822_message_id: null,
        in_reply_to: null,
      },
      {
        id: "m2",
        organization_id: "o",
        source_ref: "fixture://2",
        from_address: "b@x.test",
        subject: "B",
        body_text: "y",
        status: "stored",
        party_id: "p-pl",
        external_id: null,
        rfc822_message_id: null,
        in_reply_to: null,
      },
    ]
    const parties = [
      { id: "p-nl", country_code: "NL" },
      { id: "p-pl", country_code: "PL" },
    ]
    expect(groupInboundMessages(rows, parties, "country").map((row) => row.key)).toEqual(["NL", "PL"])
    expect(groupInboundMessages(rows, parties, "party").map((row) => row.key)).toEqual(["p-nl", "p-pl"])
  })

  it("groups by rfc822 thread key", () => {
    const page = readFileSync(path.join(srcRoot, "features/mail-integration/catalog-page.tsx"), "utf8")
    expect(page).toContain('value="thread"')
    const rows = [
      {
        id: "root",
        organization_id: "o",
        source_ref: "fixture://1",
        from_address: "a@x.test",
        subject: "A",
        body_text: "x",
        status: "draft",
        party_id: "p-nl",
        external_id: null,
        rfc822_message_id: "<root@ex.com>",
        in_reply_to: null,
      },
      {
        id: "reply",
        organization_id: "o",
        source_ref: "fixture://2",
        from_address: "b@x.test",
        subject: "Re: A",
        body_text: "y",
        status: "draft",
        party_id: "p-pl",
        external_id: null,
        rfc822_message_id: "<reply@ex.com>",
        in_reply_to: "<root@ex.com>",
      },
      {
        id: "orphan",
        organization_id: "o",
        source_ref: "fixture://3",
        from_address: "c@x.test",
        subject: "C",
        body_text: "z",
        status: "draft",
        party_id: null,
        external_id: null,
        rfc822_message_id: null,
        in_reply_to: null,
      },
    ]
    expect(groupInboundMessages(rows, [], "thread").map((row) => row.key)).toEqual([
      "<root@ex.com>",
      "—",
    ])
    expect(groupInboundMessages(rows, [], "thread")[0]?.rows).toHaveLength(2)
  })
})
