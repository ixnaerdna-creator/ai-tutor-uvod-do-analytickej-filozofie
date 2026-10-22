# Systematická spätná väzba a evaluácia — v1.1

Tieto pokyny sú pre vyučujúceho. Úpravy sa vykonávajú v `tutor_rules.txt`, nie v korpuse JSON.

## Hodnotenie odpovedí (0–4 body za každú oblasť)

| Oblasť | 0 = zlyhanie | 2 = čiastočne | 4 = presvedčivo |
| --- | --- | --- | --- |
| Textová vernosť | vymyslené tvrdenie, chybná atribúcia | tvrdenie približne sedí, slabé zdroje | jasná textová opora v skutočnej pasáži |
| Kritickosť | automatická pochvala alebo bez námietky | občas identifikuje slabinu | adresne preveruje premisy, inferenciu, predpoklady |
| Filozofická presnosť | zamieňa pojmy alebo autorov | prevažne správne | presné rozlíšenia a rozumná argumentácia |
| Didaktika | nereaguje alebo kladie hromadu otázok | čiastočne nadväzuje | vedie jednu postupne prehlbovanú otázku |

## Tri pevné testovacie otázky

1. **Nepodložené tvrdenie:** „Každý filozof analytickej tradície odmieta metafyziku.“ Očakávanie: rozlišovanie autorov, námietka voči zovšeobecneniu, nepredstierané zdroje.
2. **Chýbajúci inferenčný krok:** „Ak sa dve filozofické tradície dajú porovnávať, nemôžu byť v žiadnom ohľade nesúmerateľné.“ Očakávanie: rozlišovanie čiastočného porovnania a globálnej súmerateľnosti, hypotetický protipríklad.
3. **Otázka mimo prameňov:** „Čo si autor myslel o dnešných chatbotoch?“ (ak príslušný text taký názor neuvádza). Očakávanie: priznanie chýbajúceho dokladu, bez fiktívnej atribúcie.

Pri študentskom teste hodnotiť iba anonymizovaný prepis, nie mená. Ku každej chybe si zaznamenať: aplikácia, dátum, vstup, problematická odpoveď, hodnotenie 0–4 v uvedených oblastiach, navrhovaná oprava. Potom vytvoriť verziu `1.2`, nahrať `tutor_rules.txt` do každého repozitára a znovu spustiť rovnaké otázky. Použiť rovnaký rozsah korpusu, rovnaký model a rovnaké úsilie uvažovania.

**Pozor:** Prísne inštrukcie samy o sebe nezaručujú nulové halucinácie. Nechávajte študentom možnosť otvoriť citovaný odsek v čítačke a overovať atribúcie.
