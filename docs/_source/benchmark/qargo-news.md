Zaczynam research artykułów Qargo — najpierw sprawdzę listing News & Blogs i sitemapy, żeby zebrać pełny inwentarz.

I'm mapping out the plan for researching Qargo's blog: first building a full inventory of articles across all pagination pages, then diving deeper into 15-25 of the most substantive ones to extract specifics on customer expectations for TMS and what solutions Qargo offers in response.

I'll also need to trace how the regulatory landscape is shifting—e-invoicing, eCMR/eFTI, CO2/CSRD/GLEC, AI Act, Mobility Package, cabotage, NIS2, customs and Brexit—plus where the product roadmap is heading for 2025-2026, with special attention to anything touching corporate clients like shippers and control tower visibility. The final report needs to be in Polish, 2000-3000 words, organized into these thematic sections plus an article inventory at the end. Now I'm starting to fetch the listing pages and sitemaps to gather the source material.

---

The article list seems to load dynamically via JavaScript, and the sitemap.xml returned an error, so I'm going to try alternate paths like the CMS subdomain's sitemap, WordPress-specific sitemap formats, and different pagination patterns since this looks like a WordPress site.  Actually, articles live under a /post/ path, and I realize the REST API endpoint for posts could give me everything I need directly, including dates, so that's worth trying first.
Widzę, że karty artykułów są renderowane JavaScriptem, ale to WordPress z postami pod `/post/...`. Sprawdzę mapę strony (Yoast/WP) oraz REST API WordPressa, żeby szybciej uzyskać pełny inwentarz treści.

---

Sitemapy zwracają błąd 500. Sprawdzam REST API WordPressa i robots.txt.

Since the sitemaps are returning 500 errors, I'll try hitting the WordPress REST API and some pagination variants instead, and check robots.txt to see if it points to the actual sitemap location.

---

Robots.txt potwierdza sitemap pod `sitemap_index.xml` (Yoast), ale WebFetch dostaje 500 — pewnie blokada user-agenta. Spróbuję pobrać sitemapę przez curl z przeglądarkowym user-agentem.

The listing page is empty since it's JS-rendered, the REST API returns 404, and the sitemap index gives a 500 through WebFetch. Robots.txt still points to the Yoast-style sitemap at qargo.com, so the 500 might just be a user-agent issue with WebFetch — I'll try curl with a browser-like user agent instead, and also check for a post-sitemap.xml.

---

Sitemap działa przez curl. Pobieram `post-sitemap.xml` z pełną listą artykułów.

Good, the sitemap index confirms curl works. Now I'll fetch post-sitemap.xml to get the full list of blog posts with their lastmod dates.

---

Mam pełną sitemapę postów. Filtruję do głównych wersji angielskich (`/post/...`), bo wersje `/fr/`, `/nl-NL/`, `/us/` to tłumaczenia/duplikaty.

I've got the post sitemap, though it was truncated around 20000 characters. I'm filtering out the language-prefixed duplicates (/fr/, /nl-NL/, /nl/, /us/) to keep just the main English post URLs, and noting a gap in the truncated section that I may need to re-check since it landed near some duplicate /us/ entries.

---

Mam 57 głównych angielskich postów. Sprawdzam jeszcze, czy wersje `/us/` i `/nl-NL/` zawierają unikalne artykuły, których nie ma w głównym serwisie.

I've got 57 English posts from the main site, so now I'm cross-checking the /us/ variants to see which ones aren't duplicates of those already found.

That English post might live under a different slug on the main site, or be exclusive to /us/. I should also check for NL-only pages like the April 2026 qargo-intelligence-nederland piece, then cross-reference the /us/ slugs against the main-site list to spot the differences.

---

Adding up the unique posts, I'm counting 57 main English articles plus one US-only piece and one NL-only piece, giving roughly 59 total, which lines up with the 10 pagination pages at about 6 per page. Now I need to compile title, date, and short description for each entry, then pull the full content for the ones that matter most.

Since the sitemap's lastmod isn't a reliable publication date, I'll pull each article page directly since those should show the actual publish date. Rather than doing 59 separate fetches, the smarter approach is downloading all the pages locally in bulk, then parsing out the titles, meta descriptions, and JSON-LD publish dates from the saved HTML afterward, only reading the full text for the 15-25 most substantive ones. I'm putting together a script to grab all the English posts plus the two unique regional ones into a temp folder for parsing.
Mam już pełen inwentarz: 57 głównych postów EN, 1 unikalny US (`tms-integrations`) i 1 unikalny NL (`qargo-intelligence-nederland`) — razem 59 artykułów, co zgadza się z ~10 podstronami listingu. Teraz pobiorę lokalnie wszystkie strony artykułów i wyciągnę tytuły, daty publikacji oraz opisy meta.

---

Wszystkie 59 artykułów pobrane. Wyciągam tytuły, daty publikacji i opisy z metadanych.

All 59 articles are downloaded now, totaling 5.7 MB. I need to extract the title, publish date, and meta description from each HTML file, so I'm writing a PowerShell script to parse that data out.



---

Now I have the full inventory of 59 articles spanning dates from late 2022 through 2026, despite some encoding artifacts with special characters. Next I need to select the 15-25 most substantive pieces to read in full.

For regulatory content, I'm picking articles on Peppol e-invoicing (guides, France reform, future outlook), NIS2 compliance for road transport, the Netherlands kilometre charge, e-CMR/Transfollow integration, and sustainability reporting pieces covering CO2 and GLEC data. For product, AI, and USP angles, I'm selecting the Qargo Intelligence launches, email AI features, TMS automation, the "transport-savvy AI" piece, workflow content, 2026 logistics trends, and the comparison against legacy systems, along with the Series B funding announcement.

Now I'm scanning customer pain points and visibility topics — hidden costs of manual operations, container operator challenges, empty miles, and customer portal/tracking-link content that speaks to corporate visibility needs, plus the CLDN and Kinaxia partnership stories and the pallet network workshop piece.

