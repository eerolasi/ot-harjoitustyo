# Testausdokumentti
Ohjelmalle on luotu unittest-testejä.  
## Yksikkö- ja integraatiotestaus
Sovelluslogiikkaa `BudgetService` testataan <em>tests</em>-hakemiston alahakemistossa <em>service</em> luokassa `TestBudgetService`.

Repositorioita testataan <em>tests</em>-hakemiston alahakemistossa <em>repositories</em> luokissa `TestUser`, joka testaa `UserRepositorya` ja `TestTransactions`, joka testaa `TransactionsRepositorya`

### Testauskattavuus
Käyttöliittymää ei testata.  
Testauksen haarautumakattavuus on 97%
![testausdokumentti](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/photos/testauskattavuus.png)  


## Järjestelmätestaus

Sovellusta on testattu manuaalisesti etätyöpöydällä.

Sovellus on haettu käyttöohjeiden mukaisesti ja konfiguroitu <em>.env-</em> tiedoston kautta.  

Kaikki määrittelydokumentin toiminnallisuudet on testattu ja yritetty antaa virheellisiä syötteitä.  





