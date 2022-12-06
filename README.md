# Budjetointisovellus
- [vaatimusmaarittely](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/vaatimusmaarittely.md)  
- [tuntikirjanpito](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/tuntikirjanpito.md)  
- [changelog](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/changelog.md)
- [arkkitehtuuri](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/arkkitehtuuri.md)

## Käyttöohjeet
Siirry aluksi budgetapp hakemistoon

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


