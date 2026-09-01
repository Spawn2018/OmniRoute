# Bicie serca nocy (szablon)

Agent `/noc` kopiuje ten kształt do lokalnego pliku o nazwie `NOC-LIVE.md` **w tym samym katalogu**. Żywy plik jest w `.gitignore` i nie wchodzi do gita.

```
until: 2026-09-02T07:00:00+02:00
status: idle
last_beat: 2026-09-01T22:00:00+02:00
```

`status`: `busy` (pytest/commit), `idle` (między cyklami), `stop` (zmiana skończona).
