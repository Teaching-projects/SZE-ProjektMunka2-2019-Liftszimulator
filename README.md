# SZE-ProjektMunka2-Liftszimulator

## Funkcionális követelmények

#### Állítható paraméterek (főmenüben)

- Emeletek száma
- Liftek száma
- Liftek kapacitása (fő)
- Gyorsulási faktor és végsebesség
- Irányítási mód (3 algoritmus + manuális)
- Utasok száma
- Időkeret, amire el vannak osztva az utasok
- Random seed, ami alapján megismételhető az utasok érkezési eloszlása

#### Algoritmus / operátor információi

Minden emeleten két gomb: fel és le. Vagy meg van nyomva, vagy nem.
Minden liftben az, hogy melyik szintek gombjai vannak megnyomva.

#### Utasok viselkedése

- Utasok beszállása, emelet kiválasztása 0 sec, automatikus
- Haladási irány nincs, így ha megérkezik egy lift, mindenképp beszállnak a várakozók

#### Statisztikai eredmények

- Személyenkénti átlagos idő lifthez érkezéstől célbaérkezésig
- Maximális várakozási idő (lift megérkezéséig)
- Liftek által megtett összes távolság

#### Szimuláció során megjelenítendő információk

- Liftek helyzete
- Liftekben lévő és hívógombok állapota
- Timer is, ami mutatja, hogy mióta van benyomva egy hívógomb
- Liftekben lévő személyek száma
- Aktuális statisztikai eredmények
- Szimuláció közben állítható, hogy megjelenjen-e:
- Hány ember várakozik az egyes szinteken
- Melyik emeletre tartanak

#### Manuális irányítás

- Lift kijelölése, majd emelet megadása
- Liftnek csak álló helyzetben adható parancs

## Nemfunkcionális követelmények

- Windows és Linux platformok támogatása
- 2D vagy 3D grafikus megjelenítés
- Python3
- Legyen egy install script, ami letölti a szükséges csomagokat, pythonon kívül mást ne kelljen kézzel telepítenie a usernek
