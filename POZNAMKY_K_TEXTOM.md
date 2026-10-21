# Poznámky k zdrojovému korpusu

Všetkých deväť textov pochádza z dokumentov DOCX dodaných v rozhovore. Využíva sa existujúci JSON so zachovaným textovým znením. Slovenská a česká terminológia nebola novým prekladom upravovaná.

## Štruktúra

- 9 autorov, 9 textov, 754 záznamov.
- Obsahové bloky určené na individuálny výklad: `paragraph`, `quotation`, `thesis`, `list_item`, `table`. V projektovom JSON ich je 488.
- Ďalšie typy: `heading`, `note`, `bibliography`, `source_info`, `front_matter`. Slúžia na zobrazenie kontextu a oddelenie poznámok, nepoužívajú sa ako hlavné argumentačné pasáže vyhľadávania.
- Pri `AF05-0003` je opravený **iba typ záznamu** z `front_matter` na `paragraph`; obsah je bez zmeny. Išlo o prvý odsek Hyltonovej štúdie.
- Peregrinova tabuľka `AF07-0051` je reprezentovaná v `rows` a zobrazuje sa ako 3-stĺpcová HTML tabuľka.
- `source_paragraph` je pracovní identifikátor poradia odseku, nie pôvodné stránkovanie.

## Upozornenia pre interpretáciu

1. Glock a Stroll sú zastúpení iba vybranými kapitolami väčších kníh. Pri Hyltonovi a Hackerovi zachovávajte význam autorových vnútorných nadpisov.
2. Vlastné postoje autorov striktne oddeľujte od citátov iných filozofov a od historických charakteristík.
3. Model používa len výňatky vybrané lokálnym indexom. Ak relevantná pasáž nebola nájdená, treba to priznať, nie vymyslieť dôkaz.
4. Porovnávací dialóg neznamená, že všetci autori majú rovnaký názor na definíciu analytickej filozofie, jazyk, logiku či metódu.
5. Preklady nemajú úplnú filologickú revíziu. Pred ich uverejnením preveriť práva k prekladom.
