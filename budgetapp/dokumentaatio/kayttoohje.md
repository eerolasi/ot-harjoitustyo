# Käyttöohje

## Ohjelman käynnistäminen

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

## Kirjautuminen
Sovellus käynnistyy kirjautumisnäkymästä, jossa kirjaudutaan sisään olemassaolevilla käyttäjätiedoilla tai siirrytään luomaan uusi käyttäjätunnus.

![kirjautuminen]((https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/photos/kirjautuminen.png)

## Käyttäjän luonti
Käyttäjä luodaan antamalla käyttäjätunnus ja salasana ja painamalla "Luo". Sivulta voi myös siirtyä takaisin kirjautumisnäkymään.

![rekisterointi](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/photos/rekisterointi.png)
