# Budjetointisovellus
- [vaatimusmaarittely](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/vaatimusmaarittely.md)  
- [tuntikirjanpito](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/tuntikirjanpito.md)  
- [changelog](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/changelog.md)
- [arkkitehtuuri](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/arkkitehtuuri.md)
- [release](https://github.com/eerolasi/ot-harjoitustyo/releases/tag/viikko5)
## Käyttöohjeet

Jos lataa koodin viikon5 releasen kautta on se alustettava manuaalisesti:
- luo budgetapp-hakemistoon data-hakemisto
- luo data hakemistoon tiedosto .gitkeep

Siirry budgetapp-hakemistoon
1. Asenna riippuvuudet:  

```
poetry install
```
2. Alusta sovellus:
``` 
poetry run invoke build
```
3. Käynnistä sovellus:
```
poetry run invoke start
```

Testaus:
```
poetry run invoke test 
```
Testikattavuus:
```
poetry run invoke coverage-report
```
Pylint:
```
poetry run invoke lint
```


