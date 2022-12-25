# Arkkitehtuuri

## Pakkauskaavio

![pakkauskaavio](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/photos/pakkauskaavio.png)

- ui sisältää käyttöliittymän koodin
- services sisältää sovelluslogiikan koodin:
  - sovelluslogiikasta vastaa `BudgetService`, joka tarjoaa seuraavat metodit käyttöliittymän toiminnoille:
    - `get_logged_user()`
    - `signup(username, password, login)`
    - `login(username, password)`
    - `logout()`
    - `add_budget(budget)`
    - `add_income(budget, income)`
    - `add_transaction(category, amount)`
    - `get_budget()`
    - `get_balance()`
    - `get_transactions_sum_by_category()`
    - `get_transactions_by_category()`
    - `clear_all()`
- repositories sisältää tietojen tallennuksesta ja käsittelystä vastaavan koodin
  - `UserRepository`:ssä käsitellään kaikki käyttäjiin liittyvät tietokantaoperaatiot ja `TransactionRepository`:ssä käsitellään käyttäjän menoihin liittyvät tietokantaoperaatiot. Sovelluslogiikka pääsee näiden repositorioiden kautta käsiksi tietokantoihin.
- entities sisältää luokat, jotka kuvastavat sovelluksen käyttämiä tietokohteita.
  - `User` kuvastaa yksittäistä käyttäjää ja `Transaction` kuvastaa yksittäistä menoa.

    ```mermaid
    classDiagram
    Transaction "*" --> "1" User
    Transaction: username
    Transaction: category
    Transaction: amount
    User: username
    User: password
    User: budget
    ```


## Käyttöliittymä
Käyttöliittymä koostuu kolmesta näkymästä.
- Uuden käyttäjän rekisteröintu, josta vastaa luokka SignupPage
- Kirjautuminen, josta vastaa luokka LoginPage
- Budjetointinäkymä, josta vastaa luokka FrontPage
Luokka UI vastaa näiden näkymien näyttämisestä. Kun budjetointinäkymän eli etusivun tilanne muuttuu esimerkiksi uuden budjetin lisättäessä kutsutaan sovelluksen metodia reload, joka päivittää näkymän.

## Toiminnallisuudet

### Käyttäjän kirjautuminen

```mermaid
sequenceDiagram
User ->> UI: "Kirjaudu"
UI ->> BudgetService: login("user","123")
BudgetService ->> UserRepository: find_by_username("user")
UserRepository -->> BudgetService: user
BudgetService -->> UI: user
UI ->> UI: show_front_page()
```

Käyttäjä täyttää käyttäjätunnuksen ja salasanan ja painaa "Kirjaudu"-painiketta. Käyttöliittymän tapahtumankäsittelijä kutsuu sovelluslogiikka `BudgetServicen` metodia `login` kirjautumistiedoilla. Sovelluslogiikka kutsuu `UserRepositoryn` metodia `find_by_username` annetulla käyttätunnuksella ja palauttaa User-oliona käyttäjätunnuksen jos sellainen löytyy. Sovelluslogiikan `login`-metodi selvittää vastaako käyttäjätunnus ja salasana, jos vastaa niin se kirjaa käyttäjän sisään ja palauttaa käyttäjän käyttöliittymälle. Käyttöliittymä vaihtaa näkymäksi sovelluksen etusivun.

### Käyttäjän luominen

```mermaid
sequenceDiagram
User ->> UI: "Luo"
UI ->> BudgetService: signup("user","123")
BudgetService ->> UserRepository: find_by_username("user")
UserRepository -->> BudgetService: None
BudgetService ->> user: User("user","123")
BudgetService ->> UserRepository: signup(user)
UserRepository -->> BudgetService: user
BudgetService -->> UI: user
UI ->> UI: show_front_page()
```

