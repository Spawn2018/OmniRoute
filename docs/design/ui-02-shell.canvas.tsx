import {
  Button,
  Callout,
  Grid,
  H1,
  H2,
  H3,
  Pill,
  Row,
  Spacer,
  Stack,
  Stat,
  Table,
  Text,
  TextInput,
  Toggle,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

type PaletteGroup = "nawigacja" | "akcje" | "rekordy";

const NAV = [
  { id: "/", label: "Pulpit", section: "Operacje" },
  { id: "/extractions", label: "Ekstrakcje", section: "Operacje" },
  { id: "/rate-lines", label: "Stawki", section: "Cennik" },
  { id: "/charges", label: "Opłaty", section: "Cennik" },
  { id: "/quotations", label: "Wyceny", section: "Cennik" },
  { id: "/tenancy/users", label: "Użytkownicy", section: "Organizacja" },
  { id: "/organization-settings", label: "Ustawienia", section: "Organizacja" },
];

const PALETTE: {
  group: PaletteGroup;
  label: string;
  hint: string;
  allowed: boolean;
}[] = [
  { group: "nawigacja", label: "Idź do stawek", hint: "G", allowed: true },
  { group: "nawigacja", label: "Idź do kolejki ekstrakcji", hint: "E", allowed: true },
  { group: "akcje", label: "Zapisz widok tabeli", hint: "S", allowed: true },
  { group: "akcje", label: "Akceptuj szkic HITL", hint: "A", allowed: true },
  { group: "akcje", label: "Eksport stawek CSV", hint: "X", allowed: false },
  { group: "rekordy", label: "CNSHA–PLGDY 40HC · rate_line", hint: "", allowed: true },
  { group: "rekordy", label: "Szkic MAERSK-SHA-0926", hint: "", allowed: true },
];

const NOTICES = [
  { title: "3 szkice HITL czekają", detail: "kolejka ekstrakcji · reviewer" },
  { title: "Stawka CNSHA–PLGDY wygasa 7 dni", detail: "source_ref MAERSK-SHA-0926" },
];

export default function UiShell() {
  const [route, setRoute] = useCanvasState("ui-02-route", "/rate-lines");
  const [tenant, setTenant] = useCanvasState("ui-02-tenant", "sped-bałtyk");
  const [dark, setDark] = useCanvasState("ui-02-dark", false);
  const [density, setDensity] = useCanvasState("ui-02-density", "compact");
  const [paletteOpen, setPaletteOpen] = useCanvasState("ui-02-palette", true);
  const [query, setQuery] = useCanvasState("ui-02-query", "");
  const [noticesOpen, setNoticesOpen] = useCanvasState("ui-02-notices", false);

  const crumbs =
    route === "/rate-lines"
      ? ["Cennik", "Stawki kupna"]
      : route === "/extractions"
        ? ["Operacje", "Ekstrakcje"]
        : ["Organizacja", NAV.find((item) => item.id === route)?.label ?? "Pulpit"];

  return (
    <Stack gap={24}>
      <Stack gap={8}>
        <H1>Shell — tenant, paleta, motyw</H1>
        <Text tone="secondary">
          Docelowy AppShell. Dziś: nagłówek „Platforma spedycyjna” bez tenanta,
          bez motywu, ⌘K miesza nawigację z akcjami bez filtra uprawnień.
        </Text>
      </Stack>

      <Row gap={16} wrap>
        <Stat value={tenant} label="aktywny tenant" />
        <Stat value="⌘K" label="paleta z grupami" />
        <Stat value={density} label="gęstość shella" />
      </Row>

      <Callout tone="warning" title="Zasada 12 — kontekst tenanta zawsze widoczny">
        Przełącznik organizacji w shell barze. Żadne zapytanie UI nie sięga po
        dane innego tenanta. Brak tenanta = odmowa, nie pusty katalog.
      </Callout>

      <ShellChrome
        route={route}
        onRoute={setRoute}
        tenant={tenant}
        onTenant={setTenant}
        dark={dark}
        onDark={setDark}
        density={density}
        onDensity={setDensity}
        paletteOpen={paletteOpen}
        onPalette={setPaletteOpen}
        noticesOpen={noticesOpen}
        onNotices={setNoticesOpen}
        crumbs={crumbs}
      />

      {paletteOpen ? (
        <PalettePanel query={query} onQuery={setQuery} />
      ) : noticesOpen ? (
        <NoticesPanel />
      ) : (
        <Callout tone="neutral" title="Obszar roboczy">
          Tu wchodzi DataTableShell / HITL / wycena. Shell nie dubluje joba
          operatora — pulpit zostaje listą jobów (U-admin-ref).
        </Callout>
      )}

      <H2>Uprawnienia OpenFGA w UI</H2>
      <Grid columns={2} gap={16}>
        <Stack gap={8}>
          <H3>Ukryj vs wyszarzyj</H3>
          <Table
            headers={["Sytuacja", "UI"]}
            rows={[
              ["Brak relacji w FGA", "Ukryj pozycję palety i nawigacji"],
              ["Ma read, nie write", "Wyszarzyj akcję · 403 z uzasadnieniem"],
              ["Cross-tenant", "Nie pokazuj rekordu. Nie 404-teatr."],
              ["Accept HITL bez reviewer", "Przycisk nie istnieje"],
            ]}
          />
        </Stack>
        <Stack gap={8}>
          <H3>Skróty poza ⌘K</H3>
          <Table
            headers={["Skrót", "Kontekst"]}
            rows={[
              ["⌘K", "globalnie — paleta"],
              ["G potem R", "goto stawki (chord)"],
              ["?", "ściąga skrótów widoku"],
              ["Esc", "zamyka paletę / panel"],
            ]}
          />
        </Stack>
      </Grid>
    </Stack>
  );
}

function ShellChrome({
  route,
  onRoute,
  tenant,
  onTenant,
  dark,
  onDark,
  density,
  onDensity,
  paletteOpen,
  onPalette,
  noticesOpen,
  onNotices,
  crumbs,
}: {
  route: string;
  onRoute: (id: string) => void;
  tenant: string;
  onTenant: (id: string) => void;
  dark: boolean;
  onDark: (v: boolean) => void;
  density: string;
  onDensity: (v: string) => void;
  paletteOpen: boolean;
  onPalette: (v: boolean) => void;
  noticesOpen: boolean;
  onNotices: (v: boolean) => void;
  crumbs: string[];
}) {
  const theme = useHostTheme();

  return (
    <div
      style={{
        border: `1px solid ${theme.stroke.tertiary}`,
        borderRadius: 6,
        overflow: "hidden",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          padding: "6px 12px",
          background: theme.bg.elevated,
          borderBottom: `1px solid ${theme.stroke.tertiary}`,
          fontSize: 12,
        }}
      >
        <Text weight="semibold">OmniRoute</Text>
        <select
          aria-label="Organizacja"
          value={tenant}
          onChange={(event: { target: { value: string } }) => onTenant(event.target.value)}
          style={{
            fontSize: 12,
            padding: "2px 6px",
            background: theme.bg.editor,
            color: theme.text.primary,
            border: `1px solid ${theme.stroke.secondary}`,
            borderRadius: 4,
          }}
        >
          <option value="sped-bałtyk">Sped Bałtyk</option>
          <option value="nordic-fwd">Nordic Forwarding</option>
        </select>
        <span style={{ color: theme.text.tertiary }}>/</span>
        {crumbs.map((crumb, index) => (
          <span key={crumb}>
            <Text as="span" size="small">
              {crumb}
            </Text>
            {index < crumbs.length - 1 ? (
              <Text as="span" size="small" tone="tertiary">
                {" / "}
              </Text>
            ) : null}
          </span>
        ))}
        <Spacer />
        <Row gap={8} align="center">
          <Text size="small" tone="secondary">
            {dark ? "ciemny" : "jasny"}
          </Text>
          <Toggle checked={dark} onChange={onDark} />
          <span>
            <Pill
              active={density === "compact"}
              size="sm"
              onClick={() =>
                onDensity(density === "compact" ? "comfortable" : "compact")
              }
            >
              {density}
            </Pill>
          </span>
          <Button
            variant={noticesOpen ? "primary" : "secondary"}
            onClick={() => {
              onNotices(!noticesOpen);
              onPalette(false);
            }}
          >
            2
          </Button>
          <Button
            variant={paletteOpen ? "primary" : "secondary"}
            onClick={() => {
              onPalette(!paletteOpen);
              onNotices(false);
            }}
          >
            Akcje ⌘K
          </Button>
        </Row>
      </div>
      <div style={{ display: "flex", minHeight: 220 }}>
        <nav
          style={{
            width: 168,
            background: theme.bg.chrome,
            borderRight: `1px solid ${theme.stroke.tertiary}`,
            padding: 8,
          }}
        >
          <Text size="small" tone="tertiary">
            gęsty admin
          </Text>
          {NAV.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => onRoute(item.id)}
              style={{
                display: "block",
                width: "100%",
                textAlign: "left",
                marginTop: 2,
                padding: "4px 8px",
                fontSize: 12,
                border: "none",
                borderRadius: 4,
                background: route === item.id ? theme.fill.secondary : "transparent",
                color: theme.text.primary,
                cursor: "pointer",
              }}
            >
              {item.label}
            </button>
          ))}
        </nav>
        <div style={{ flex: 1, padding: 16 }}>
          <H3>{NAV.find((item) => item.id === route)?.label ?? "Pulpit"}</H3>
          <Text size="small" tone="secondary">
            Tenant `{tenant}` · motyw {dark ? "ciemny" : "jasny"} · gęstość{" "}
            {density}. Condensed nie przełącza się tutaj — tylko w gridzie stawek.
          </Text>
        </div>
      </div>
    </div>
  );
}

