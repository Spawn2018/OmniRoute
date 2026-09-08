/* Seed i pełny job per M-xx. Rodzina = kolumny + akcje, nie jedna tabela USD. */
window.OR_MOD = (function () {
  const $ = (s, c) => (c || document).querySelector(s);
  const store = {};
  const filters = {};
  const files = {};
  const LAYER = { kanon: "kanon", uzup: "uzup.", a: "luka A", b: "linia B", c: "odroczone", plat: "platforma", ops: "ops" };

  const MONEY = new Set(["quote", "rates", "charges", "channels", "finance"]);
  const SOURCE = new Set(["rates", "charges", "channels", "quote"]);
  const HITL = new Set(["hitl", "quote", "party"]);
  const PARK = new Set(["portal", "c"]);

  const COLS = {
    quote: [
      { k: "ref", t: "Ref" }, { k: "party", t: "Klient" }, { k: "lane", t: "Relacja" },
      { k: "status", t: "Status" }, { k: "hs", t: "HS" }, { k: "incoterm", t: "Incoterm" },
      { k: "amt", t: "Kwota", money: true }, { k: "src", t: "source_ref" }
    ],
    ship: [
      { k: "ref", t: "Ref" }, { k: "party", t: "Klient" }, { k: "lane", t: "Relacja" },
      { k: "incoterm", t: "Incoterm" }, { k: "status", t: "Status" }, { k: "docs", t: "Dokumenty" }, { k: "src", t: "source_ref" }
    ],
    hitl: [
      { k: "ref", t: "Szkic" }, { k: "src", t: "Źródło" }, { k: "lane", t: "Relacja" },
      { k: "age", t: "Wiek" }, { k: "status", t: "Status" }
    ],
    rates: [
      { k: "ref", t: "Ref" }, { k: "lane", t: "Relacja" }, { k: "party", t: "Dostawca" },
      { k: "code", t: "Kod" }, { k: "amt", t: "Kupno", money: true }, { k: "src", t: "source_ref" }, { k: "status", t: "Wersja" }
    ],
    charges: [
      { k: "ref", t: "Ref" }, { k: "code", t: "Kod" }, { k: "party", t: "Strona" },
      { k: "buy", t: "Kupno", money: true }, { k: "sell", t: "Sprzedaż", money: true },
      { k: "margin", t: "Marża", money: true }, { k: "src", t: "source_ref" }
    ],
    party: [
      { k: "ref", t: "Ref" }, { k: "party", t: "Nazwa" }, { k: "tax", t: "Tax ID" },
      { k: "vat", t: "VAT UE" }, { k: "eori", t: "EORI" }, { k: "duns", t: "DUNS" },
      { k: "role", t: "Role" }, { k: "status", t: "Status" }, { k: "src", t: "source_ref" }
    ],
    finance: [
      { k: "ref", t: "Ref" }, { k: "party", t: "Strona" }, { k: "ksef", t: "ksef_ref" },
      { k: "status", t: "Status" }, { k: "amt", t: "Kwota", money: true }, { k: "src", t: "source_ref" }
    ],
    customs: [
      { k: "ref", t: "Pakiet" }, { k: "incoterm", t: "Incoterm" }, { k: "recipient", t: "Odbiorca" },
      { k: "docs", t: "Komplet" }, { k: "status", t: "Status" }, { k: "src", t: "source_ref" }
    ],
    catalog: [
      { k: "ref", t: "Ref" }, { k: "title", t: "Nazwa" }, { k: "code", t: "Kod" },
      { k: "status", t: "Status" }, { k: "src", t: "source_ref" }
    ],
    channels: [
      { k: "ref", t: "Ref" }, { k: "party", t: "Armator" }, { k: "lane", t: "POL/POD" },
      { k: "tt", t: "TT" }, { k: "status", t: "Status" }, { k: "amt", t: "Kwota", money: true },
      { k: "src", t: "source_ref" }
    ],
    compliance: [
      { k: "ref", t: "Ref" }, { k: "title", t: "Sprawa" }, { k: "party", t: "Strona" },
      { k: "status", t: "Werdykt" }, { k: "src", t: "source_ref" }
    ],
    settings: [
      { k: "ref", t: "Klucz" }, { k: "title", t: "Wartość" }, { k: "party", t: "Zakres" },
      { k: "status", t: "Status" }, { k: "src", t: "source_ref" }
    ],
    platform: [
      { k: "ref", t: "Zdarzenie" }, { k: "title", t: "Rodzaj" }, { k: "status", t: "Stan" },
      { k: "src", t: "klucz idempotencji" }
    ],
    portal: [
      { k: "ref", t: "Ref" }, { k: "party", t: "Konto" }, { k: "role", t: "Rola" },
      { k: "status", t: "Dostęp" }, { k: "src", t: "source_ref" }
    ],
    modal: [
      { k: "ref", t: "Ref" }, { k: "lane", t: "Odcinek" }, { k: "party", t: "Przewoźnik" },
      { k: "status", t: "Status" }, { k: "src", t: "source_ref" }
    ],
    warehouse: [
      { k: "ref", t: "Ref" }, { k: "title", t: "Lokalizacja" }, { k: "status", t: "Status" },
      { k: "src", t: "source_ref" }
    ],
    trade: [
      { k: "ref", t: "Ref" }, { k: "party", t: "Strona" }, { k: "title", t: "Przedmiot" },
      { k: "status", t: "Status" }, { k: "src", t: "source_ref" }
    ],
    ops: [
      { k: "ref", t: "Zadanie" }, { k: "title", t: "Opis" }, { k: "status", t: "Stan" },
      { k: "src", t: "source_ref" }
    ],
    home: [
      { k: "ref", t: "Job" }, { k: "title", t: "Opis" }, { k: "status", t: "Stan" }, { k: "src", t: "source_ref" }
    ]
  };

  const SPEC_COLS = {
    89: [
      { k: "ref", t: "Ref" }, { k: "code", t: "booking_scope" }, { k: "role", t: "target_role" },
      { k: "status", t: "Status" }, { k: "src", t: "source_ref" }
    ],
    99: [
      { k: "incoterm", t: "Incoterm" }, { k: "role", t: "trade_side" }, { k: "code", t: "document_kind" },
      { k: "recipient", t: "recipient_role" }, { k: "src", t: "source_ref" }
    ],
    106: [
      { k: "ref", t: "container_no" }, { k: "code", t: "iso_size_type" }, { k: "lane", t: "Zlecenie" },
      { k: "status", t: "Status" }, { k: "src", t: "source_ref" }
    ],
    108: [
      { k: "ref", t: "Kraj" }, { k: "title", t: "calendar_day" }, { k: "code", t: "day_kind" },
      { k: "status", t: "is_working_day" }, { k: "src", t: "source_ref" }
    ],
    111: [
      { k: "ref", t: "Ref" }, { k: "code", t: "resource_kind" }, { k: "title", t: "display_name" },
      { k: "lane", t: "registration_no" }, { k: "status", t: "Status" }, { k: "src", t: "source_ref" }
    ],
    116: [
      { k: "ref", t: "Ref" }, { k: "lane", t: "Odcinek" }, { k: "code", t: "leg_kind" },
      { k: "party", t: "Zlecenie" }, { k: "status", t: "Status" }, { k: "src", t: "source_ref" }
    ],
    205: [
      { k: "incoterm", t: "Incoterm" }, { k: "role", t: "trade_side" }, { k: "lane", t: "mode" },
      { k: "code", t: "document_kind" }, { k: "status", t: "blocks_dispatch" }, { k: "src", t: "source_ref" }
    ]
  };

  function familyOf(mod) {
    return COLS[mod.tpl] ? mod.tpl : "catalog";
  }

  function colsFor(mod) {
    return SPEC_COLS[mod.n] || COLS[familyOf(mod)];
  }

  function hasMoney(mod) {
    return MONEY.has(familyOf(mod));
  }

  function parties() {
    return ["Meblexport", "Nordwood", "Baltic Parts", "Andes Cargo", "Hapag-Lloyd"];
  }

  function seedSpec(mod) {
    const src = (i) => `${mod.id}-SRC-${1000 + i}`;
    if (mod.n === 89) {
      const scopes = ["ocean", "oncarriage", "contact_exchange", "precarriage", "none", "ocean"];
      const roles = ["ocean_carrier", "dest_agent", "origin_agent", "shipper", "consignee", "omni_customs"];
      const st = ["suggested", "accepted", "suggested", "confirmed", "rejected", "sent"];
      return scopes.map((scope, i) => ({
        id: `${mod.id}-${i + 1}`, ref: `BI/${2026}/${String(12 + i).padStart(4, "0")}`,
        title: scope, party: parties()[i % 5], lane: "GD/2026/00412", status: st[i],
        amt: "0,00", cur: "USD", src: src(i), code: scope, role: roles[i],
        incoterm: "DAP", named_place: "Lima", trade_side: "export"
      }));
    }
    if (mod.n === 99) {
      const kinds = ["commercial_invoice", "packing_list", "bill_of_lading", "export_declaration", "commercial_invoice", "packing_list"];
      const rec = ["omni_customs", "omni_customs", "dest_agent", "omni_customs", "client_customs", "shipper"];
      return kinds.map((kind, i) => ({
        id: `${mod.id}-${i + 1}`, ref: `DDR/${2026}/${String(20 + i).padStart(4, "0")}`,
        title: kind, party: rec[i], lane: "DAP × export", status: "aktywna",
        amt: "0,00", cur: "USD", src: `fixture://document-dispatch-rule/${i + 1}`,
        code: kind, role: i % 2 ? "import" : "export", recipient: rec[i],
        incoterm: i < 4 ? "DAP" : "FOB", named_place: i < 4 ? "Lima" : "", trade_side: i % 2 ? "import" : "export"
      }));
    }
    if (mod.n === 106) {
      const nos = ["MSKU7823410", "MSKU7823528", "TCLU5566771", "HLBU1234567", "CMAU9988770", "MSCU1100228"];
      return nos.map((no, i) => ({
        id: `${mod.id}-${i + 1}`, ref: no, title: no, party: "Hapag-Lloyd AG",
        lane: i < 2 ? "GD/2026/00412" : "—", status: i < 2 ? "na zleceniu" : "wolny",
        amt: "0,00", cur: "USD", src: `fixture://container/${i + 1}`,
        code: i % 2 ? "45G1" : "22G1", incoterm: "DAP"
      }));
    }
    if (mod.n === 108) {
      const days = [
        ["PL", "2026-09-08", "working", "tak"],
        ["PL", "2026-11-11", "holiday", "nie"],
        ["PE", "2026-09-08", "working", "tak"],
        ["PE", "2026-07-28", "holiday", "nie"],
        ["NL", "2026-09-08", "working", "tak"],
        ["DE", "2026-10-03", "holiday", "nie"]
      ];
      return days.map((d, i) => ({
        id: `${mod.id}-${i + 1}`, ref: d[0], title: d[1], party: "tenant",
        lane: d[0], status: d[3], amt: "0,00", cur: "USD",
        src: `fixture://organization-calendar/${i + 1}`, code: d[2]
      }));
    }
    if (mod.n === 111) {
      const rows = [
        ["vehicle", "Volvo FH 500", "GD 4821L", "aktywny"],
        ["driver", "Piotr Zieliński", "—", "aktywny"],
        ["trailer", "Krone 40HC", "GD 9012N", "aktywny"],
        ["vehicle", "MAN TGX", "PO 2201K", "aktywny"],
        ["driver", "Anna Lis", "—", "aktywny"],
        ["trailer", "Schmitz Cargobull", "GD 3310M", "superseded"]
      ];
      return rows.map((r, i) => ({
        id: `${mod.id}-${i + 1}`, ref: `RES/${2026}/${String(40 + i).padStart(4, "0")}`,
        title: r[1], party: r[1], lane: r[2], status: r[3], amt: "0,00", cur: "USD",
        src: `fixture://resource/${i + 1}`, code: r[0]
      }));
    }
    if (mod.n === 116) {
      return [
        ["PLWAW→PELIM", "air", "GD/2026/00418", "noted"],
        ["PLWAW→DEHAM", "air", "GD/2026/00419", "noted"],
        ["FRAA→PLWAW", "air", "GD/2026/00420", "superseded"],
        ["PLWAW→USNYC", "air", "GD/2026/00421", "noted"],
        ["PELIM→PLWAW", "air", "GD/2026/00422", "noted"],
        ["PLGDY→PECLL", "air", "—", "odrzucony"]
      ].map((r, i) => ({
        id: `${mod.id}-${i + 1}`, ref: `LEG-AIR/${2026}/${String(80 + i).padStart(4, "0")}`,
        title: r[0], party: r[2], lane: r[0], status: r[3], amt: "0,00", cur: "USD",
        src: `fixture://shipment-leg/${i + 1}`, code: r[1]
      }));
    }
    if (mod.n === 205) {
      const kinds = ["commercial_invoice", "packing_list", "bill_of_lading", "export_declaration", "commercial_invoice", "packing_list"];
      const modes = ["ocean", "ocean", "ocean", "ocean", "air", "road"];
      return kinds.map((kind, i) => ({
        id: `${mod.id}-${i + 1}`, ref: `CHK/${2026}/${String(30 + i).padStart(4, "0")}`,
        title: kind, party: "export", lane: modes[i], status: i === 2 ? "nie" : "tak",
        amt: "0,00", cur: "USD", src: `fixture://document-checklist-rule/${i + 1}`,
        code: kind, role: "export", incoterm: "DAP", named_place: "Lima", trade_side: "export"
      }));
    }
    return null;
  }

  function seed(mod) {
    const spec = seedSpec(mod);
    if (spec) return spec;
    const fam = familyOf(mod);
    const p = parties();
    const lanes = ["PLGDY→PECLL", "CNSHA→PLGDY", "DEHAM→USNYC", "PLGDY→SGSIN", "PLPOZ→PELIM"];
    const codes = ["OFR", "BAF", "THC", "ISPS", "DOC"];
    const incos = ["DAP", "FOB", "CIF", "EXW", "CFR"];
    const st = fam === "rates"
      ? ["aktywna", "aktywna", "superseded", "aktywna", "aktywna", "aktywna"]
      : fam === "hitl"
        ? ["w recenzji", "powyżej 24 h", "oczekuje", "w recenzji", "oczekuje", "w recenzji"]
        : fam === "compliance"
          ? ["czysty", "do recenzji", "wstrzymany", "czysty", "do recenzji", "czysty"]
          : ["otwarty", "w toku", "gotowy", "zablokowany", "otwarty", "gotowy"];
    return Array.from({ length: 6 }, (_, i) => {
      const row = {
        id: `${mod.id}-${i + 1}`,
        ref: `${mod.id}/${2026}/${String(410 + i).padStart(5, "0")}`,
        title: `${mod.name} · wiersz ${i + 1}`,
        party: p[i % p.length],
        lane: lanes[i % lanes.length],
        status: st[i % st.length],
        amt: ["1 240,00", "8 442,00", "410,00", "2 040,00", "18 420,00", "3 480,00"][i],
        buy: ["1 100,00", "7 900,00", "380,00", "1 880,00", "16 200,00", "3 100,00"][i],
        sell: ["1 240,00", "8 442,00", "410,00", "2 040,00", "18 420,00", "3 480,00"][i],
        margin: ["140,00", "542,00", "30,00", "160,00", "2 220,00", "380,00"][i],
        cur: i === 2 ? "EUR" : "USD",
        src: `${mod.id}-SRC-${1000 + i}`,
        code: codes[i % codes.length],
        hs: i % 3 === 0 ? "brak" : "9403.60.00",
        incoterm: incos[i % incos.length],
        tax: ["5272859987", "1132337753", "5252348871", "20100123456", "DE812857193"][i % 5],
        role: ["klient", "agent", "armator", "broker", "przewoźnik"][i % 5],
        ksef: i % 2 ? "—" : `KSEF-2026-${410 + i}`,
        docs: `${4 + (i % 3)}/9`,
        recipient: ["omni_customs", "client_customs", "dest_agent", "armator"][i % 4],
        age: `${2 + i * 3} h`,
        vat: i % 2 ? "—" : `PL${5270000000 + i}`,
        eori: i % 3 ? "—" : `PL${5270000000 + i}000`,
        duns: i % 4 ? "—" : String(422074590 + i),
        tt: String(29 + (i % 6)),
        named_place: incos[i % incos.length] === "DAP" || incos[i % incos.length] === "DDP" ? "Lima" : ""
      };
      if (fam === "platform" || fam === "settings") row.src = `idem-${mod.n}-${i}`;
      if (mod.layer === "c" || PARK.has(fam)) row.status = i % 2 ? "named park" : "horyzont";
      return row;
    });
  }

  function rowsOf(mod) {
    if (!store[mod.id]) store[mod.id] = seed(mod);
    const q = (filters[mod.id] || "").toLowerCase();
    const all = store[mod.id];
    if (!q) return all;
    return all.filter((r) => Object.values(r).join(" ").toLowerCase().includes(q));
  }

  function moneyCell(amount, currency) {
    if (typeof window.money === "function") return window.money(amount, currency);
    return `${amount} ${currency}`;
  }

  function cell(col, r) {
    if (col.money) return `<td class="r">${moneyCell(r[col.k], r.cur)}</td>`;
    if (col.k === "ref") return `<td><button class="linkish" type="button" data-act="mod-open" data-id="${r.id}">${r.ref}</button></td>`;
    if (col.k === "src") return `<td><button class="linkish" type="button" data-act="mod-src" data-src="${r.src}">${r.src}</button></td>`;
    if (col.k === "status") {
      const cls = /blok|wstrzym|24|park|horyzont/.test(r.status) ? "alert" : "ok";
      return `<td><span class="chip ${cls}">${r.status}</span></td>`;
    }
    if (col.k === "hs" && r.hs === "brak") return `<td><span class="chip alert">brak</span></td>`;
    return `<td>${r[col.k] == null ? "—" : r[col.k]}</td>`;
  }

  function insp(mod) {
    const fam = familyOf(mod);
    const notes = {
      quote: "Warianty i luki. Send zablokowany bez HS. Marża na charge.",
      ship: "Strony, booking, stopy, paczki QR Omni, kontener ISO. Mapa AIS tylko na zleceniu oceanicznym.",
      hitl: "Accept/reject. ExtractionService nie zapisuje rate_line.",
      rates: "Niemutowalna. Zastąp = nowy wiersz + superseded_by.",
      charges: "Jedyny wiersz buy+sell. UI nie liczy marży.",
      party: "Lookup = szkic. NIP/VAT UE/EORI/DUNS unikalne · 409 z linkiem. Klient bez NIP = 400.",
      channels: "channel_quote: TT + najtańsza / najszybszy TT z SQL. Nie marża.",
      finance: "Kwota para z walutą. ksef_ref to pole, nie live HTTP.",
      customs: "document_dispatch_rule: adresat, nie send. Checklista U5 osobno (blocks_dispatch).",
      platform: "Zdarzenie / klucz. Brak kolumny kwoty.",
      compliance: "Werdykt, nie scoring osoby i nie kwota.",
      portal: "Chip horyzont / named park. Pełny flow makiety.",
      settings: "Kalendarz dni roboczych. is_working_day liczy SQL, nie JS."
    };
    const extra = {
      89: "booking_instruction: suggested → accept człowieka. Nie S21 / nie HTTP armatora.",
      99: "Adresat z reguły. Send leftover po S11. Nie auto-send.",
      106: "container_no ISO 6346 + iso_size_type. Nie VGM. Cyfrę kontrolną liczy serwer.",
      108: "organization_calendar. Święto = day_kind holiday. Nie V5 GPS.",
      111: "resource: vehicle / driver / trailer. trip ma opcjonalny slot — nie km.",
      116: "shipment_leg air. Lotnisko = port z airport w function_flags. Nie HAWB.",
      205: "document_checklist_rule. blocks_dispatch to dana, nie C8."
    };
    return `<div class="rsec"><h3>${mod.id}</h3>
      <p class="note">${extra[mod.n] || notes[fam] || "Pełny job makiety. Seed w sesji. RLS z paska."}</p>
      <p class="note">Warstwa: ${LAYER[mod.layer] || mod.layer}. Szablon: ${fam}.</p>
      <button class="fix" type="button" data-act="mod-new">Nowy rekord</button>
    </div>`;
  }

  function paint(mod) {
    const fam = familyOf(mod);
    const cols = colsFor(mod).filter((c) => !c.money || hasMoney(mod));
    const list = rowsOf(mod);
    const q = filters[mod.id] || "";
    const warn = mod.n === 14
      ? `<p class="note">Zakaz auto-scoringu natural_person / JDG (AI Act). Ocena tylko z karty i wywiadowni po HITL.</p>`
      : mod.n === 51
        ? `<p class="note">Odcinek ocean_lcl na zleceniu. Katalog linii LTL (groupage_line: cutoff_local, transit_days, ISODOW) jest na Lokalizacjach. Nie WMS.</p>`
        : mod.n === 56
          ? `<p class="note">Wniosek RODO access/erasure. Brak kolumny kwoty. Nie DPIA. Nie DELETE app_user.</p>`
          : mod.n === 111
            ? `<p class="note">Katalog floty. Przejazd (trip) ze statusem i opcjonalnym resource — nie km, nie mapa. Slot T2 na Zleceniu.</p>`
            : "";
    const park = (mod.layer === "c" || PARK.has(fam))
      ? `<span class="chip alert">horyzont / named park</span>`
      : "";
    const attach = (files[mod.id] || []).map((f) => `<li>${f.name} <span class="note">wskazanie M-38</span></li>`).join("");
    const head = cols.map((c) => `<th${c.money ? ' class="r"' : ""}>${c.t}</th>`).join("") + "<th></th>";
    const body = list.map((r) => `<tr>${cols.map((c) => cell(c, r)).join("")}<td><button class="btn" type="button" data-act="mod-open" data-id="${r.id}">Otwórz</button></td></tr>`).join("");
    $("#v-mod").innerHTML = `<div class="cmd">
      <button class="btn btn-p" type="button" data-act="mod-new">Nowy</button>
      <button class="btn" type="button" data-act="mod-edit">Edytuj wybrany</button>
      <button class="btn" type="button" data-act="mod-filter">Filtr</button>
      <button class="btn" type="button" data-act="mod-export">Eksport podglądu</button>
      <button class="btn" type="button" data-act="mod-file">Załącznik</button>
      <button class="btn" type="button" data-act="mod-mail">Szkic maila</button>
      ${HITL.has(fam) ? `<button class="btn" type="button" data-act="mod-hitl">HITL</button>` : ""}
      <span class="chip">${LAYER[mod.layer] || mod.layer}</span>
      <span class="chip">${fam}</span>
      <span class="chip">${mod.id} · RLS</span>
      ${park}
    </div>
    ${window.screenBanner(`${mod.id} · org z paska · makieta`, mod.name, extraBanner(mod))}
    ${window.screenFacts([
      { t: "Moduł", v: mod.id },
      { t: "Warstwa", v: LAYER[mod.layer] || mod.layer },
      { t: "Rekordy", v: String(list.length), s: q ? "po filtrze" : "seed sesji" },
      { t: "Kwoty", v: hasMoney(mod) ? "string z seedu" : "brak w BC" },
      { t: "Tenant", v: "z paska", s: "zero cross-tenant" }
    ], "n5")}
    <div class="pad" style="padding-top:0">${warn}
      ${q ? `<p class="note">Filtr: <b>${q}</b> · <button class="linkish" type="button" data-act="mod-filter-clear">wyczyść</button></p>` : ""}
      <div class="card xscroll" style="padding:0"><table class="grid"><thead><tr>${head}</tr></thead><tbody>${body || `<tr><td colspan="${cols.length + 1}">Brak wierszy po filtrze.</td></tr>`}</tbody></table></div>
      <p class="note" style="margin-top:var(--s3)">Załączniki sesji: ${attach ? `<ul class="kfiles">${attach}</ul>` : "brak — wskazanie, nie bajty."}</p>
      ${extraPanel(mod)}
    </div>`;
  }

  function extraBanner(mod) {
    if (mod.n === 89) return "Instrukcja bookingu na zleceniu. Status dane, nie S21.";
    if (mod.n === 99) return "Reguła adresata. Nie send.";
    if (mod.n === 106) return "Kontener ISO 6346. Nie VGM.";
    if (mod.n === 108) return "Dni robocze per kraj. is_working_day w SQL.";
    if (mod.n === 111) return "Pojazd / kierowca / naczepa. Nie trip w tym wierszu.";
    if (mod.n === 116) return "Odcinek air. Port bez flagi airport = odrzut.";
    if (mod.n === 205) return "Checklista dokumentów. blocks_dispatch = dana.";
    return "Lista, detal, zapis do seedu sesji. Puste pole = komunikat. LLM nie liczy.";
  }

  function extraPanel(mod) {
    if (mod.n === 111) {
      return `<div class="card" style="margin-top:var(--s4)">
      <h3 class="h-id">trip · T2</h3>
      <p class="note">Status + opcjonalny resource. Nie km. Nie mapa.</p>
      <table class="grid"><thead><tr><th>trip_no</th><th>status</th><th>vehicle</th><th>driver</th><th>trailer</th><th>source_ref</th></tr></thead>
      <tbody>
        <tr><td class="mono">TR/POZ/2026-0193</td><td><span class="chip ok">completed</span></td><td>Volvo FH 500</td><td>Piotr Zieliński</td><td>Krone 40HC</td><td>fixture://trip/1</td></tr>
        <tr><td class="mono">TR/LIM/2026-0144</td><td><span class="chip">planned</span></td><td>—</td><td>—</td><td>—</td><td>fixture://trip/2</td></tr>
      </tbody></table>
    </div>`;
    }
    if (mod.n === 108) {
      return `<div class="card" style="margin-top:var(--s4)">
      <h3 class="h-id">is_working_day</h3>
      <p class="note">Wynik z SQL na seedzie sesji. UI nie dodaje trzech dni.</p>
      <button class="btn" type="button" data-act="cal-working">Sprawdź PL 2026-11-11</button>
    </div>`;
    }
    return "";
  }

  function specFields(mod, row) {
    const src = { id: "source_ref", label: "source_ref", required: true, value: row?.src || "" };
    if (mod.n === 89) {
      return [
        { id: "ref", label: "Ref", required: true, value: row?.ref || "BI/2026/0013" },
        { id: "code", label: "booking_scope", type: "select", required: true, options: ["precarriage", "ocean", "oncarriage", "contact_exchange", "none"], value: row?.code || "ocean" },
        { id: "role", label: "target_role", type: "select", required: true, options: ["shipper", "consignee", "origin_agent", "dest_agent", "ocean_carrier", "omni_customs", "client_customs"], value: row?.role || "ocean_carrier" },
        { id: "status", label: "status", type: "select", required: true, options: ["suggested", "accepted", "sent", "confirmed", "rejected"], value: row?.status || "suggested" },
        src
      ];
    }
    if (mod.n === 99) {
      return [
        { id: "incoterm", label: "incoterm", type: "select", required: true, options: ["EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"], value: row?.incoterm || "DAP" },
        { id: "trade_side", label: "trade_side", type: "select", required: true, options: ["import", "export"], value: row?.trade_side || "export" },
        { id: "code", label: "document_kind", type: "select", required: true, options: ["commercial_invoice", "packing_list", "bill_of_lading", "export_declaration"], value: row?.code || "commercial_invoice" },
        { id: "recipient", label: "recipient_role", type: "select", required: true, options: ["shipper", "consignee", "origin_agent", "dest_agent", "ocean_carrier", "omni_customs", "client_customs"], value: row?.recipient || "omni_customs" },
        src
      ];
    }
    if (mod.n === 106) {
      return [
        { id: "ref", label: "container_no", required: true, value: row?.ref || "MSKU7823410", placeholder: "11 znaków ISO 6346" },
        { id: "code", label: "iso_size_type", required: true, value: row?.code || "45G1" },
        { id: "lane", label: "shipment (opcjonalnie)", value: row?.lane === "—" ? "" : (row?.lane || "") },
        src
      ];
    }
    if (mod.n === 108) {
      return [
        { id: "ref", label: "country_code", required: true, value: row?.ref || "PL" },
        { id: "title", label: "calendar_day", required: true, value: row?.title || "2026-09-08", placeholder: "RRRR-MM-DD" },
        { id: "code", label: "day_kind", type: "select", required: true, options: ["working", "holiday"], value: row?.code || "working" },
        src
      ];
    }
    if (mod.n === 111) {
      return [
        { id: "ref", label: "Ref", required: true, value: row?.ref || "RES/2026/0046" },
        { id: "code", label: "resource_kind", type: "select", required: true, options: ["vehicle", "driver", "trailer"], value: row?.code || "vehicle" },
        { id: "title", label: "display_name", required: true, value: row?.title || "" },
        { id: "lane", label: "registration_no", value: row?.lane === "—" ? "" : (row?.lane || "") },
        src
      ];
    }
    if (mod.n === 116) {
      return [
        { id: "ref", label: "Ref", required: true, value: row?.ref || "LEG-AIR/2026/0086" },
        { id: "lane", label: "origin→destination", required: true, value: row?.lane || "PLWAW→PELIM", placeholder: "PLWAW→PELIM" },
        { id: "party", label: "shipment_id", required: true, value: row?.party || "GD/2026/00418" },
        src
      ];
    }
    if (mod.n === 205) {
      return [
        { id: "incoterm", label: "incoterm", type: "select", required: true, options: ["EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"], value: row?.incoterm || "DAP" },
        { id: "trade_side", label: "trade_side", type: "select", required: true, options: ["import", "export"], value: row?.trade_side || "export" },
        { id: "lane", label: "mode", type: "select", required: true, options: ["ocean", "road", "rail", "air"], value: row?.lane || "ocean" },
        { id: "code", label: "document_kind", type: "select", required: true, options: ["commercial_invoice", "packing_list", "bill_of_lading", "export_declaration"], value: row?.code || "commercial_invoice" },
        { id: "status", label: "blocks_dispatch", type: "select", required: true, options: ["tak", "nie"], value: row?.status || "tak" },
        src
      ];
    }
    return null;
  }

  function fieldsFor(mod, row) {
    const spec = specFields(mod, row);
    if (spec) return spec;
    const fam = familyOf(mod);
    const base = [
      { id: "ref", label: "Ref", required: true, value: row?.ref || `${mod.id}/${2026}/00` },
      { id: "party", label: fam === "catalog" ? "Właściciel" : "Strona", required: true, value: row?.party || "" },
      { id: "status", label: "Status", required: true, value: row?.status || "otwarty" }
    ];
    if (fam !== "platform" && fam !== "compliance" && fam !== "settings") {
      base.splice(2, 0, { id: "lane", label: "Relacja / zakres", value: row?.lane || "" });
    }
    if (SOURCE.has(fam) || fam === "rates" || fam === "charges") {
      base.push({ id: "source_ref", label: "source_ref", required: true, value: row?.src || "" });
    } else {
      base.push({ id: "source_ref", label: "source_ref", value: row?.src || "" });
    }
    if (hasMoney(mod)) {
      base.push({ id: "amt", label: "Kwota (string z serwera)", value: row?.amt || "" });
      base.push({ id: "cur", label: "Waluta", required: true, value: row?.cur || "USD" });
    }
    if (fam === "finance") base.push({ id: "ksef", label: "ksef_ref", value: row?.ksef || "" });
    if (fam === "customs" || fam === "quote" || fam === "ship") {
      base.push({
        id: "incoterm", label: "incoterm", type: "select",
        options: ["EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"],
        value: row?.incoterm || "DAP"
      });
      base.push({
        id: "incoterms_version", label: "incoterms_version", type: "select",
        options: ["2020", "2010"],
        value: row?.incoterms_version || "2020"
      });
      base.push({
        id: "trade_side", label: "trade_side", type: "select",
        options: ["import", "export"],
        value: row?.trade_side || "export"
      });
      base.push({ id: "named_place", label: "named_place", value: row?.named_place || "Lima", placeholder: "named_place" });
    }
    if (fam === "channels") {
      base.push({ id: "tt", label: "transit_days", value: row?.tt || "32" });
    }
    if (fam === "party") {
      base.push({ id: "tax", label: "Tax ID / NIP", value: row?.tax || "" });
      base.push({ id: "vat", label: "VAT UE", value: row?.vat || "" });
      base.push({ id: "eori", label: "EORI", value: row?.eori || "" });
      base.push({ id: "duns", label: "DUNS", value: row?.duns || "" });
      base.push({ id: "role", label: "Role", value: row?.role || "customer", placeholder: "customer, vendor" });
      base.push({ id: "jdg", label: "JDG", type: "checkbox", value: row?.jdg === "1" ? "1" : "" });
    }
    return base;
  }

  function formValidate(mod, data, existingId) {
    const fam = familyOf(mod);
    if ((fam === "quote" || fam === "ship" || fam === "customs") && (data.incoterm === "DAP" || data.incoterm === "DDP") && !data.named_place) {
      return "409 · DAP/DDP wymaga named_place.";
    }
    if (mod.n === 106) {
      const no = (data.ref || "").replace(/\s/g, "").toUpperCase();
      if (no.length !== 11) return "409 · container_no musi mieć 11 znaków ISO 6346. Cyfrę kontrolną liczy serwer.";
    }
    if (mod.n === 108) {
      if (!/^[A-Z]{2}$/.test((data.ref || "").toUpperCase())) return "409 · country_code to ISO 2 liter.";
    }
    if (mod.n === 116) {
      const lane = (data.lane || "").toUpperCase();
      const air = ["PLWAW", "PELIM", "DEHAM", "USNYC"];
      const parts = lane.split("→").map((s) => s.trim());
      if (parts.length !== 2) return "409 · odcinek air: origin→destination.";
      if (!air.includes(parts[0]) || !air.includes(parts[1])) {
        return "409 · port bez flagi airport w function_flags. Nie HAWB.";
      }
      if (parts[0] === parts[1]) return "409 · start i koniec muszą być różne.";
    }
    if (mod.n === 111 && data.code === "trip") return "409 · trip to osobna tabela, nie resource_kind.";
    if (fam === "party") {
      if ((data.role || "").includes("customer") && !data.tax) {
        return "400 · klient bez NIP.";
      }
      const list = store[mod.id] || [];
      const taxHit = data.tax ? list.find((r) => r.id !== existingId && r.tax === data.tax) : null;
      if (taxHit) return `409 · tax_id zajęty — otwórz ${taxHit.party} (${taxHit.ref}).`;
      const vatHit = data.vat && data.vat !== "—"
        ? list.find((r) => r.id !== existingId && r.vat === data.vat)
        : null;
      if (vatHit) return `409 · VAT UE zajęty — otwórz ${vatHit.party} (${vatHit.ref}).`;
    }
    return "";
  }

  function upsert(mod, data, existingId) {
    const list = store[mod.id] || (store[mod.id] = seed(mod));
    if (existingId) {
      const row = list.find((r) => r.id === existingId);
      if (!row) return;
      Object.assign(row, {
        ref: data.ref, party: data.party || data.title || row.party, status: data.status || row.status,
        lane: data.lane || row.lane, src: data.source_ref || row.src, amt: data.amt || row.amt, cur: data.cur || row.cur,
        ksef: data.ksef || row.ksef, incoterm: data.incoterm || row.incoterm, tax: data.tax || row.tax,
        vat: data.vat || row.vat, eori: data.eori || row.eori, duns: data.duns || row.duns,
        role: data.role || row.role, tt: data.tt || row.tt, title: data.title || row.title,
        code: data.code || row.code, recipient: data.recipient || row.recipient,
        named_place: data.named_place != null ? data.named_place : row.named_place,
        trade_side: data.trade_side || row.trade_side,
        incoterms_version: data.incoterms_version || row.incoterms_version
      });
      applySpec(mod, row, data);
      return;
    }
    list.unshift({
      id: `${mod.id}-${Date.now()}`,
      ref: data.ref,
      title: data.ref,
      party: data.party,
      lane: data.lane || "—",
      status: data.status,
      amt: data.amt || "0,00",
      buy: data.amt || "0,00",
      sell: data.amt || "0,00",
      margin: "—",
      cur: data.cur || "USD",
      src: data.source_ref || `${mod.id}-SRC-NEW`,
      code: data.code || "OFR",
      hs: "brak",
      incoterm: data.incoterm || "DAP",
      tax: data.tax || "—",
      vat: data.vat || "—",
      eori: data.eori || "—",
      duns: data.duns || "—",
      role: data.role || "klient",
      tt: data.tt || "—",
      named_place: data.named_place || "",
      trade_side: data.trade_side || "export",
      incoterms_version: data.incoterms_version || "2020",
      ksef: data.ksef || "—",
      docs: "0/9",
      recipient: data.recipient || "omni_customs",
      age: "0 h"
    });
    applySpec(mod, list[0], data);
  }

  function applySpec(mod, row, data) {
    if (mod.n === 89) {
      row.code = data.code || row.code;
      row.role = data.role || row.role;
    }
    if (mod.n === 99) {
      row.recipient = data.recipient || row.recipient;
      row.code = data.code || row.code;
      row.role = data.trade_side || row.role;
    }
    if (mod.n === 106) {
      row.ref = (data.ref || row.ref).replace(/\s/g, "").toUpperCase();
      row.title = row.ref;
    }
    if (mod.n === 108) {
      row.ref = (data.ref || row.ref).toUpperCase();
      row.title = data.title || row.title;
      row.code = data.code || row.code;
      row.status = row.code === "working" ? "tak" : "nie";
    }
    if (mod.n === 111) {
      row.title = data.title || row.title;
      row.party = row.title;
      row.code = data.code || row.code;
      row.lane = data.lane || row.lane || "—";
    }
    if (mod.n === 116) {
      row.code = "air";
      row.lane = (data.lane || row.lane).toUpperCase();
    }
    if (mod.n === 205) {
      row.code = data.code || row.code;
      row.lane = data.lane || row.lane;
      row.role = data.trade_side || row.role;
      row.status = data.status || row.status;
    }
  }

  function openRow(mod, id) {
    const row = (store[mod.id] || []).find((r) => r.id === id);
    if (!row) return;
    const K = window.OR_KERNEL;
    const rows = [
      { k: "Ref", v: row.ref },
      { k: "Strona", v: row.party },
      { k: "Status", v: row.status },
      { k: "source_ref", v: row.src }
    ];
    if (row.lane) rows.splice(2, 0, { k: "Relacja", v: row.lane });
    if (hasMoney(mod)) rows.push({ k: "Kwota", v: `${row.amt} ${row.cur}` });
    if (row.ksef) rows.push({ k: "ksef_ref", v: row.ksef });
    if (row.incoterm) rows.push({ k: "Incoterm", v: row.incoterm });
    if (row.named_place) rows.push({ k: "named_place", v: row.named_place });
    if (row.trade_side) rows.push({ k: "trade_side", v: row.trade_side });
    if (mod.n === 89) {
      rows.push({ k: "booking_scope", v: row.code });
      rows.push({ k: "target_role", v: row.role });
    }
    if (mod.n === 99) rows.push({ k: "recipient_role", v: row.recipient });
    if (mod.n === 106) rows.push({ k: "iso_size_type", v: row.code });
    if (mod.n === 108) rows.push({ k: "is_working_day (SQL)", v: row.status });
    if (mod.n === 111) rows.push({ k: "resource_kind", v: row.code });
    if (mod.n === 116) rows.push({ k: "leg_kind", v: "air" });
    if (mod.n === 205) rows.push({ k: "blocks_dispatch", v: row.status });
    K.detail({
      title: row.ref,
      note: `${mod.id} · ${mod.name} · tenant z paska`,
      rows,
      actions: [
        { act: "mod-edit", label: "Edytuj", attrs: `data-id="${row.id}"` },
        { act: "mod-mail", label: "Szkic maila", attrs: `data-id="${row.id}"` }
      ]
    });
  }

  function handle(act, el, mod) {
    if (!mod || !window.OR_KERNEL) return false;
    const K = window.OR_KERNEL;
    if (act === "cal-working") {
      K.blocked("is_working_day = false · PL 2026-11-11 · day_kind holiday. Wynik z SQL, nie z JS.");
      return true;
    }
    if (act === "mod-filter-clear") {
      filters[mod.id] = "";
      paint(mod);
      return true;
    }
    if (act === "mod-filter") {
      K.form({
        title: "Filtr " + mod.id,
        note: "Filtr w ramach jednego tenanta, na seedzie sesji.",
        fields: [{ id: "q", label: "Szukaj", value: filters[mod.id] || "", placeholder: "ref, strona, status…" }],
        saveLabel: "Zastosuj",
        onSave: (d) => { filters[mod.id] = d.q || ""; paint(mod); }
      });
      return true;
    }
    if (act === "mod-export") {
      const fam = familyOf(mod);
      const cols = colsFor(mod).filter((c) => !c.money || hasMoney(mod));
      K.exportCsv(
        `${mod.id}-podglad.csv`,
        cols.map((c) => c.t),
        rowsOf(mod).map((r) => cols.map((c) => r[c.k] == null ? "" : r[c.k]))
      );
      return true;
    }
    if (act === "mod-file") {
      K.pickFile((f) => {
        (files[mod.id] = files[mod.id] || []).push(f);
        paint(mod);
        if (typeof window.toast === "function") window.toast(`Załączono ${f.name} — wskazanie, nie bajty (M-38).`);
      });
      return true;
    }
    if (act === "mod-mail") {
      K.mail({
        to: "anna@spedbaltyk.pl",
        subject: `${mod.id} · ${mod.name}`,
        body: `Proszę o uzupełnienie rekordu w ${mod.id}. Tenant z paska. HITL przed zapisem.`
      });
      return true;
    }
    if (act === "mod-src") {
      K.detail({
        title: "source_ref",
        note: "Pochodzenie. Bez niego rekord nie wchodzi.",
        rows: [{ k: "Źródło", v: el.dataset.src || "—" }, { k: "Moduł", v: mod.id }]
      });
      return true;
    }
    if (act === "mod-hitl") {
      K.confirm({
        title: "HITL · " + mod.id,
        note: "Nic z ekstrakcji nie wchodzi bez akceptacji.",
        text: "Zaakceptować szkic i zapisać wskazanie w seedzie sesji? ExtractionService nie woła innych BC.",
        onAccept: () => { if (typeof window.toast === "function") window.toast("Accept — seed sesji. Nie produkcja."); }
      });
      return true;
    }
    if (act === "mod-open") {
      openRow(mod, el.dataset.id);
      return true;
    }
    if (act === "mod-new") {
      const fam = familyOf(mod);
      K.form({
        title: "Nowy · " + mod.id,
        note: HITL.has(fam) ? "Lookup / extract = szkic. Zapis po potwierdzeniu." : "Zapis do seedu sesji.",
        fields: fieldsFor(mod, null),
        hitl: HITL.has(fam),
        requireSource: SOURCE.has(fam),
        validate: (d) => formValidate(mod, d),
        onSave: (d) => {
          upsert(mod, d);
          paint(mod);
          if (typeof window.toast === "function") window.toast("Zapisano w sesji makiety.");
        }
      });
      return true;
    }
    if (act === "mod-edit") {
      const id = el.dataset.id || (store[mod.id] && store[mod.id][0] && store[mod.id][0].id);
      const row = (store[mod.id] || []).find((r) => r.id === id);
      if (!row) {
        K.blocked("Brak wybranego rekordu do edycji.");
        return true;
      }
      const fam = familyOf(mod);
      if (fam === "rates" && row.status === "superseded") {
        K.blocked("Wiersz superseded jest niemutowalny. Zmiana = nowy rekord.");
        return true;
      }
      K.form({
        title: "Edycja · " + row.ref,
        note: fam === "rates" ? "Stawki niemutowalne — tu makieta pokazuje nowy wiersz po zapisie." : "Zapis do seedu sesji.",
        fields: fieldsFor(mod, row),
        hitl: HITL.has(fam),
        requireSource: SOURCE.has(fam),
        validate: (d) => formValidate(mod, d, row.id),
        onSave: (d) => {
          if (fam === "rates") {
            row.status = "superseded";
            upsert(mod, d);
          } else {
            upsert(mod, d, row.id);
          }
          paint(mod);
          if (typeof window.toast === "function") window.toast(fam === "rates" ? "Nowy rate_line + superseded_by." : "Zapisano w sesji.");
        }
      });
      return true;
    }
    return false;
  }

  return { paint, insp, handle, familyOf, hasMoney, store };
})();
