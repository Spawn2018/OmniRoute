# Machine — styl to test, nie autorecenzja

**Status:** machine. Orakulum: `craft_style.scan_errors` + sufit w `quality_floor`.

Kod produktu (`backend/app`, `frontend/src` bez `*.gen.ts`) nie wnosi TODO, `except Exception`, `float()`, echo-komentarza nad `def`, `as any`, banerów ani emoji. Komentarz mówi *dlaczego* (VAT, RLS), nie powtarza nazwy funkcji.

Nowa funkcja >40 linii podnosi `long_functions` / `long_function_overflow` i pada `quality_floor`. Nie twierdź, że testy robią z agenta człowieka — merytoryka zostaje w recenzji i HC.