Käyttäjä täyttää käyttäjätunnuksen ja salasanan ja painaa "Luo"-painiketta. Käyttöliittymän tapahtumankäsittelijä kutsuu sovelluslogiikka `BudgetServicen` metodia `signup` annetuilla tiedoilla. Sovelluslogiikka kutsuu `UserRepositoryn` metodia `find_by_username` annetulla käyttätunnuksella ja palauttaa User-oliona käyttäjätunnuksen jos sellainen löytyy muuten None. Jos käyttäjätunnuksella ei löytynyt käyttäjää kutsuu sovelluslogiikka `UserRepositoryn` metodia signup, joka lisää käyttäjän tietokantaan ja palauttaa luodun käyttäjän. `BudgetService` palauttaa käyttäjän edelleen käyttöliittymälle. Käyttöliittymä vaihtaa näkymäksi sovelluksen etusivun.

### Budjetin asettaminen

```mermaid
sequenceDiagram
User ->> UI: "Lisää"
UI ->> BudgetService: add_budget(100)
BudgetService ->> UserRepository: add_budget(100, "user")
UserRepository -->> BudgetService: 100
BudgetService -->> UI: 100
UI ->> UI: reload()
```
Käyttäjä asettaa budjetin summan ja painaa "Lisää"-painiketta. Käyttöliittymän tapahtumakäsittelijä kutsuu `BudgetServicen` metodia `add_budget` annetulla budjetin summalla. Sovelluslogiikka tarkastaa onko budjetti kelvollinen ja kutsuu sitten budjetilla ja käyttäjätunnuksella `UserRepositoryn` metodia `add_budget`, joka lisää budjetin tietokantaan. `UserRepository` palauttaa lisätyn summan `BudgetServicelle`, joka palauttaa edelleen budjetin käyttöliittymälle. Käyttöliittymä päivittää käyttäjän budjetin `reload`:illa vastaamaan annettua budjettia.

### Menon lisääminen

```mermaid
sequenceDiagram
User ->> UI: "Lisää"
UI ->> BudgetService: add_transaction(category,amount)
BudgetService ->> transaction: Transaction("user","muu",50)
BudgetService ->> TransactionRepository: add_transaction(transaction)
TransactionRepository -->> BudgetService: 50
BudgetService -->> UI: 50
UI ->> UI: reload()
```

Käyttäjä lisää uuden menon valitsemalla kategorian listasta ja lisää menon summan painamalla "Lisää"-painiketta. Käyttöliittymän tapahtumakäsittelijä kutsuu juuri annetuilla tiedoilla `BudgetServicen` metodia `add_transaction`, joka tarkastaa syötteen kelvollisuuden ja  luo sitten käyttäjästä, kategoriasta ja summasta transaction-olion. Sovelluslogiikka kutsuu `TransactionRepositoryn` metodia `add_transaction` transaction-olio parametrinään. Metodi lisää menon tietokantaa ja palauttaa sovelluslogiikalle lisätyn menon summan. Sovelluslogiikka palauttaa summan edelleen käyttöliittymälle, joka päivittää `reload`:illa annetut tiedot etusivulle.

#### Muut toiminnallisuudet
Muut toiminnallisuudet noudattavat samoja periaatteita kun esitetyt toiminallisuudet. Käyttöliittymän tapahtumakäsittelijä kutsuu jotakin sovelluslogiikan metodai, joka päivittää jotakin toiminnallisuuden tilaa ja käyttöliittymään palatessa näkymä päivitetään vastaamaan nykytilaa.

## Tietojen pysyväistallennus
Hakemistossa <em>repositories</em> olevat luokat `UserRepository` ja `TransactionRepository` vastaavat tietojen tallettamisesta. Molemmat luokat tallentavat tiedot SQLite-tietokantaan. `UserRepository` tallentaa käyttäjästä `users`-tauluun käyttäjän käyttäjänimen, salasanan ja budjetin, joka asetetaan vasta kirjauduttua eli se on aluksi None. `TransactionRepository` tallentaa `Transactions`-tauluun käyttäjänimen, kategorian ja menon määrän. Taulut alustetaan `initialize_database.py`-tiedostossa.


### Heikkous
Ympyrädiagrammi toimii huonosti kun lisää muutaman pienen menon ja yhden niitä paljon suuremman menon.
![heikkous](https://github.com/eerolasi/ot-harjoitustyo/blob/master/budgetapp/dokumentaatio/photos/heikkous.png)
