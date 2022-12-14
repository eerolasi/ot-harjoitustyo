# Budjetointisovellus
Sovelluksen avulla voi seurata rahankäyttöään. Käyttäjä voi lisätä ja nollata budjettinsa sekä lisätä menoja ja tuloja.
- [vaatimusmäärittely](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/vaatimusmaarittely.md)  
- [tuntikirjanpito](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/tuntikirjanpito.md)  
- [changelog](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/changelog.md)
- [arkkitehtuuri](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/arkkitehtuuri.md)
- [käyttöohje](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/kayttoohje.md)
- [viimeisin release](https://github.com/eerolasi/ot-harjoitustyo/releases/tag/loppupalautus)
- [testausdokumentti](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/testausdokumentti.md)
### Python-versio  
- Sovellus toimii Pythonin versiolla 3.8

### Sovelluksen alustus
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

### Testaus:
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