function PalettePanel({
  query,
  onQuery,
}: {
  query: string;
  onQuery: (v: string) => void;
}) {
  const q = query.trim().toLowerCase();
  const visible = PALETTE.filter(
    (item) => q === "" || item.label.toLowerCase().includes(q),
  );
  const groups: PaletteGroup[] = ["nawigacja", "akcje", "rekordy"];

  return (
    <Stack gap={12}>
      <H2>Paleta poleceń</H2>
      <TextInput
        value={query}
        onChange={onQuery}
        placeholder="Szukaj akcji, nawigacji, rekordów…"
      />
      {groups.map((group) => {
        const rows = visible.filter((item) => item.group === group);
        if (rows.length === 0) {
          return null;
        }
        return (
          <div key={group}>
            <Stack gap={6}>
              <Text size="small" weight="semibold" tone="secondary">
                {group}
              </Text>
              <Table
                headers={["Pozycja", "Skrót", "Uprawnienie"]}
                rows={rows.map((item) => [
                  item.label,
                  item.hint === "" ? "—" : item.hint,
                  item.allowed ? "widoczna" : "ukryta (brak can_export)",
                ])}
                rowTone={rows.map((item) => (item.allowed ? "success" : "neutral"))}
              />
            </Stack>
          </div>
        );
      })}
      <Text size="small" tone="tertiary">
        Eksport CSV nie wchodzi na listę, gdy FGA nie ma `can_export`. Nie
        mieszaj rekordów z akcjami w jednej grupie. Antywzorzec z badania:
        wyniki dopiero po Enter.
      </Text>
    </Stack>
  );
}

function NoticesPanel() {
  return (
    <Stack gap={8}>
      <H2>Powiadomienia</H2>
      <Table
        headers={["Zdarzenie", "Kontekst"]}
        rows={NOTICES.map((item) => [item.title, item.detail])}
        rowTone={["warning", "info"]}
      />
      <Text size="small" tone="tertiary">
        To nie toast-spam. Lista jobów operatora, te same co pulpit.
      </Text>
    </Stack>
  );
}