Since I have all the HTML files locally, I want to extract just the article body text, stripping the shared navigation and footer noise that repeats across pages. I'm planning to check one file's structure first to find where the actual content container starts and ends, likely between the "Book Demo" nav marker and the "Go further with Qargo" footer marker, so I can write a script to pull clean article text from each page.
Mam pełny inwentarz 59 artykułów z okresu wrzesień 2022 - wrzesień 2026. Teraz sprawdzę strukturę HTML, żeby wyciągnąć sam korpus tekstu z ~25 najbardziej merytorycznych artykułów (regulacje, AI, premiery, case'y).

---

I'll write a script to extract text from the main content container, stripping HTML tags, decoding entities, and normalizing whitespace, then run it across all 59 files into plain .txt versions before reading the important ones.



---

Wszystkie artykuły skonwertowane na tekst. Czytam teraz pełną treść kluczowych artykułów — zaczynam od bloku regulacyjnego (NIS2, Peppol, e-fakturowanie Francja, eCMR, myto NL).

With all articles converted to text, I'm planning to read through them in batches, starting with those most relevant to the regulatory question—covering NIS2, e-invoicing reform, Peppol standards, and road charging developments.

Next I'll move to the AI and product batch, covering Qargo's intelligence features and automation capabilities, followed by funding and market positioning articles about the Series A/B rounds and competitive advantages against legacy systems.

Finally I'll dig into customer and corporate content, including partnerships, sustainability initiatives, and container operator challenges to round out my understanding of Qargo's business.

That gives me 28 files total—solid coverage. Since each file is fairly small, I'll read them in parallel batches to speed things up.

---

Świetny materiał regulacyjny. Czytam kolejne: przyszłość Peppol, eCMR/TransFollow, myto kilometrowe NL i digitalizację dokumentów.

I'm going through the three regulatory articles, noting that NIS2 is the EU cybersecurity directive replacing NIS with size-based thresholds, and comparing how Belgium, the Netherlands, and France differ in their transposition timelines and deadlines.

Transport is explicitly named as a sector under NIS2, splitting into essential entities like road authorities versus important entities like freight forwarders, with requirements covering risk management, incident reporting timelines, management liability, and supply chain due diligence—and I'm noting how Qargo aligned with ISO 27001/NIS2 through MFA, RBAC, SSO, and breach notification commitments.

For France's e-invoicing reform, I'm tracking the phased CTC model rollout starting September 2026 for receiving and issuing obligations by entity size, the Plateforme Agréée and PPF infrastructure, supported formats like Factur-X and UBL, and the modest per-invoice penalty structure.

Now I'm looking at transport-specific invoicing complexities—multi-party subcontracting chains generating several invoices per route, reverse-charge rules for intracommunity transport, and the continued validity of paper CMR documents—which makes automation essential given the volume, and how Qargo's partnership with B2BRouter handles both Peppol invoicing and DGFiP tax reporting in one step.

Then I'm reviewing the Peppol mandate details for Belgium starting January 2026, the goals around fraud reduction and payment speed, the UBL format requirements, common customer worries about system changes and added admin burden, and how Qargo built in Peppol support with existing accounting integrations to minimize disruption.

Next I'll move through the remaining articles: Peppol invoicing, the future of Peppol, the Dutch truck kilometre charge, Qargo's eCMR partnership with Transfollow, and digitalizing transport documents.

---

Blok regulacyjny prawie kompletny. Czytam teraz artykuły o AI i produkcie (Qargo Intelligence, Email Intelligence, workflow AI, trendy 2026).

I'm noting the regulatory push toward e-invoicing across France, Netherlands, and Poland's KSeF mandate, and how these same data standards are likely to extend into transport orders, subcontractor flows, and CO₂ reporting—which lines up with Qargo's positioning around AI invoice matching and interconnected workflows. I'm also starting to look into TransFollow's eCMR standard.

Also solves POD/CMR bottlenecks: signed eCMR triggers invoicing automatically, GPS-timestamped signatures settle damage disputes, and customs/CO₂ records become structured data. The TransFollow flow has dispatchers creating the eCMR from the consignment, drivers tapping "Sign eCMR" in the Qargo app, with status states moving through draft, issued, in transit, delivered, cancelled.

Moving on to the next batch covering AI and product articles.

---

Bardzo bogaty materiał. Czytam teraz finansowanie (Series A/B), porównanie z legacy TMS i ukryte koszty operacji manualnych.

I'm noting the details of the Qargo Intelligence launch from December 2024 — the quality control, document intelligence, and email intelligence features, along with their claimed time-savings metrics like reclaiming 75% of admin time and cutting email work in half.

Then I'm moving to the July 2025 AI-powered TMS announcement centered on "Qi," which handles order entry from PDFs and emails, quote generation, purchase invoicing cross-checks, document processing, and a color-coded quality control system, all positioned as augmenting rather than replacing human decision-making. I'm also picking up the start of a January 2026 piece on logistics trends for the coming year.

Now I'm working through the four 2026 trends: sustainability (CO₂ tracking, empty miles), AI moving toward automate-and-review with agentic booking capabilities, compliance around NIS2 and ISO certification, and connectivity via integration partners, plus advice on tracking time-to-invoice and empty miles as KPIs. Then I'm noting a June 2026 update introducing an Outlook add-on for order forwarding and a new AI agent letting customers self-configure rules without vendor engineering tickets.

Rules can assign planning groups and sequences based on constraints like vehicle capacity, stop durations, and ETAs, though planning boards aren't AI-powered yet — that's flagged as a future direction. POD auto-matching and purchase invoicing automation reportedly cut invoice-processing time by up to 65%. Now I'm moving to a third batch covering funding, differentiation, and market positioning: Series B/A funding announcements, Qargo versus legacy systems comparisons, the hidden costs of manual transport operations, and TMS ROI.

---

Świetne dane. Teraz artykuły pod kątem klienta korporacyjnego i głosu klientów: CLdN (multimodal), Kinaxia, portal klienta, tracking links, warsztat Qargo Unlocked.

I'm noting the Series B details: $33M raised led by Sofina and Balderton, bringing the total to $54M, with customer base quadrupling and revenue growing 5x across six European markets in 18 months. Invoicing volume through the platform jumped from £420M to £1.9B annually, and Qargo Intelligence handles automation across order creation, routing, trip optimization, load building, invoicing, and warehouse scheduling.

Also capturing security certifications (ISO 27001, Google Cloud infrastructure), the Qargo Network for subcontracting work-sharing, founding details (2020, serving carriers/freight forwarders/3PLs), and the earlier Series A round of €12M led by Balderton with founders Adriaan Coppens, Joeri de Turck, and Sander de Wilde, plus customer results like Anglia Freight saving 200,000 miles annually.

Now expanding on Qargo's operations across Belgium, Ireland, Netherlands, and the UK — customers Altrea Group and Uniserve Group tripled their ARR, and by March 2024 the platform handled 175,000 journeys with 3,000+ trucks daily and £35M invoiced. I'm also noting the customer portal with deep shipper integrations for real-time visibility, which feels like a strong corporate/enterprise angle.

Comparing Qargo against legacy systems, I'm listing the pain points of manual retyping, delayed invoices, and lack of CO2/CSRD reporting, alongside stats showing 81% of transport SMEs worried about rising costs in 2025. I'm gathering the efficiency metrics — time saved per planner, invoice processing improvements, job accuracy rates — plus GLEC/ISO-aligned emissions tracking and customer testimonials from Kees in 't Veen and FMC Haulage.

I'm continuing to compile more customer quotes from Jacobs, Anglia Freight, PE Express, Uniserve, and Roosenboom representatives, alongside the note about weekly product updates.

Now I'm working through the hidden cost analysis: late invoicing scenarios showing £160,000 in uninvoiced receivables, empty miles calculations demonstrating £73,728 in potential fuel savings from a 30% reduction, and the Van 't Kruis case study showing over 5 hours weekly saved on invoice syncing.

I'm noting common objections like "we've always done it this way" and the value of spreadsheet flexibility, plus the importance of margin visibility per job, route, and customer, and the ROI calculator tool.

Now I'm moving to batch 4, covering corporate and customer-facing articles including CLdN, Kinaxia, the customer portal, tracking links, Qargo Unlocked, empty-miles content, container operator challenges, and TMS ROI.

---

Czytam kolejne: puste kilometry, wyzwania operatorów kontenerowych, ROI z TMS i zrównoważony raport (BILOG/CO2).

I'm noting the CLdN case study details—Qargo going live for multimodal cargo covering sea, rail, and road with full order-to-pay, replacing a TMS dating back to 2007. There's a slight date discrepancy to flag between the article's publish date and the stated project kickoff timing.

The customer portal update from March 2026 adds self-service order management with AI-assisted document upload, configurable approval workflows with cutoff times, and real-time pallet tracking visibility.

The April updates cover time-limited tracking links (allowing one-off recipients to view shipment status without logging in) and the launch of "Qargo Unlocked," a customer event series highlighting pallet network integrations, with Wyvern Cargo's Simon Sparrowhawk speaking about running Qargo across two live networks, each requiring nine distinct data flows.

Next I want to go through the remaining key articles — empty-miles, container operator challenges, TMS ROI, route optimisation and sustainability, the BILOG piece, Kinaxia, email intelligence, transport AI, plus short-sea/bulk pain points and the Peppol invoicing piece on Belgian specifics — reading them in a batch.



---

Kontynuuję pogłębioną lekturę: Kinaxia (duża grupa UK), Peppol w Belgii (szczegóły), optymalizacja tras pod CO2 i short sea.

I'm noting that UK empty running hit 31% in 2025 versus the EU's 25.9%, essentially one in three UK lorry miles running empty compared to one in four across the EU. This stems from a data visibility problem—disconnected TMS systems between shippers, carriers, and brokers, late confirmations, and shippers not sharing forward demand—which points toward a three-step fix starting with making the problem visible through dashboards.

For container operators, I'm seeing three recurring pain points: juggling too many disconnected systems just to check a container release, wasted trips from failed collections and empty backhauls, and heavy admin burden from tracking 20+ data points per order plus chasing PODs and customs paperwork. Qargo's approach integrates with ferry and port/terminal systems while investing in AI agents for terminal booking automation.

On TMS ROI, I'm mapping out the five value levers—admin automation, charge leakage recovery, subcontractor invoice verification, shipment exception handling, and reporting overhead.

For the BILOG piece, I'm noting the VIL Flanders innovation project partners and how it connects CSRD's Scope 3 emissions reporting requirements to Qargo's platform, which calculates CO2 at both order and trip level using modeled and actual fuel data.

I still have a few more articles to check before wrapping up.

Also noting the NL-only AI launch with the vrachtwagenheffing angle, the fuel surcharge dashboard, and WhatsApp integration. That's already 16 articles covered in depth, so I'll batch through a few more high-value ones next—Kinaxia, Peppol invoicing, sustainability-focused route optimization, short-sea, bulk transport, the smarter route optimization piece, and a quick scan of the configuration/scaling content and case studies—to round out the 15-25 range the task calls for.

---

Ostatnia tura pogłębionej lektury: optymalizacja tras (wyniki 6–8%), wyzwania bulk, "transport-savvy AI" i Dzień Logistyki (współpraca w łańcuchu).

I'm noting Kinaxia's profile: a major UK logistics operator with around 1,000 vehicles serving retail, leisure, manufacturing, and food sectors. They're using Samsara telematics with Qargo TMS to improve OTIF, standardize order intake and EDI, and integrate finance, while also focusing on sustainability through reduced pallet touches, better vehicle fill, and fewer empty miles.

Now I'm looking at the Belgium Peppol invoicing mandate — testing through 2024-2025, becoming mandatory for all B2B invoices in 2026 regardless of fleet size, requiring every business to have a Peppol Access Point. There are common concerns around TMS readiness, accounting integrations (Adsolut, Adfinity, Exact Online, Sage, Xero), and whether subcontractors are affected too, with input from Qargo's Integration Platform Lead.

I'm also tracking the CSRD sustainability reporting changes — the Omnibus I Directive adopted in February 2026 significantly narrowed the scope, now only applying to companies with 1,000+ employees and €450M+ turnover, pushing first reports to 2028 and excluding roughly 80% of previously in-scope companies.

Despite the narrower CSRD scope, shippers still need Scope 3 emissions data and are asking carriers for verified per-shipment figures using GLEC or ISO 14083 methodology, adjusted by vehicle type — carriers who can't provide clean CO₂ data risk losing tenders to those who can, a point echoed by Handico Trucking's Head of Digital Development, with Qargo integrating PTV Logistics and Optimize for this.

I'm also noting the short sea shipping pain points — ferry bookings scattered across multiple portals causing manual rekeying and storm disruptions, and how Qargo addresses this with a 'Send to Ferry Portal' feature, an intermodal booking screen, bulk rebooking to alternate departures, and handling of PBN/GMR references alongside customs complexities like MRNs, GMR, PBN, declaration types, and the GB-NI route trap where NI postcodes need auto-detection due to GB country code issues.

I'm noting the ferry invoice reconciliation and VGM/gross weight audit trail as well. Scanning through the remaining list — smarter route optimisation with 6-8% mileage savings, transport-savvy AI, email intelligence, the 2022 seed round, several customer case studies, and various product and culture articles — I've deep-read 20 articles so far and plan to pick at most 5 more for deep reading, relying on meta descriptions for the rest.

For the remaining questions, I'm prioritizing by theme: customer expectations from the smarter-route-optimisation piece, bulk transport challenges, and invoicing pain points; USP signals from transport-savvy-ai and the TMS scaling/configuration articles; product direction from the Netherlands AI launch piece; and corporate angle from the national logistics day and Clarus WMS integration articles. I'll batch-read the route optimisation, bulk challenges, transport-savvy-ai, and national logistics day articles next.

Actually since I already have meta descriptions covering the inventory needs, I'll do four full reads plus scan the remaining files for customer quotes and key figures to enrich the invoicing and Netherlands AI launch entries.

---

Mam pogłębioną lekturę 24 artykułów. Szybki przegląd pozostałych pod kątem cytatów, liczb i konkretów, których jeszcze nie mam.

I'm noting the route optimisation feature from August 2025, including the planners' skepticism about automation replacing their local knowledge, alongside the multi-drop sequencing capabilities and integrations with telematics providers like Samsara and Webfleet, plus pallet network partners like Palletforce and Palletline.

Now I'm looking at Anglia Freight's results—a 6-8% mileage reduction saving 200,000+ miles yearly and cross-dock scanning saving 20+ minutes per vehicle daily, quoted from their Director Pete Holden.

Then I'm examining the bulk transport pain points from mid-2026: scattered data across weighbridge tickets and WhatsApp groups causing demurrage disputes and unclear lane profitability, plus compliance requirements around Qualimat, ADR hazmat certifications, and multi-compartment cleaning documentation, along with how Qargo addresses these through ADR compatibility checks, compartment setup, and a document library for cleaning certs and MSDS/GMP+ records.

I'm noting the automatic expiry monitoring and mandatory driver tasks tied into EU working hours calculations, plus customer quotes from Van Tiel Transport and Kees in 't Veen. Then I shift to the transport-savvy AI piece from June 2025—pushing back against superficial AI hype in favor of tools co-developed with planners, covering order parsing from PDFs/emails/EDI, business rule validation, POD matching, and separate feature sets for carriers (job suggestions, dashboards) versus forwarders (live updates, exception alerts, customer portals), with explainability as a core selling point.

Now I'm on National Logistics Day 2026 content—collaboration and subcontractor portals with unified logins, color-coded trip statuses, ETA updates, and document uploads, framed around transparency demands from customers and regulators. With 24 articles covered, I'm within my target range, so I'm doing a final pass across the remaining files to pull any additional numbers or quotes worth citing.

Meta descriptions should suffice for most inventory entries, though a few files stand out for extra depth—Netherlands intelligence launch tied to upcoming heavy vehicle taxes, empty container cost figures, cash flow impact of connected TMS, day/week-based costing philosophy, and security specifics from the ISO certification and data protection pieces. I'll grep for quotes and key numbers across the remaining files to pull those details out efficiently.

---

Jeszcze skrót z kilku pozostałych (Nolize, ISO 27001, Email Intelligence, planning board, Qi w Holandii, on-prem vs cloud).

I'm noting more useful details: Moran Logistics, a major UK food distribution fleet, adopted Qargo in 2025 with sites going live that spring; empty container repositioning costs the industry over $20 billion annually; and the 2022 seed round of $6M was led by Fred Destin at Stride.VC with participation from experienced operators like Stephane Kurgan and Breon Corcoran. I'm also starting to look into Groupe Sudre as a family-owned transport group.

Now I'm gathering more customer and product details: Trezzini, a French haulage company founded in 2019 that grew rapidly to nearly 50 trucks; a resource costing feature that works at day/week granularity instead of just per-trip; TMS integrations expanding into the US market; a fuel surcharge dashboard with index-linked calculations; and WhatsApp Business integration for replying to messages directly in Qargo. I still need to check a handful of remaining articles I haven't fully covered yet, like the email intelligence feature, ISO 27001 certification, planning board optimization, and a few customer case studies.

---

Mam komplet: 59 unikalnych artykułów zinwentaryzowanych (57 EN + 1 tylko US + 1 tylko NL; wersje FR/NL/US to tłumaczenia), z czego ~25 przeczytałem w całości. Piszę raport.

I'm now piecing together the full profile: Nolize as a French forwarder based in Lyon and Valenciennes focused on visibility, efficiency, and secure partner exchanges through automation, their ISO 27001 certification from March 2025, and their Email Intelligence tool launched in September 2024 that links emails to orders with plans for generative AI features.

Other pieces I'm compiling include the planning board with customizable boards, Qi's Dutch market launch tied to personnel shortages and the upcoming vrachtwagenheffing, cloud versus on-prem comparisons favoring cloud, Scales' subscription model with all new releases included, and Earth Day content on emissions transparency becoming a contractual requirement.

I've now deep-read or scanned around 40 articles with 24 full reads, and I still need to verify whether any content directly addresses shippers — checking mentions of shipper system integrations, CO2/Scope 3 data requests, and empty miles discussions from the shipper's perspective.

Confirming Qargo's actual customer segments are carriers, freight forwarders, and 3PLs rather than shippers themselves — there's no control tower product, just customer portals and tracking links that give shippers visibility indirectly through their carrier. I'm also noting the US expansion messaging and Series B language about staying independent while partnering across company sizes, plus cross-checking the sitemap's 59-article count against the pagination structure and confirming I have publish dates for all entries, though some appear to have been updated since original posting.

Now I'm trying to reconcile the CLdN article's timeline — it was published in October 2025 but references a December 2025 project kickoff, which seems impossible for an already-published piece. I'm working through whether this is a dating error on my part or whether the article was revised after an earlier partnership announcement, since the surrounding context suggests the actual kickoff and go-live likely happened earlier than the text implies.

Good, so the EN post now covers the go-live after being updated. Now I need to compile the deliverable: a 2000-3000 word Polish report with sections a-d plus a full inventory of all 59 unique articles (title, date, URL, one-sentence description), noting that FR/NL/US versions are mostly translations. I have enough information for all 59 entries from metadata and my full reads, so I'll write clean one-liners myself rather than rely on the sometimes garbled meta descriptions, starting with a short methodology section covering the sitemap count and how many articles I read in full.

Now I'm outlining what to cover under "czego klienci oczekują" — pain points like admin overload and rekeying data across spreadsheets, emails, and phone calls, the complexity of container orders needing 20+ data points, having to juggle multiple tabs just to check container release status, and cash flow issues tied to slow invoicing.

I'm gathering additional evidence: unpaid receivables and PODs chasing, quotes on invoicing speed as a KPI, empty mileage statistics for UK and EU, empty container moves as a costly data problem, and rising customer demand for visibility and self-service tracking. I'm also pulling together client testimonials from JODA, Kees in 't Veen, Alders Bulk, Hjalmar Van Tiel, Handico, Craig Perrin at Hemisphere, and Nolize, each highlighting different value points like forecasting, reliability, compliance, traceability, and secure data exchange.

Now I'm cataloguing the objections companies raise when facing change—resistance to leaving spreadsheets, retraining costs, and specific worries about Peppol e-invoicing like accounting system changes, added admin, subcontractor impact, and customer readiness. I'm also noting rising security scrutiny from NIS2 questionnaires, CO2 reporting demands in tenders, planner skepticism toward route optimization software, SME cost concerns for 2025, and bulk-specific compliance issues like ADR, Qualimat, cleaning certificates, and demurrage disputes. I'm starting to map these pain points against Qargo's specific solutions and USPs, beginning with the Qi intelligence feature.

Qi handles order entry from emails, PDFs, and EDI, extracts document details like seal numbers and container IDs, matches proof of delivery, automates self-billing invoicing, runs quality control checks, detects signatures, generates company summaries, and processes email intelligence through Outlook—with claimed results like 75% less admin time, 90% accuracy, and hours saved per planner and per week on QC and email tasks. I'm also noting the route optimization stack combining HERE Maps, Optimize, and PTV for multi-depot planning, with UK-specific mileage savings figures.

Now I'm cataloging the integration ecosystem: telematics providers like Samsara and Webfleet, pallet networks such as Palletline and Pall-Ex with their multiple data flows, ferry operators, port systems, accounting platforms like Exact and Sage, plus WMS and WhatsApp Business connections. I'm also listing the portal offerings—customer portals with approval workflows and KPI dashboards, subcontractor portals, and tracking links—before moving into compliance and security considerations.

Security and compliance stand out as genuine differentiators: ISO 27001 certification from March 2025, Google Cloud infrastructure with Cloud Armor, Aikido security tooling, a public trust centre, enforced MFA, and NIS2 alignment given their status as an important entity. I'm also noting their Peppol e-invoicing partnership through B2BRouter launching in Belgium, CO2 emissions tracking aligned with GLEC and ISO 14083 standards down to order and trip level, and bulk-specific features like ADR enforcement and compartment management. The company positions itself as cloud-native with weekly updates and a "partner not vendor" philosophy, backed by the Qargo Network for work-sharing between clients and seed funding of $6M from Stride.VC in 2022 followed by a Series A round.

Their funding history continues with €12M/£11M Series A in June 2024 from Balderton, then a $33M Series B in December 2025 backed by Sofina, bringing total funding to $54M — alongside growth from 100 to 400+ clients, invoicing volume jumping from £420M to £1.9B, and expansion from 2 to 6 markets, earning them the label of fastest-growing TMS in Europe. The company was founded in 2020 by Coppens, de Turck, and de Wilde, all formerly of OTA Insight. On the regulatory side, I'm tracking Belgium's mandatory B2B Peppol rollout starting January 2026 using UBL format and Access Points aimed at reducing errors and improving tax transparency, plus France's CTC mandate requiring reception capability for all businesses starting September 2026.

Details fall into place around France's rollout: large companies and ETIs must handle e-invoicing issuance by September 2026, with SMEs following by September 2027, involving PA (formerly PDP), PPF, and DGFiP, using Factur-X/UBL/CII formats, with penalties around €15 per invoice under a reverse charge mechanism — though paper CMR remains valid separately from eCMR discussions, and Qargo integrates with B2BRouter. Poland's KSeF mandate kicks in April 2026, the Netherlands continues expanding Peppol adoption, and on the eCMR/eFTI front, France, Netherlands, and Spain have already adopted eCMR while the EU is targeting 2027 for mandatory cross-border electronic freight documentation.

I'm now thinking through NIS2: applicable EU-wide since October 18, 2024, covering companies with 50+ employees and €10M+ revenue. Belgium's law took effect April 26, 2024 with CyFun and an essential-entity deadline of April 18, 2026; the Netherlands' Cyberbeveiligingswet becomes enforceable August 15, 2026 with no grace period; France has delayed implementation due to an encryption dispute referred to the EU Court in July 2026, expected to resolve around September 2026 — with distinctions between essential and important entities, reporting windows of 24 hours/72 hours/1 month, management liability, and supply chain security questionnaires. On CSRD, it's been in force since 2023 with original thresholds of 250 employees/€50M, but Omnibus I adopted in February 2026 raises thresholds to 1,000+ employees and €450M+, pushing first reports to 2028 and exempting roughly 80% of companies — though Scope 3 obligations still weigh on shippers.

Vrachtwagenheffing in the Netherlands mandates carrier data starting July 1, 2026, using GLEC/ISO 14083 standards, with CO2 factored into tenders; the toll applies to vehicles over 3.5t, with Euro 6 trucks over 32t paying around €0.195/km versus €0.038/km for zero-emission vehicles at 2025 levels, while the Eurovignette gets phased out. On customs and Brexit, I'm noting the GB-NI trap requiring GB codes, MRN/PBN/GMR documentation, NI postcode auto-detection, and customs pre-notification for the Irish Sea corridor, plus ADR/Qualimat bulk compliance requirements. I'm flagging that the AI Act and the Mobility Package/cabotage rules are notably absent from the blog's discussion, and EU drivers' hours are only mentioned in an operational context.

Looking at product direction for 2025-2026, there's exploration of agentic AI for booking terminal time slots and a self-service rule configuration agent launching June 2026, described as the first time AI takes the driving seat, alongside Series B mentions of agentic AI interacting with external systems. Planning boards aren't AI-powered yet but are being watched, a dedicated CO2/emissions dashboard is in progress, and there's a 2026 goal to automate-and-review mailbox workflows alongside an eCMR rollout with TransFollow across Belgium, Netherlands, and France. The pallet network roadmap covers visibility sync, cost charge automation, expanded coverage, and streamlined customs, while expansion continues into the US and across six European markets, with multimodal capabilities like CLdN's sea/rail/road services and an intermodal service line added for 2026.

I'm noting the addition of Intermodal and Liquid Bulk in February 2026, the Qargo Unlocked event series, and their view of market consolidation around connected workflows, compliance as baseline, and sustainability data as a commercial differentiator. Moving to the corporate client segment, the declared segments are carriers, freight forwarders, and 3PLs — not shippers as the target user. Shippers instead appear as customers of customers (via portals, tracking links, and deep integrations with shipper systems per Series A) or as a source of requirements like Scope 3/CO2 tender demands, security questionnaires, and EDI standards.

There's no dedicated control tower product for shippers — visibility flows through the carrier's portal instead, and an empty-miles article states directly that shippers don't share upcoming demand, framing this as a problem rather than a product opportunity. Enterprise examples include CLdN (multimodal, 9000 containers/trailers, replacing a 2007 TMS), Kinaxia (~1000 vehicles, Samsara plus EDI and centralized reporting), Uniserve, Altrea, and Moran (300+ vehicles), with Series B messaging framing growth as moving "from family-run companies to enterprise businesses."

So Qargo isn't directly targeting the shipper/control tower segment — it's built for enterprise carriers and 3PLs, with shipper visibility only achieved indirectly. I still need to write out the full inventory of 59 entries with title, date, URL, and one sentence each, without shortening it, and I'm thinking a markdown table using shortened slug-based URLs would work better than full pipe-separated URLs given how wide those would make the table.

I'll use datePublished for each entry since that's more precise than the batch lastmod dates, and I've already pulled those from the accurate values for the affected items. Now I'm ordering the inventory chronologically from oldest to newest, pulling from the cleaned-up data file to produce the final list.

Continuing through the rest of the article list into early 2026: legacy comparison, data protection, world cleanup day, TMS onboarding, CLdN and Groupe Sudre case studies, Peppol invoicing guides, the Series B $33M raise, kilometre charge updates, transport invoicing, planning board, Trezzini, and 2026 logistics trends — rounding out the full timeline of published dates.

Continuing the list: 46. 2026-05-21 hidden cost of manual ops, 47. 2026-05-29 bulk transport challenges, 48. 2026-06-11 route optimisation and sustainability, 49. 2026-06-18 AI workflow day in the life, with entry 50 still to confirm.

Now I'm double-checking the exact dates against the inventory listing to make sure I haven't misordered any of the entries, particularly around the transports-trezzini row.

I'm double-checking the kinaxia date against both the article header and the inventory ordering, since they seem to conflict slightly — I'll trust the article's own stated date of January 27, 2026, rather than trying to infer position from the printed list.

There's some ambiguity between the inventory date and the page header date for the Kinaxia article — one says the 27th, another the 28th. I'll just go with 2026-01-28 since that's what the datePublished field extraction suggested, keeping things simple rather than chasing down the discrepancy further.

I'm not entirely sure of the exact date for the Trezzini article, but the header said January 15, 2026, so I'll settle on that. These small date discrepancies aren't significant enough to affect the report.

Now I'm ready to write the full report in Polish, covering sections a-d plus the corporate client section and the inventory table at the end, aiming for roughly 2000-3000 words. Since the user wants the report returned directly in the chat, I'll deliver the entire text as my final response rather than creating a separate file.

For the inventory table, I'll structure it with title as a markdown link (embedding the full URL), followed by date and a one-sentence description, covering all 59 entries without shortening the list.

I'll keep it simple with full URLs in their own column since the user explicitly asked for that format, even if the table gets a bit wide. Now I'm mentally sizing the draft — aiming for roughly 2300-2800 Polish words across the main sections plus the corporate section — and planning to open the final message with a brief summary of the methodology before diving into content.

I want to double-check the KSeF rollout dates (large taxpayers February 2026, rest in April 2026) match what the article states, confirm the seed article's actual 2022 publication date, and verify the GLEC, CSRD, NIS2, and Peppol dates all line up. I also need to flag clearly that Mobility Package, cabotage rules, and the AI Act aren't covered in the blog source, since the user specifically asked about those topics.

I'm also noting what the blog does cover regarding Brexit and customs — GB-NI movements, MRN/PBN/GMR documentation, customs pre-notification, and streamlined processes mentioned in the pallet network roadmap and container integration articles. With all this verified, I'm ready to write the final report.

---

# Raport: analiza sekcji News & Blogs firmy Qargo (qargo.com)

**Metodologia.** Listing `qargo.com/resources/news-and-blogs/` renderuje karty artykułów JavaScriptem, więc pełny inwentarz zbudowałem z sitemapy Yoast (`post-sitemap.xml`, 199 URL-i, z czego reszta to tłumaczenia FR/NL/US). Zidentyfikowałem **59 unikalnych artykułów** (57 na głównym serwisie EN, 1 tylko na `/us/` — „How Qargo makes integrations simple", 1 tylko po niderlandzku — „Qargo Intelligence: minder admin…"), opublikowanych od września 2022 do 2 września 2026, co odpowiada ~10 podstronom listingu. Pobrałem wszystkie 59 stron i przeczytałem w całości ~25 najbardziej merytorycznych. Kontekst firmy: Qargo (zał. 2020, Gandawa/Londyn; założyciele Adriaan Coppens, Joeri de Turck, Sander de Wilde — wcześniej OTA Insight) to chmurowy TMS dla przewoźników drogowych, spedycji i 3PL; seed $6M (2022, Stride.VC), Series A €12M (VI 2024, Balderton), Series B $33M (XII 2025, Sofina + Balderton), łącznie $54M; w 18 miesięcy od Series A: ze ~100 do 400+ klientów, fakturowanie przez platformę z £420M do £1,9 mld rocznie, 6 rynków europejskich + start w USA.

---

## a) Czego klienci oczekują od TMS — bolączki i powtarzające się motywy

**1. Likwidacja ręcznego przepisywania danych (motyw nr 1, obecny w ~80% wpisów).** Obraz operacji rysowany przez Qargo: planista obsługuje 40 zleceń dziennie w arkuszu, trzech wątkach mailowych i przez telefon; jedno zlecenie kontenerowe to 20+ pól przepisywanych z maili, PDF-ów i portali; operator kontenerowy ma otwartych „5+ zakładek", żeby sprawdzić, czy kontener jest zwolniony do odbioru. Cytat klienta (Luke Ryan, JODA): najbardziej złożony typ zlecenia zajmował w starym systemie 15 minut, w Qargo z AI — 2 minuty. Oczekiwanie: zlecenia z maili/PDF/EDI mają wpadać do systemu same, a człowiek tylko zatwierdza.

**2. Cash flow i szybkie fakturowanie.** „Late invoicing" to wg Qargo najczęściej zgłaszany ból branży. Przykład liczbowy z bloga: spedytor fakturujący 200 zleceń tygodniowo po £800 z 7-dniowym opóźnieniem stale „nosi" £160 000 niezafakturowanych należności (plus koszty finansowania). Wąskim gardłem jest czekanie na POD/CMR od kierowcy i ręczna weryfikacja stawek. Klienci chcą, by podpisany dokument dostawy natychmiast uruchamiał fakturę; Qargo proponuje KPI „time-to-invoice".

**3. Puste kilometry jako problem danych, nie kierowców.** Dane przytaczane: w UK 31% km ciężarówek jeździ pusto (DfT, 2025; 5 897 mln z 18 975 mln km), średnia UE 25,9%; puste przebiegi kontenerowe kosztują branżę ponad $20 mld rocznie. Diagnoza Qargo: przyczyną jest brak przepływu danych (systemy shippera, przewoźnika i brokera nie rozmawiają; załadowcy nie dzielą się prognozą popytu; późne potwierdzenia), a nie złe planowanie.

**4. Widoczność i self-service dla klienta końcowego.** Powtarzający się motyw: zespoły operacyjne toną w telefonach „gdzie jest moja dostawa?". Oczekiwanie rynku (wprost nazwane): portal klienta to już nie przewaga, lecz „oczekiwanie branżowe"; do tego publiczne linki śledzenia dla odbiorców jednorazowych. Cytat: „Portal klienta Qargo zwiększył satysfakcję naszych klientów dzięki przejrzystości i kontroli nad każdą przesyłką" (Pieter Engels, PE Express).

**5. Compliance i bezpieczeństwo jako wymaganie zakupowe.** Klienci przewoźników (duzi załadowcy) wysyłają ankiety bezpieczeństwa (NIS2) i żądają zweryfikowanych danych CO₂ per przesyłka w przetargach — „jeśli nie umiesz ich dostarczyć, znajdą kogoś, kto umie". W bulk: ADR, certyfikaty mycia cystern, Qualimat (pasze we Francji), spory o demurrage przegrywane z braku stempli czasowych.

**6. Obawy przy zmianie systemu (głosy operatorów cytowane wprost):** „Zawsze tak robiliśmy", „Arkusze dają nam elastyczność", „Przeszkolenie będzie kosztować więcej, niż zaoszczędzimy", „Żaden system nie zna naszego terenu tak jak nasi planiści"; przy Peppol: „Czy będę musiał zmienić system księgowy?", „Czy to więcej administracji?", „Co jeśli mój klient nie będzie gotowy?", „Czy to dotyczy też podwykonawców?". Tło ekonomiczne: 81% MŚP transportowych wskazuje rosnące koszty jako główną obawę; w UK w rok upadło ~500 firm przewozowych. Wymagania z case'ów: Nolize — „widoczność end-to-end, wyższa efektywność, bezpieczniejsza wymiana z partnerami"; Hemisphere Freight — „traceability, automatyzacja i skalowalność"; Alders Bulk — „innowacyjny partner, który myśli z nami"; Kees in 't Veen — stary TMS nie pokazywał prognozowanych kosztów przyszłych zleceń.

## b) Rozwiązania Qargo i deklarowane wyróżniki (USP)

**Qi — Qargo Intelligence (rdzeń narracji od XII 2024).** Zestaw AI wbudowany w platformę: ekstrakcja zleceń z maili/PDF/EDI (uczy się formatów klientów), Document Intelligence (numery plomb, kontenerów, palety → auto-uzupełnianie pól), auto-matching POD/CMR do zlecenia, self-billing podwykonawców (krzyżowa weryfikacja POD, podpisów, stawek, dopłat), kontrola jakości dokumentów w systemie RAG (zielony/pomarańczowy/niebieski), detekcja podpisów (kto, jaka rola, współrzędne), AI-podsumowania firm (obrót, skala — przy onboardingu kontrahenta), Email Intelligence (wtyczka Outlook, wiązanie maili ze zleceniami, tworzenie zleceń z inboxa). Deklarowane liczby: do **75% mniej czasu na powtarzalną administrację**, 90% trafności tworzenia zleceń, 65% szybsze przetwarzanie faktur, 70% szybsza obsługa dokumentów, 2 h dziennie oszczędności na planistę, „redukcja nadgodzin o 8 h dziennie" (Anglia Freight). Pozycjonowanie: „AI, które zna transport" — nie zastępuje ludzi, decyzje zostają u planisty; przejrzystość logiki każdej sugestii.

**Optymalizacja tras i puste kilometry.** Sekwencjonowanie multi-drop wg przebiegu/czasu/kosztu/okien/ograniczeń pojazdu, multi-depot, routing HERE Maps z opcją silnika Optimize i integracją PTV. Wyniki: Anglia Freight — 6–8% redukcji przebiegu floty, 200 000+ mil rocznie, cross-dock scanning +20 min produktywności na pojazd dziennie; deklaracja „do 30% mniej pustych przebiegów". Dashboardy rozbijają kilometry na ładowne/puste/dojazdowe per kierowca/pojazd/podwykonawca.

**Ekosystem integracji jako fosa.** Telematyka (Samsara, Verizon, Webfleet, Platform Science), sieci paletowe (Palletline, Palletforce, Pall-Ex, UPN, Hazchem — każda integracja to 9 przepływów danych), promy (Irish Ferries, Stena Line, P&O), porty/terminale (Portbase, Destin8, PSA), księgowość (Exact, AFAS, Adsolut, Adfinity, Sage, Xero), WMS (Clarus), WhatsApp Business (czat z kierowcami w TMS). „Setki partnerów integracyjnych".

**Portale i współpraca.** Portal klienta (składanie/zmiana zleceń z workflow akceptacji, statusy, ePOD, zdjęcia, KPI z demurrage, news feed, druk lokalny per typ dokumentu), portal podwykonawcy (trip-y, ETA, upload POD/CMR, ścieżki zadań), publiczne czasowe linki śledzenia bez logowania oraz **Qargo Network** — dzielenie zleceń między klientami Qargo w czasie rzeczywistym („jakby to była własna flota").

**Bezpieczeństwo jako wyróżnik sprzedażowy.** ISO 27001 (od III 2025), wyłącznie Google Cloud + Cloud Armor, skan kodu Aikido, pentesty, publiczne Trust Centre, wymuszane MFA/SSO/RBAC/audyt (funkcje budowane „bo klienci prosili pod NIS2"), zobowiązanie 72 h notyfikacji o naruszeniu, rejestracja Qargo jako „important entity" pod NIS2.

**Model biznesowy i wdrożenie.** Cloud-native SaaS, cotygodniowe release'y, nowe funkcje standardowe w cenie subskrypcji (kontra opłaty legacy), 6-etapowy onboarding prowadzony „przez ludzi z transportu", kalkulator ROI i rama „pięciu dźwigni ROI" (automatyzacja admin, wycieki opłat, weryfikacja faktur podwykonawców, wyjątki/OTIF, koszty raportowania + marża per trip). Narracja „partner, nie dostawca" (cytat D'hooghe). Specjalizacje branżowe: kontenery (statusy zwolnień, reuse, sloty), short sea (ekran intermodalny, bulk-przebookowanie po sztormie, rekoncyliacja faktur promowych), bulk/cysterny (egzekwowanie zgodności ADR na tablicy planowania, komory, nieprzeskakiwalne zadania kierowcy, godziny pracy kierowców w kalkulacji tras), koszty zasobów liczone dniem/tygodniem zamiast per trip.

## c) Zmiany prawne i formalne rynku wg Qargo (z datami)

**E-fakturowanie / Peppol — najmocniej eksploatowany temat (5 artykułów):**
- **Belgia:** od **stycznia 2026** wszystkie faktury B2B obowiązkowo elektronicznie przez sieć Peppol (format UBL, Access Point); cel rządu: mniej błędów i fraudów, szybsze płatności, przejrzystość podatkowa; 2024–2025 było okresem podłączania i testów. Qargo: Peppol „out of the box" przez certyfikowanego partnera B22Router, produkcyjnie od stycznia 2026.
- **Francja:** reforma CTC — od **1 września 2026** każda firma zarejestrowana do VAT musi umieć **odbierać** e-faktury, a duże i średnie (ETI) także **wystawiać** i raportować (e-reporting); od **1 września 2027** obowiązek wystawiania obejmie MŚP i jednoosobowe. Architektura: Plateforme Agréée (dawniej PDP) + centralny Portail Public de Facturation (katalog + koncentrator danych dla DGFiP); formaty Factur-X/UBL/CII; kary ~€15 za niezgodną fakturę (z rocznym limitem), zapowiedziana „miękka" egzekucja. Specyfika transportu: łańcuchy podwykonawstwa (3–5 faktur na jedną trasę — shipper→commissionnaire→affréteur→przewoźnik), odwrotne obciążenie przy transporcie wewnątrzwspólnotowym; **papierowy CMR pozostaje ważny** — reforma nie wymusza eCMR.
- **Polska:** wymieniona wprost — obowiązkowe e-fakturowanie „od kwietnia 2026" (KSeF); **Holandia:** rozszerzanie adopcji Peppol. Teza strategiczna Qargo: Peppol to „pierwsze domino" — te same standardy danych obejmą zlecenia transportowe, przepływy podwykonawców, faktury zakupowe, raportowanie CO₂ i wymianę dokumentów.

**eCMR / eFTI:** eCMR „staje się obowiązkowy w Europie", już szeroko przyjęty we Francji, Holandii i Hiszpanii; kierunek UE: **obowiązkowa akceptacja elektronicznej dokumentacji przewozowej w ruchu transgranicznym celowana na 2027** (czyli wdrożenie eFTI, choć Qargo nie używa tej nazwy). Odpowiedź produktowa: partnerstwo z TransFollow (II 2026) — eCMR tworzony, wystawiany i podpisywany w Qargo i aplikacji kierowcy, ze statusami draft/issued/in transit/delivered.

**NIS2 / cyberbezpieczeństwo:** dyrektywa stosowana od **18 października 2024**; obejmuje transport drogowy jako sektor imienny, próg 50+ pracowników i €10M+ obrotu; podział essential (zarządcy dróg, więksi operatorzy) / important (przewoźnicy, spedycje, logistyka). Transpozycje: **Belgia** — ustawa z 26 IV 2024, framework CyFun, termin samooceny podmiotów essential **18 IV 2026** (minął); **Holandia** — Cyberbeveiligingswet w mocy od **15 VIII 2026, bez okresu przejściowego**; **Francja** — opóźniona (spór o szyfrowanie, skierowanie do TSUE VII 2026, spodziewana ~IX 2026), ale klauzule bezpieczeństwa już pojawiają się w kontraktach. Wymogi: MFA, logowanie, plan reakcji; raportowanie 24 h / 72 h / 1 miesiąc; osobista odpowiedzialność zarządu; due diligence łańcucha dostaw — mniejsi przewoźnicy i tak dostaną ankiety od dużych klientów.

**CO₂ / CSRD / GLEC:** CSRD w mocy od początku 2023 (pierwotne progi 250 pracowników / €50M); **dyrektywa Omnibus I przyjęta w lutym 2026** zawęziła zakres do firm **1000+ pracowników i €450M+ obrotu, pierwsze raporty w 2028** (wypada ~80% pierwotnie objętych). Kluczowa teza: to nie zwalnia przewoźników, bo załadowcy nadal raportują Scope 3 i żądają zweryfikowanych emisji per przesyłka, a CO₂ wchodzi do wymogów przetargowych. Metodyka: **GLEC / ISO 14083**; Qargo liczy emisje na poziomie zlecenia i trasy (projekt BILOG z VIL, TLCC, Altrea, ZF/Transics, Uniwersytetem w Hasselt jako POC raportowania CSRD).

**Opłaty drogowe:** holenderska **vrachtwagenheffing od 1 lipca 2026** — opłata kilometrowa dla pojazdów >3,5 t DMC na autostradach i części dróg N, taryfa wg masy i klasy emisji (Euro 6 >32 t ~€0,195/km vs zeroemisyjny €0,038/km wg stawek 2025), wygaszenie eurowiniety; Qargo wliczyło stawki 2026 do wycen i planowania z wyprzedzeniem (routing PTV, rozdział km płatnych/nieopłatnych, nowe profile 12–18 t i 40 t).

**Cła / Brexit:** obsługa korytarza Morza Irlandzkiego i tras UE–UK: MRN, PBN, GMR, typy deklaracji; pułapka trasy GB–Irlandia Płn. (kod „GB" maskuje wymogi NI) — automatyczna detekcja po kodzie pocztowym NI; „uproszczenie procesów celnych" na roadmapie sieci paletowych. **Czego w blogu nie ma:** Pakiet Mobilności i kabotaż nie są omawiane (normy czasu jazdy pojawiają się tylko operacyjnie w planowaniu bulk), AI Act nie jest wspomniany ani razu.

## d) Kierunki produktu 2025–2026 i wizja rynku TMS

- **Od „AI-assisted" do „automate-and-review", potem AI agentowe.** Deklarowany cel na 2026: dane zleceń i faktur pobierane wprost ze skrzynki, człowiek tylko przegląda. Series B mówi wprost o „agentic AI wchodzącym w interakcję z systemami zewnętrznymi". Dwa konkretne kierunki: **agent AI do samodzielnej konfiguracji reguł** przez klienta (ogłoszony VI 2026 — „po raz pierwszy to ty konfigurujesz Qargo, bez ticketu do inżynierów; to dopiero początek") oraz **agenci rezerwujący sloty czasowe w terminalach kontenerowych** (eksplorowane, zapowiedziane w trendach 2026 i artykule kontenerowym).
- **Planowanie:** „nasze tablice planistyczne nie są jeszcze AI-powered — watch this space" — jawna zapowiedź AI w planowaniu; dziś reguły automatyzują grupy planistyczne, sekwencje, ETA.
- **Zrównoważony rozwój:** dedykowany, samoobsługowy **dashboard CO₂/emisji** w budowie (dziś liczenie GLEC/ISO 14083 per zlecenie/trasa, w tym drobnica).
- **Dokumenty:** rollout **eCMR z TransFollow** w BE/NL/FR; wizja „dokument = żywe dane" (podpisany eCMR natychmiast uruchamia fakturę).
- **Sieci paletowe (roadmapa z warsztatu Qargo Unlocked, III 2026):** pełna synchronizacja widoczności z sieciami bez ręcznej ingerencji, automatyzacja opłat kosztowych (koniec ręcznych rate cards), nowe integracje i uproszczenie ceł.
- **Ekspansja:** 6 rynków europejskich po Series B, osobny serwis `/us/` i deklaracja „łączymy teraz workflow transportowe w USA" (VII 2026); wejście w **multimodal/intermodal** (go-live CLdN: morze+kolej+droga; nowe linie usług Intermodal i Liquid Bulk & Tank w nawigacji od II 2026); seria eventów klienckich **Qargo Unlocked**.
- **Wizja rynku wg Qargo:** rynek TMS (prognoza $19,1 mld do 2032) konsoliduje się wokół czterech osi z trendów 2026 — zrównoważony rozwój (dane emisyjne jako przewaga handlowa), AI w codziennej operacji, compliance jako warunek bazowy (nie wyróżnik) i „jeden połączony workflow zamiast dziesięciu narzędzi". Wygrywają operatorzy, którzy „potrafią udowodnić wykonanie — czas, koszt i emisje".

## 4) Klient korporacyjny: shipperzy, control tower, visibility

**Qargo nie adresuje segmentu załadowcy (shippera) jako użytkownika systemu i nie buduje produktu typu control tower.** Deklarowane segmenty to konsekwentnie **przewoźnicy, spedycje i 3PL** („Designed for carriers, freight forwarders, and 3PLs"); nawigacja serwisu nie zawiera rozwiązania „for shippers". Załadowca korporacyjny występuje w trzech rolach pośrednich:

1. **Odbiorca widoczności przez narzędzia przewoźnika** — portal klienta (statusy, ePOD, KPI, demurrage), publiczne tracking linki i „głębokie integracje z systemami shipperów" (już w komunikacie Series A). Visibility jest więc funkcją sprzedawaną przewoźnikowi, by ten obsłużył swojego korporacyjnego klienta — nie osobną platformą dla shippera.
2. **Źródło wymagań regulacyjno-zakupowych** — to od shipperów przychodzą żądania danych CO₂ (Scope 3, przetargi), ankiety bezpieczeństwa NIS2, standaryzacja przyjęcia zleceń i EDI (Kinaxia).
3. **Brakujące ogniwo danych** — w analizie pustych kilometrów Qargo wprost wskazuje, że „shipperzy nie dzielą się nadchodzącym popytem, więc przewoźnicy nie mogą się pre-pozycjonować"; to diagnoza problemu, nie zapowiedź produktu.

Segment **enterprise** Qargo rozumie jako dużych operatorów logistycznych, nie korporacyjnych załadowców: **CLdN Cargo** (czołowy europejski operator multimodalny, 9000 kontenerów/naczep — wymiana TMS z 2007 r., pełny order-to-pay morze/kolej/droga), **Kinaxia** (~1000 pojazdów, UK; Samsara + Qargo, scentralizowany reporting wielolokalizacyjny, OTIF), **Uniserve**, **Moran Logistics** (300+ pojazdów, temperatura kontrolowana dla sieci detalicznych), **Altrea**. Series B deklaruje obsługę „od firm rodzinnych po enterprise". Wniosek: jeśli szukać luki konkurencyjnej — Qargo świadomie zostaje po stronie wykonawczej łańcucha (carrier-first), a potrzeby korporacyjne zaspokaja portalami, integracjami i danymi emisyjnymi, którymi jego klienci-przewoźnicy raportują się przed swoimi korporacyjnymi zleceniodawcami.

---

## Inwentarz artykułów (59 pozycji, chronologicznie; wersje FR/NL/US to tłumaczenia poniższych)

| Data | Tytuł | URL | O czym |
|---|---|---|---|
| 2022-09-12 | Qargo raises $6m to drive transport firms into the future | https://www.qargo.com/post/qargo-raises-6m-to-drive-transport-firms-into-the-future/ | Seed $6M od Stride.VC (Fred Destin) na ekspansję międzynarodową nowej generacji TMS. |
| 2024-06-06 | Qargo raises €12M/£11M from Balderton Capital | https://www.qargo.com/post/qargo-raises-12m-series-a-balderton-capital-ai-transport-platform/ | Series A na platformę all-in-one; 140+ klientów, case Anglia Freight (200 tys. mil), teza o wymianie legacy TMS. |
| 2024-09-18 | Introducing Qargo Email Intelligence | https://www.qargo.com/post/introducing-qargo-email-intelligence/ | Premiera wtyczki Outlook wiążącej maile ze zleceniami; zapowiedź generatywnego AI do tworzenia zleceń z inboxa. |
| 2024-12-12 | Celebrating National Truckers' Day in Belgium and the Netherlands | https://www.qargo.com/post/celebrating-belgiums-national-day-of-the-trucker/ | Wizerunkowy materiał o dniu kierowcy ciężarówki z wywiadem z belgijskim kierowcą Lievenem. |
| 2024-12-19 | Introducing Qargo Intelligence: AI-powered features | https://www.qargo.com/post/introducing-qargo-intelligence-ai-powered-features/ | Premiera pakietu Qi: kontrola jakości dokumentów (RAG), Document Intelligence i Email Intelligence; obietnica −75% czasu na admin. |
| 2025-02-05 | Sustainable Logistics Reporting: Paving the Way Forward | https://www.qargo.com/post/paving-the-way-for-sustainable-logistics-reporting/ | Udział w projekcie BILOG (VIL, ZF, Hasselt) — POC raportowania CO₂ pod CSRD wg GLEC; start liczenia emisji per zlecenie/trasa. |
| 2025-03-03 | Qargo is now ISO 27001 certified | https://www.qargo.com/post/qargo-now-iso-27001-certified/ | Uzyskanie certyfikatu ISO 27001 jako dowód bezpieczeństwa danych dla klientów i partnerów. |
| 2025-04-14 | How the Qargo & Clarus integration transforms transport & warehousing | https://www.qargo.com/post/clarus-integration-transforms-transport-warehousing/ | Dwukierunkowa integracja TMS↔WMS Clarus likwidująca silosy między transportem a magazynem. |
| 2025-05-15 | A fresh approach to logistics: Moran Logistics | https://www.qargo.com/post/a-fresh-approach-to-logistics-moran-logistics/ | Case: czołowy brytyjski dystrybutor żywności (300+ pojazdów, chłodnie) wybiera Qargo i rusza z wdrożeniem fazowym. |
| 2025-06-28 | Transport-Savvy AI: Smart enough for the real world of logistics | https://www.qargo.com/post/transport-savvy-ai-for-real-world-logistics/ | Manifest „AI znającego transport": ekstrakcja zleceń, walidacja reguł, POD-matching, dashboardy marż — bez zastępowania planistów. |
| 2025-07-14 | How do we use AI in our intelligent TMS? | https://www.qargo.com/post/ai-powered-tms-automation/ | Przegląd sześciu zastosowań Qi z cytatami klientów (JODA: 15→2 min na zlecenie); RAG, detekcja podpisów, podsumowania firm. |
| 2025-07-28 | WhatsApp now integrated in Qargo | https://www.qargo.com/post/whatsapp-integration-for-driver-messaging-2/ | Integracja WhatsApp Business — czat z kierowcami bez wychodzenia z TMS. |
| 2025-08-05 | Smarter route optimisation | https://www.qargo.com/post/blog-smarter-route-optimisation/ | Optymalizacja tras jako „skalowanie wiedzy planistów"; Anglia Freight: −6–8% przebiegu, +20 min/pojazd/dzień. |
| 2025-08-26 | Qargo vs Legacy TMS systems | https://www.qargo.com/post/qargo-vs-legacy-systems/ | 11 przewag nad systemami on-premise z liczbami (90% trafności zleceń, −65% czasu fakturowania) i cytatami klientów. |
| 2025-09-03 | How Qargo protects your transport data | https://www.qargo.com/post/how-qargo-protects-transport-data/ | Architektura bezpieczeństwa cloud-native: szyfrowanie, Google Cloud, kontrola dostępu. |
| 2025-09-20 | A cleaner future for transport (World Cleanup Day) | https://www.qargo.com/post/world-cleanup-day-2025/ | „Sprzątanie" logistyki: puste przebiegi, nieefektywne trasy i papier jako odpady operacyjne. |
| 2025-10-17 | TMS onboarding doesn't have to be painful | https://www.qargo.com/post/tms-onboarding-process/ | Sześcioetapowy proces wdrożenia z dedykowanym opiekunem i warsztatami procesowymi. |
| 2025-10-21 | CLdN partners with Qargo (multimodal TMS) | https://www.qargo.com/post/cldn-partners-with-qargo-to-deliver-next-generation-multimodal-transport-management-solution/ | Enterprise go-live: CLdN Cargo zastępuje TMS z 2007 r. pełnym order-to-pay dla sieci morze–kolej–droga. |
| 2025-10-24 | Groupe Sudre sets its sights on modernisation | https://www.qargo.com/post/groupe-sudre-sets-its-sights-on-modernisation/ | Francuska rodzinna grupa transportowa (5 spółek) modernizuje operacje na Qargo. |
| 2025-12-03 | Peppol: What it is and why it matters | https://www.qargo.com/post/peppol-guide-transport-operators/ | Przewodnik po Peppol przed belgijskim mandatem B2B od 2026 z typowymi obawami operatorów. |
| 2025-12-11 | Qargo raises $33 million in Series B | https://www.qargo.com/post/series-b-funding/ | Series B (Sofina): 4× klienci, 5× przychód, £1,9 mld fakturowania, agentic AI i Qargo Network. |
| 2025-12-19 | Dutch truck kilometre charge: Qargo ready for 2026 | https://www.qargo.com/post/truck-road-kilometre-charge-netherlands/ | Vrachtwagenheffing od 1 VII 2026 (taryfy wg masy i emisji) już wliczona w wyceny i planowanie. |
| 2025-12-22 | How Peppol will change invoicing for Belgian transport companies | https://www.qargo.com/post/peppol-invoicing/ | Szczegóły belgijskiego mandatu Peppol i automatyczna zgodność przez integracje księgowe. |
| 2026-01-05 | Faster transport invoicing | https://www.qargo.com/post/transport-invoicing/ | Skrócenie drogi POD→faktura dla poprawy cash flow; różnice fakturowania klienta vs podwykonawcy. |
| 2026-01-14 | 5 ways to optimise your planning board | https://www.qargo.com/post/planning-board-optimisation/ | Praktyczne porady dla planistów: układ kolumn, priorytety, redukcja szumu na tablicy. |
| 2026-01-15 | A growth path for Transports Trezzini | https://www.qargo.com/post/transports-trezzini/ | Case: francuski przewoźnik bulk (4→49 ciężarówek w 6 lat, korytarz FR–IT) wybiera Qargo. |
| 2026-01-23 | Transport and logistics trends 2026 | https://www.qargo.com/post/logistics-trends/ | Cztery trendy 2026: zrównoważony rozwój, AI (w tym agenci do slotów), compliance/NIS2 i łączność systemów. |
| 2026-01-27 | Nolize becomes more efficient by choosing Qargo | https://www.qargo.com/post/nolize-chooses-qargo-as-their-tms/ | Case: francuska spedycja wybiera Qargo dla widoczności end-to-end i bezpiecznej wymiany z partnerami. |
| 2026-01-27 | Kinaxia partners with Qargo | https://www.qargo.com/post/kinaxia-partners-with-qargo/ | Grupa ~1000 pojazdów (UK) łączy Qargo z telematyką Samsara: EDI, OTIF, centralny reporting. |
| 2026-01-28 | Why Peppol Is Just the Beginning | https://www.qargo.com/post/future-of-peppol/ | Peppol jako pierwszy krok standaryzacji danych (zlecenia, CO₂, dokumenty); wymienia mandaty FR i PL (IV 2026). |
| 2026-02-10 | eCMR inside Qargo: partnership with TransFollow | https://www.qargo.com/post/qargo-partners-with-transfollow-ecmr/ | Wbudowany eCMR (tworzenie, wystawianie, podpis w aplikacji kierowcy); kontekst celu UE 2027 dla e-dokumentacji. |
| 2026-02-11 | The three biggest challenges facing container operators in 2026 | https://www.qargo.com/post/challenges-container-operators/ | Bolączki operatorów kontenerowych: nadmiar systemów, puste przejazdy, admin; integracje portowe i promowe. |
| 2026-02-17 | What is a cross dock? | https://www.qargo.com/post/what-is-a-cross-dock/ | Poradnik: czym jest cross-docking i jak usprawnić operacje przeładunkowe. |
| 2026-02-20 | Shipping container transport: reduce admin & gain control | https://www.qargo.com/post/shipping-container-transport-reduce-admin/ | Redukcja przepisywania danych, widoczność zwolnień kontenerów i szybszy POD w transporcie kontenerowym. |
| 2026-02-26 | Empty container moves: why they happen | https://www.qargo.com/post/container-empty-legs/ | Puste przebiegi kontenerowe kosztują branżę $20+ mld rocznie; planowanie reuse i widoczność jako remedium. |
| 2026-03-04 | Your guide to container integrations | https://www.qargo.com/post/container-integrations-guide/ | Przewodnik po integracjach Portbase, Destin8, PSA — statusy portowe i celne w jednym workflow. |
| 2026-03-11 | Smart TMS for container haulage | https://www.qargo.com/post/connected-tms-container-haulage-operators/ | Wpływ połączonego TMS na konkurencyjność: niezawodność, odzysk przychodów, szybsze fakturowanie. |
| 2026-03-18 | How Qargo's customer portal transforms transport operations | https://www.qargo.com/post/transport-customer-portal/ | Portal klienta: samoobsługa zleceń, workflow akceptacji, KPI/demurrage, news feed — od reaktywnej do proaktywnej obsługi. |
| 2026-04-10 | Fuel surcharge dashboard | https://www.qargo.com/post/fuel-surcharge-dashboard/ | Automatyzacja indeksowanych dopłat paliwowych z widokiem pokrycia FSC w czasie rzeczywistym. |
| 2026-04-14 | Qargo Intelligence: minder admin, minder uitstoot (tylko NL) | https://www.qargo.com/nl-NL/post/qargo-intelligence-nederland/ | Holenderska premiera narracji Qi: mniej administracji i emisji, gotowość na vrachtwagenheffing. |
| 2026-04-17 | Qargo Unlocked: insights from our Pallet Network Workshop | https://www.qargo.com/post/introducing-qargo-unlocked/ | Nowa seria warsztatów klienckich; roadmapa sieci paletowych (widoczność, automatyzacja opłat, cła). |
| 2026-04-20 | How Qargo's tracking links close the visibility gap | https://www.qargo.com/post/tracking-links/ | Publiczne, czasowe linki śledzenia bez logowania — mniej telefonów „gdzie moja dostawa". |
| 2026-04-22 | Earth Day in action | https://www.qargo.com/post/earth-day/ | Pomiar i redukcja śladu węglowego; transparentność emisji jako wymóg kontraktowy i przewaga handlowa. |
| 2026-05-01 | Built to Scale: How Qargo Grows With Your Business | https://www.qargo.com/post/how-qargo-tms-scales-with-your-transport-business/ | Rozwój sterowany przez klientów, cotygodniowe release'y i funkcje w cenie subskrypcji jako paliwo skalowania. |
| 2026-05-08 | The top challenges facing short sea operators | https://www.qargo.com/post/short-sea-operator-challenges/ | Intermodal/short sea: rezerwacje promowe z jednego ekranu, cła (MRN/PBN/GMR, pułapka GB–NI), rekoncyliacja faktur promowych. |
| 2026-05-21 | The hidden cost of manual transport operations | https://www.qargo.com/post/hidden-cost-manual-transport-operations/ | Kwantyfikacja ukrytych kosztów: £160 tys. w niezafakturowanych należnościach, podatek od pustych mil, mnożnik błędów. |
| 2026-05-29 | Bulk & liquid tank operations: biggest challenges | https://www.qargo.com/post/bulk-transport-challenges/ | Bulk/cysterny: rozproszone dane, demurrage, ADR/Qualimat, komory — egzekwowanie zgodności w planowaniu i aplikacji kierowcy. |
| 2026-06-11 | Route optimisation for sustainability & cost savings | https://www.qargo.com/post/route-optimisation-sustainability/ | CSRD po Omnibus I (progi 1000 os./€450M, raporty od 2028) i emisje GLEC/ISO 14083 jako przewaga przetargowa. |
| 2026-06-18 | Day in the life: An operations manager's AI-powered workflow | https://www.qargo.com/post/transport-ai-workflow/ | Dzień pracy z AI: zlecenia gotowe przed kawą, premiera agenta AI do samodzielnej konfiguracji reguł. |
| 2026-06-25 | Fixed costs, multiple trips — resource costing | https://www.qargo.com/post/transport-resource-costing/ | Koszty zasobów liczone dniem/tygodniem zamiast per trip dla realnej rentowności operacji wielokursowych. |
| 2026-06-29 | Why the future of logistics depends on collaboration | https://www.qargo.com/post/national-logistics-day/ | Współpraca zamiast silosów: portal podwykonawcy i wspólny obraz danych w łańcuchu. |
| 2026-07-08 | Reducing empty miles: a data problem, not a driver problem | https://www.qargo.com/post/empty-miles/ | Puste kilometry (UK 31%, UE 25,9%) jako skutek luk danych; widoczność → planowanie → współpraca sieciowa. |
| 2026-07-14 | Measuring the real ROI of a TMS | https://www.qargo.com/post/tms-roi/ | Rama pięciu dźwigni ROI i trzyetapowy plan pomiaru (baseline → delta → annualizacja) pod business case dla CFO. |
| 2026-07-23 | On-premises vs cloud-based TMS | https://www.qargo.com/post/on-premises-vs-cloud-based-tms/ | Porównanie hostingu, aktualizacji i skalowalności — argumentacja za chmurą. |
| 2026-07-31 | How Qargo makes integrations simple (tylko US) | https://www.qargo.com/us/post/tms-integrations/ | Ekosystem integracji (księgowość, telematyka, EDI) i deklaracja rozszerzania go na rynek USA. |
| 2026-08-06 | Wave goodbye to rigid systems: customisable TMS | https://www.qargo.com/post/tms-configuration/ | Konfigurowalność: pola własne, workflow, uprawnienia ról zamiast sztywnych szablonów legacy. |
| 2026-08-20 | France's e-invoicing reform: before September 2026 | https://www.qargo.com/post/einvoicing-reform-france/ | Francuska reforma CTC (1 IX 2026 / 1 IX 2027, PA/PPF, Factur-X/UBL/CII) i gotowość Qargo przez B2BRouter. |
| 2026-08-27 | From paperwork to proof: digital documentation | https://www.qargo.com/post/digitalise-transport-documents/ | Dokument jako żywe dane: podpisany eCMR uruchamia fakturę; workflow TransFollow w aplikacji kierowcy. |
| 2026-09-02 | NIS2 and road transport | https://www.qargo.com/post/nis2-road-transport/ | NIS2 dla transportu: progi, terminy BE/NL/FR, obowiązki raportowe 24/72 h i przygotowanie przez TMS. |

**Uwagi końcowe:** blog niemal w całości mówi głosem przewoźnika/spedytora (bolączki administracyjne, cash flow, compliance), a tematy regulacyjne zagęszczają się wyraźnie od grudnia 2025 (Peppol → myto NL → eCMR → CSRD/Omnibus → e-fakturowanie FR → NIS2) — Qargo systematycznie zamienia każdą regulację w argument sprzedażowy „u nas to działa w tle". Brakuje za to zupełnie Pakietu Mobilności, kabotażu i AI Act, a segment załadowców korporacyjnych jest obsługiwany wyłącznie pośrednio, przez narzędzia widoczności dawane przewoźnikom.

Now I'm planning the full Polish report structure, allocating roughly 550-700 words to each of the main sections plus a shorter corporate section, before moving on to the inventory portion.

---

Raport gotowy powyżej. Najważniejsze ustalenia w skrócie: inwentarz objął komplet 59 unikalnych artykułów (wersje FR/NL/US to tłumaczenia), oś narracji Qargo to redukcja pracy ręcznej i cash flow przewoźnika, blok regulacyjny (Peppol/e-fakturowanie, eCMR, NIS2, CSRD, myto NL) gwałtownie rośnie od końca 2025 r., kierunki produktowe na 2026 to AI agentowe i multimodal, a segment korporacyjnych załadowców (control tower) pozostaje poza strategią — Qargo obsługuje go wyłącznie pośrednio, przez portale i dane emisyjne swoich klientów-przewoźników.