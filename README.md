![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=flat&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=flat&logo=Matplotlib&logoColor=black)
![GUI](https://img.shields.io/badge/GUI-Tkinter-red?style=flat)

![Status](https://img.shields.io/badge/Status-Development-orange?style=flat) 

# Python Adatvizualizáló és Plottoló Alkalmazás

Ez a projekt egy asztali (desktop) alkalmazás, amely lehetővé teszi CSV adatok egyszerű kezelését, szerkesztését és vizualizációját. A program Python nyelven íródott, a Tkinter grafikus felület és a Matplotlib könyvtár felhasználásával.

⚠️ Fejlesztési Státusz: Work in Progress (Folyamatban) A projekt jelenleg aktív fejlesztés alatt áll. Az alapvető funkciók működnek, de további fejlesztések várhatók.

## 🛠 Telepítés és Környezet Beállítása

A projekt futtatásához ajánlott egy izolált virtuális környezet (venv) használata. Kövesd az alábbi lépéseket a terminálban:

### 1. Virtuális környezet létrehozása

Navigálj a projekt főkönyvtárába, és futtasd:

`python -m venv venv`


### 2. Környezet aktiválása

Windows:

`venv\Scripts\activate`


macOS / Linux:

`source venv/bin/activate`


(Sikeres aktiválás esetén a terminál sor elején megjelenik a `(venv)` felirat.)

### 3. Függőségek telepítése

A szükséges csomagok telepítése:

`pip install pandas matplotlib`

### 4. Program indítása

`python plotter_app.py`


## 🚀 Jelenlegi Funkciók

A program az alábbi lehetőségeket biztosítja:

- CSV Kezelés:

    - Fájlok beolvasása (Fájl -> CSV Megnyitása).

    - Módosított adatok mentése (Fájl -> CSV Mentése).

- Adattábla:

    - Adatok áttekinthető, táblázatos megjelenítése.

    - Szerkesztés: Dupla kattintással bármely cella értéke módosítható.

- Interaktív Vizualizáció:

    - Grafikon készítése az adatok oszlopai alapján (Plot -> Diagram megjelenítése).

    - Interaktív szerkesztés: A grafikonon lévő vonalra/pontokra kattintva egy szerkesztő ablak ugrik fel.

- Testreszabható tulajdonságok:

    - Vonal színe.

    - Vonal vastagsága (csúszkával).

    - Jelölő (marker) típusa (kör, négyzet, háromszög stb.).

## Lehetséges jövőbeli fejlesztések: 
1. 📊 Vizualizációs Funkciók Bővítése (Magas Prioritás)

Jelenleg a program automatikusan az első két oszlopot ábrázolja vonaldiagramként. Ezt kell rugalmasabbá tenni.

- Oszlopválasztó (Column Selector):

    - Legördülő menük (Dropdown) hozzáadása a diagram ablakhoz, ahol a felhasználó kiválaszthatja, melyik oszlop legyen az X és melyik az Y tengely.

- Több Diagramtípus, lehetőség váltani a típusok között:

    - Vonaldiagram (Line plot - jelenlegi)

    - Oszlopdiagram (Bar chart)

    - Pontdiagram (Scatter plot)

    - Hisztogram (eloszlás vizsgálathoz)

- Feliratok és Címek:

    - Bemeneti mezők a diagram címének, valamint az X és Y tengely feliratainak módosítására.

1. 🛠️ Adatkezelés és Elemzés (Közepes Prioritás)

A táblázat jelenleg csak megjelenít és szerkeszt, de nem "érti" az adatokat.

- Adattípus Validáció:

    - Jelenleg, ha szöveges oszlopot próbálunk plotolni, a program hibára fut. Szűrést kell beépíteni, hogy a tengelyválasztónál csak numerikus oszlopok jelenjenek meg.

- Új Oszlop/Sor Hozzáadása:

    - Gombok a táblázat nézethez: "Új sor hozzáadása" és "Új oszlop számítása" (pl. két oszlop összege).

- Alapvető Statisztikák:

    - Egy oldalsáv vagy popup, ami mutatja a kijelölt oszlop átlagát, minimumát és maximumát.

3. 🎨 UI/UX (Felhasználói Élmény) Modernizálása

A felugró (popup) ablakok működnek, de nehézkesek lehetnek.

- Integrált Szerkesztőpanel (Sidebar):

    - A felugró ablakok helyett (színválasztás, marker) egy fix oldalsáv létrehozása a plot ablak jobb oldalán. Így nem kell mindig bezárni/megnyitni az ablakot a módosításhoz.

- Drag & Drop:

    - Fájlok behúzása az ablakba a megnyitáshoz (TkinterDnD könyvtárral).

- Státuszsor:

    - Lent jelezni a betöltött sorok számát vagy az éppen végrehajtott műveletet.

4. 🛡️ Kódminőség és Stabilitás

- Hibakezelés (Error Handling):

    - try-except blokkok beépítése a fájlbeolvasáshoz (pl. ha a CSV formátuma rossz).

- Konfiguráció Mentése:

    - Megjegyezni az utoljára megnyitott mappa útvonalát vagy az ablak méretét a következő indításra.

## 📄 Licenc
Ez a projekt nyílt forráskódú, és szabadon felhasználható vagy módosítható oktatási és személyes célokra (MIT Licenc).