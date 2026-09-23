# Notatka przekazania SBAR

Na `/handover-notes` zapisujesz **wpis przekazania zmiany** z czterema polami tekstu.

1. Wejdź na Notatka SBAR.
2. Wklej `note_code` (snake 2–32) oraz `source_ref` (`fixture://handover-note/…` albo `tenant:manual`).
3. Wypełnij cztery pola: sytuacja, tło, ocena, rekomendacja (1–2000 znaków każde).
4. „Zapisz notatkę SBAR” wstawia wiersz.

Czego tu nie ma: auto z tablicy planowania, drugi czat, LLM, znacznik katalogu kind (`/handover-sbar-marks`), kwota, live HTTP.

Nazwy w kodzie: `handover_note` · `note_code` · `situation` · `background` · `assessment` · `recommendation` · `source_ref` · `/handover-notes`.

Osobno na `/handover-bind-marks` zapisujesz **stance wiązania** (`note`|`board`|`shift`|`other`) — bez FK UUID i bez tablicy T6.
