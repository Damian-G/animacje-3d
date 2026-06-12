# Projekt Końcowy - Miasto Nocą

[![](https://img.shields.io/badge/Blender-4.x-orange?style=for-the-badge&logo=blender&logoColor=white)](#)
[![](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)](#)
[![](https://img.shields.io/badge/Status-Gotowy%20do%20oceny-success?style=for-the-badge)](#)

**Kurs:** Systemy Animacji Komputerowej  
**Autor:** [Damian Grzyb]  
**Technologia:** Blender 4.x (Python bpy + GUI)  

---

## 1. Opis sceny
Animacja przedstawia widok z perspektywy osoby idącej chodnikiem w środku deszczowej nocy przez miejski korytarz. Głównym założeniem projektu było stworzenie mrocznego, kinowego klimatu w stylistyce cyberpunk / synthwave. 

Kluczowe elementy budujące nastrój sceny:
* **Efekty świetlne:** Kontrast pomiędzy głębokim mrokiem nocy a jaskrawymi, wielokolorowymi neonami na budynkach oraz reflektorami samochodów.
* **Mokra nawierzchnia:** Zaawansowany materiał chodnika i asfaltu (wykorzystujący Principled BSDF oraz mapy Roughness/Specular), który realistycznie odbija światła otoczenia, tworząc efekt lustra na deszczowej ulicy.
* **Dynamika:** Dynamiczny ruch dwóch mijających się pojazdów (sportowego McLarena oraz auta miejskiego) zestawiony z gęstym opadem deszczu reagującym na oświetlenie sceny.
* **Proceduralność:** Pasy zieleni wzdłuż drogi zostały automatycznie obsiane zróżnicowaną roślinnością.
* **Oprawa dźwiękowa (Audio): Dźwięk obejmujący przestrzenne odgłosy ulewnego deszczu w tle.
---

## 2. Instrukcja uruchomienia i renderowania
Aby poprawnie otworzyć projekt i wyrenderować animację, należy wykonać poniższe kroki:

1. Pobierz cały katalog `lab_15` i zachowaj strukturę plików.
2. Otwórz program Blender (zalecana wersja 4.x).
3. Wejdź w **File -> Open** i wybierz plik `assets/scena.blend`.
4. Przejdź do zakładki **Scripting** na górnym pasku Blendera.
5. W oknie edytora tekstu zobaczysz skrypty Python. Kliknij ikonę **Run Script** (symbol „Play”), żeby zainicjować systemy cząsteczkowe, rozsiać roślinność oraz wygenerować klatki kluczowe dla ruchu kamery i pojazdów.
6. Powróć do zakładki **Layout**. Wciśnij **Spację**, aby odtworzyć animację w podglądzie (Viewport).
7. Aby wyrenderować gotowy plik wideo, upewnij się, że w zakładce *Output Properties* ustawiony jest format *FFmpeg Video* (kodowanie MP4), a następnie wciśnij skrót **Ctrl + F12** (Render Animation). Gotowe.

---

## 3. Opis komponentu skryptowego (Python `bpy`)
Projekt wykorzystuje elastyczny kod Python do automatyzacji i generowania kluczowych elementów animacji. Zgodnie z wymaganiami, parametry sterujące zostały wyciągnięte na początek kodu w postaci zmiennych zapisanych wielkimi literami.

Skrypt realizuje 4 główne zadania:

### A. Symulacja chodu POV (Kamera)
Skrypt oblicza pozycję kamery dla każdej klatki (od 1 do 150), dodając do ruchu postępowego matematyczne funkcje trygonometryczne (`sinus` dla kołysania pionowego, `cosinus` dla kołysania bocznego). Pozwoliło to na uzyskanie płynnego, naturalnego efektu kroków człowieka.
* `PREDKOSC_KROKOW` – częstotliwość stąpnięć.
* `AMPLITUDA_PIONOWA` / `AMPLITUDA_POZIOMA` – siła kołysania kamery.
* `PREDKOSC_MARSZU` – prędkość, z jaką kamera przemieszcza się wzdłuż ulicy.

### B. Generator deszczu
Proceduralnie tworzy obiekt bazowy kropli (spłaszczona i wydłużona geosfera), przypisuje mu błękitny materiał z emisją światła (*Emission Strength*), a następnie konfiguruje emiter cząsteczek nad miastem oraz dodaje siłę fizyczną wiatru (*Turbulence*).
* `INTENSYWNOSCDESZCZU` – ogólna liczba kropel w scenie.
* `PREDKOSC_OPADANIA` / `CHAOS_PRĘDKOSCI` – parametry fizyki opadu.
* `MOC_EMISJI_DESZCZU` – jasność świecenia kropel w ciemności.

### C. Automatyzacja ruchu pojazdów
Funkcja `animuj_pojazd` dynamicznie czyści stare animacje z pamięci Blendera i nakłada klatki kluczowe pozycji (`location`) na osi Y dla wskazanych obiektów, pozwalając im na płynne mijanie się z różnymi prędkościami.
* `PREDKOSC_AUTA_1` / `PREDKOSC_AUTA_2` – prędkości przypisane do konkretnych modeli samochodów.

### D. Proceduralny generator rozmieszczenia obiektów (Kwiaty)
Dodatkowy zaawansowany komponent kodu. Skrypt automatycznie buduje z prymitywów 3D bazy trzech gatunków kwiatów (Stokrotka, Mak, Tulipan), nadaje im wygładzenie i materiały, a następnie za pomocą modułu `random.uniform` rozsiewa je z losową skalą i obrotem w granicach geometrycznych obiektów `Pas_Zieleni_Lewy` i `Pas_Zieleni_Prawy`.
* `GĘSTOŚĆ_KWIATÓW` – liczba roślin generowana na każdym pasie zieleni.

---

## 4. Lista użytych assetów i elementy własne

Projekt łączy modele zrobione ręcznie, elementy wygenerowane automatycznie przez kod oraz gotowe z bazy.

### A. Własne modele (Zrobione ręcznie)
* **Infrastruktura:** Budynki, latarnie uliczne, chodniki oraz krawężniki – wymodelowane od zera z podstawowych brył (Cube i Cylinder).

### B. Elementy generowane przez kod Python (Proceduralne)
* **Deszcz:** Skrypt automatycznie tworzy geometrię kropli, emiter, ustawia całą fizykę cząsteczek oraz dodaje wiatr.
* **Kwiaty:** Skrypt sam buduje od zera geometrię trzech gatunków kwiatów (łodygi, środki, płatki), nadaje im kolory i losowo rozsiewa je na pasach zieleni.

### C. Pobrane modele i tekstury
1. **McLaren** (Samochód 1) – BlenderKit (Licencja: Free / CC0)
2. **Cartoon Car** (Samochód 2) – BlenderKit (Licencja: Free / CC0)
3. **Asphalt Procedural** (Tekstura drogi) – BlenderKit (Licencja: Free / CC0)
4. **Night/City HDRI** (Światło tła) – Poly Haven (Licencja: CC0)
   * *Uwaga:* Moc HDRI została mocno zmniejszona w opcjach *World*, aby utrzymać mroczny, nocny klimat sceny.
5. Efekt dźwiękowy (rain.mp3) – Pixabay (Licencja: Pixabay Content License / Darmowe do użytku komercyjnego i niekomercyjnego).
---

## 5. Znane bugi i ograniczenia
* **Pamięć podręczna systemu cząsteczek:** Przy zmianie wartości zmiennej `INTENSYWNOSCDESZCZU` bezpośrednio w kodzie, należy ręcznie odświeżyć pamięć podręczną Blendera (kliknąć klatkę `0` na osi czasu), aby system cząsteczek zaktualizował gęstość opadu.
* **Ograniczenie klatek:** Animacja jest zoptymalizowana pod sztywny przedział 1-150 klatek. Zwiększenie zakresu w samym Blenderze bez zmiany zmiennej `END_FRAME` w skrypcie spowoduje zatrzymanie ruchu obiektów po 6 sekundzie.
