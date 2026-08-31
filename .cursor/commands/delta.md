---
description: Tworzy szkielet delta-spec dla plastra
---

Argument: identyfikator plastra z `docs/MODULES.md`.

Utwórz `docs/deltas/open/<id>.md` wg szablonu:

# Plaster <id> · <M-xx> <nazwa modułu>
**Spec źródłowa:** docs/spec/<moduł>.md, sekcje <x–y>
**Zależy od:** <lista plastrów>

## Zakres
<co powstaje — trzy zdania maksimum>

## Poza zakresem
<co świadomie zostaje na później — to jest ważniejsze od zakresu>

## Ustalenia
<decyzje podjęte przed startem, np. która data odniesienia>

## Kryteria akceptacji
- [ ] <sprawdzalne maszynowo>
- [ ] <test izolacji tenantów, jeśli nowa tabela>
- [ ] <budżet wydajności, jeśli ścieżka krytyczna>

Wypełnij tyle, ile wynika ze spec. Puste miejsca oznacz jako DO USTALENIA
i wypisz je na końcu jako pytania do mnie.
