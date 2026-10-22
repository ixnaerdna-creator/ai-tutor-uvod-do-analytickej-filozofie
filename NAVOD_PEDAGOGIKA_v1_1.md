# Jednotná aktualizácia pedagogických pravidiel AI tútorov – verzia 1.1

**Obsah:** jedenásť samostatných projektov GPT-6 Luna / medium, spoločné pravidlá hodnotenia a práce s výhradne priloženými textmi. Texty JSON zostali bez zmien.

## 1. Prvá aktualizácia existujúcej Streamlit aplikácie

1. Rozbaľte príslušný projekt zo spoločného ZIP archívu; jeho priečinok obsahuje `app.py`, `tutor_rules.txt`, `pedagogical_rules.py`, `openai_backend.py`, `tutor_core.py`, ďalšie súbory a testy.
2. V GitHube otvorte **existujúci** repozitár daného tútora, napríklad `ai-tutor-zaver-analytickej-filozofie`, a nahrajte všetky súbory z príslušného priečinka do koreňa repozitára. Neodstraňujte existujúce autorizované súbory, ktoré v archíve nie sú (najmä `text.json` pre Traktát).
3. Na Streamlit Community Cloud ponechajte správny repozitár, vetvu `main` alebo `master` a `app.py`; v Secrets ponechajte vlastný API kľúč a modelové nastavenia nižšie. Nastavenie Secrets nemení textové pravidlá – tie sú v GitHub súboroch.
4. Po nasadení reštartujte Streamlit aplikáciu, najmä ak ste menili iba `tutor_rules.txt`, aby sa prejavila zmena pravidiel a opakovane načítali cached moduly.
5. Otestujte jeden výklad odseku, aspoň jednu kritickú repliku a zobrazenie odkazu na skutočný zdrojový odsek. Skontrolujte, že bez textovej opory AI prizná limit a pri poslednom, 20. vstupe už nekladie ďalšiu otázku.

### Streamlit Secrets (rovnaké pre všetkých tútorov)

```toml
OPENAI_API_KEY = "VÁŠ_SÚKROMNÝ_KĽÚČ"
OPENAI_MODEL = "gpt-6-luna"
OPENAI_REASONING_EFFORT = "medium"
OPENAI_TIMEOUT_MS = 120000
```

Skutočný kľúč patrí výhradne do Streamlit Secrets, nikdy do GitHubu. Študentom sa nezobrazujú ceny ani tokeny.

## 2. Ako po spätnej väzbe upravovať pravidlá

V každom projekte otvorte súbor `tutor_rules.txt`. Sekcie sú:

- `[COMMON]`: striktne uzavreté zdroje, rozlišovanie explicitného výroku, rekonštrukcie a námietky, odkazy na doložené záznamy.
- `[EXPLANATION]`: interpretácia kliknutého odseku bez spotrebovania diskusného kroku.
- `[DIALOGUE]`: vecná kritickosť, skúmanie premís a inferencií, žiadne automatické pochvaly, na konci kroku najviac jedna otázka, po kroku 20 žiadna.

Pôvodné odborné inštrukcie každého autora zostali v `app.py`. Nový súbor sa k nim pripája pomocou `pedagogical_rules.py`. NEMEŇTE v bežných iteráciách `tutor_core.py` ani JSON, ak máte za cieľ iba upraviť kritickosť či formu výkladu.

Pri každej úprave súbor uložte, aktualizujte verziu komentára, urobte GitHub commit a zopakujte pevné skúšobné otázky zo súboru `SPATNA_VAZBA_A_TESTY.md`. Rovnaké pravidlá treba preniesť do **všetkých** jedenástich repozitárov; nejde o jedno automaticky zdieľané centrálne uloženie.

## 3. Limity

Toto je zmena riadiacich inštrukcií modelu, nie vytrénovanie nového modelu ani formálny dôkaz absencie halucinácií. Pravidlá požadujú citovanie **len skutočne sprístupnených odsekov**; pri neúspešnom lokálnom vyhľadaní musí model priznať neúplnú textovú oporu. Presnosť sa preto overuje anonymizovanými dialógmi a otvorením citovaných odsekov.

Niektoré pôvodné README obsahujú staršie príklady modelov alebo poznámky o Gemini: v aktualizovanej verzii sú nadradené tieto inštrukcie v1.1 a skutočné aktuálne nastavenie cez Streamlit Secrets.

## 4. Technická kontrola

Testovanie pri zostavení: jedenásť aplikácií, 176 lokálnych automatizovaných kontrol vrátane pravidiel, backendu a jednotkových testov korpusov. Živé odpovede OpenAI API ani skutočné 20-krokové dialógy neboli bez vášho kľúča spustené.
