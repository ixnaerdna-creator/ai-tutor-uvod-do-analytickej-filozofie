# AI tútor – Úvod do analytickej filozofie

Samostatný študijný projekt pre predmet **Úvod do analytickej filozofie**. Streamlit aplikácia sprístupňuje deväť pôvodných dodaných textov, lokálnu čítačku s vyhľadávaním, výklad vybraného odseku prostredníctvom Gemini a 20-krokový sokratovský dialóg.

## Obsah

1. Pavel Cmorej – *Čo je a čo nie je súčasná analytická filozofia*
2. Dagfinn Føllesdal – *Analytická filozofia: Čo je a prečo sa jej venovať?*
3. Hans-Johann Glock – *Čo je analytická filozofia? – Úvod* (**iba úvodná kapitola knihy**)
4. P. M. S. Hacker – *Analytická filozofia: čo je, odkiaľ pochádza a kam smeruje?*
5. Peter Hylton – *Analýza v analytickej filozofii*
6. Anat Matar – *Analytická filozofia: racionalizmus verzus romantizmus*
7. Jaroslav Peregrin – *Co je to analytická filosofie* (**v češtine**)
8. J. J. Ross – *Analytická filozofia ako otázka štýlu*
9. Avrum Stroll – *Analytická filozofia 20. storočia – Systém solera* (**iba prvá kapitola knihy**)

## Funkcie

- **Autor a text:** dva rozbaľovacie zoznamy; výber autora obmedzí zoznam textov.
- **Čítačka:** vlastný 770-pixelový posuvník so spoľahlivým posunom na začiatok i úplný koniec; voľba nadpisu/oddielu a skok na konkrétny **pracovný odsek DOCX**. Pracovné číslovanie nie je autorským § ani stranou pôvodného vydania.
- **Vyhľadávanie v otvorenej štúdii:** označí jeden aktuálny nález, šípky prechádzajú ďalšie; funguje aj bez Gemini. Vyhľadávanie zachováva polohu a výraz pri prerenderovaní komponentu.
- **Vyhľadávanie v celom korpuse:** lokálny index, ktorý vráti pasáže a otvorí ich vo vybranom texte.
- **Výklad:** klik na bežný odsek, citát, tézu, položku zoznamu či Peregrinovu chronologickú tabuľku otvorí AI výklad bez zvýšenia počtu diskusných vstupov.
- **Sokratovský dialóg:** maximálne 20 **úspešne spracovaných študentských vstupov**. Zvolený rozsah (*jedna štúdia*, *jeden autor* alebo *všetkých deväť textov*) sa uzamkne po prvej otázke. Posledný vstup obsahuje záverečné kritické zhodnotenie práce študenta s argumentmi.
- **Chyby Gemini API:** pri 429, 503, 404, prístupových problémoch a timeoutoch sa neúspešný vstup **nezapočíta**. Otázku možno vedome zopakovať alebo zrušiť.
- **Export TXT:** zápis celého dialógu vrátane metadát a hodnotenia.

## Nasadenie na GitHub + Streamlit Community Cloud

1. Vytvorte **samostatný** repozitár napríklad `ai-tutor-uvod-do-analytickej-filozofie`.
2. Rozbaľte ZIP a nahrajte **obsah priečinka** projektu priamo do koreňa repozitára. `app.py`, `book_reader.py`, `tutor_core.py` a JSON musia byť vedľa seba.
3. V [Streamlit Community Cloud](https://share.streamlit.io/) vytvorte novú aplikáciu: vyberte repozitár a hlavný súbor `app.py`.
4. V nastaveniach aplikácie (**Settings → Secrets**) vložte hodnoty podľa `.streamlit/secrets.toml.example`:

```toml
GEMINI_API_KEY = "VÁŠ_EXISTUJÚCI_KĽÚČ"
GEMINI_MODEL = "gemini-3.5-flash-lite"
GEMINI_TIMEOUT_MS = 120000
```

5. Reštartujte aplikáciu po zmene Secrets. Dostupné modely pre vlastný projekt overte v [oficiálnej dokumentácii Gemini](https://ai.google.dev/gemini-api/docs/models). Ak sa objaví chyba `404`, model uvedený v Secrets nie je pre konkrétny projekt prístupný; ak `429`, môže ísť o kvótu.

### Lokálne spustenie

```bash
python -m venv .venv
# Aktivujte venv podľa operačného systému
pip install -r requirements.txt
streamlit run app.py
```

Pre lokálne API volania uložte svoj skutočný kľúč do *necommitovaného* `.streamlit/secrets.toml`, alebo nastavte premennú prostredia `GEMINI_API_KEY`.

## Overenie

```bash
pip install pytest playwright
pytest -q tests/test_core.py
python tests/test_reader_browser.py
```

Test prehliadača používa systémový `/usr/bin/chromium`; ak ho váš počítač nemá, prispôsobte `executable_path` v skripte alebo použite `playwright install chromium`.

## Kvalita zdrojov a hranice AI

Korpus obsahuje **9 textov, 754 záznamov a 488 obsahových blokov** v projektovej kópii. Poznámky, bibliografické položky a redakčné informácie sa zobrazujú v čítačke, ale nevstupujú do lokálneho vyhľadávania hlavných filozofických pasáží. Jediná oprava štruktúry oproti pôvodnému JSON: `AF05-0003`, úvodný obsahový odsek štúdie Hyltona, je správne označený ako `paragraph` namiesto `front_matter`; slová sa nemenili.

**Princíp textovej vernosti:** tutor má odpovedať iba na základe výňatkov dodaného korpusu. Implementácia používa lexikálne vyhľadávanie a do API posiela **relevantný výber úryvkov**, nie celú knižnicu naraz. Takéto nastavenie znižuje riziko nedoložených tvrdení, ale nedokáže absolútne zaručiť, že model nepridá nepodložené informácie. Pri výklade je preto nutné overovať presné formulácie v texte.

Preklady neboli úplne kolacionované podľa pôvodných vydaní. **Pôvodné čísla strán nie sú pri jednotlivých odsekoch spoľahlivo doložené**: zobrazované poradie odsekov nie je číslo stránky. Bibliografia a zahrnuté citácie nie sú automaticky názorom autora štúdie.

**Autorské práva:** Pred sprístupnením plných textov na verejnom GitHube alebo verejnej aplikácii overte, že máte potrebné oprávnenie na publikovanie prekladov. Zvážte súkromné repo a podľa potreby prístupový režim aplikácie.

## Štruktúra projektu

```
ai-tutor-uvod-do-analytickej-filozofie/
├── app.py
├── book_reader.py
├── tutor_core.py
├── uvod_do_analytickej_filozofie_texty.json
├── requirements.txt
├── .gitignore
├── .streamlit/secrets.toml.example
├── README.md
├── POZNAMKY_K_TEXTOM.md
└── tests/
    ├── test_core.py
    └── test_reader_browser.py
```
