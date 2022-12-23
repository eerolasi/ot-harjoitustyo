# Käyttöohje
Projektin lähdekoodi löytyy loppupalautus releasesta Assets osion alta. Pura koodi

## Konfigurointi
Tiedostojen pysyväistallennuksesta vastaavat tiedostot luodaan automaattisesti <em>data</em>-hakemistoon, jos niitä ei ole siellä vielä. 

Halutessaan voi tietojen tallennukseen käytettävien tiedostojen nimiä muokata projektin juuressa olevassa <em>.env</em>-tiedostossa, jonka muoto on:
```
DATABASE_FILENAME=database.sqlite
```

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

![kirjautuminen](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/photos/kirjautuminen.png)

## Käyttäjän luonti
Käyttäjä luodaan antamalla käyttäjätunnus ja salasana ja painamalla "Luo". Sivulta voi myös siirtyä takaisin kirjautumisnäkymään.

![rekisterointi](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/photos/rekisterointi.png)

## Budjetin asettaminen
Käyttäjä voi asettaa budjetin kohdan Anna budjettisi: alla olevaan kenttään ja painaa kentän alla olevaa lisää-painikeella. Kun budjetti on asetettu poistuu budjetinasettamisen vaihtoehto ja kokonaan uuden budjetin saa lisättyä nollaamalla budjettinsa tai vaihtoehtoisesti voi lisätä tuloja.
![budjetti](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/photos/budjetinasetus.png)

## Tulon lisääminen
Käyttäjä voi lisätä tuloja kohdan Lisää tuloja alla olevan kentän avulla lisäämällä asettamalla tulon ja painamalla kentän alla olevaa lisää painiketta. Budjetin määrä nouseee annetulla tulon määrällä.
![tulot](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/photos/tulonlisays.png)

## Menojen lisääminen
Käyttäjä voi lisätä menon Lisää meno alla olevasta kategoriavalikosta. Kohdan Valitse kategoria alla lukevasta "muu"-kohdasta painamalla ilmestyy valikko, josta voi valita haluamansa kategorian. Määrä kohdan alla olevaan kenttään lisätään menon määrä ja painetaan sitten Lisää-painiketta. Tämän jälkeen sivun yläkulmassa oleva budjetin tasapaino ja käytetyn rahan määrä muuttuvat ja sivulle ilmestyy ympyrädiagrammi, joka näyttää menojen jakautumisen.
![menonlisays](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/photos/menonlisays.png)

## Menojen asettamisen jälkeen
Kun käyttäjä on lisännyt menon näytetään se ympyrädiagrammin muodossa. Yllämainittujen toimintojen lisäksi voidaan budjetti nollata painamalla "Nollaa"-painiketta ja kirjautua ulos "Kirjaudu ulos"-painikkeella
![ympyradiagrammi](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/photos/ympyradiagrammi.png)



