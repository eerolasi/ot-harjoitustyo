from entities.user import User
from entities.transaction import Transaction
from repositories.user_repository import user_repository as default_user_repository
from repositories.transaction_repository import (
    transaction_repository as default_transaction_repositiory)


class UserExitsError(Exception):
    pass


class LoginError(Exception):
    pass


class InvalidInputError(Exception):
    pass


class BudgetService:
    """Luokka, joka vastaa sovelluslogiikasta
    """
    def __init__(self, user_repository=default_user_repository,
                 transaction_repository=default_transaction_repositiory):
        """Luokan konstruktori, joka luo uuden palvelun

        Args:
            user_repository (object, optional): user_repositoryn-olio
            transaction_repository (object, optional): transaction_repositoryn-olio
        """
        self._user = None
        self._user_repository = user_repository
        self._transaction_repository = transaction_repository

    def get_logged_user(self):
        """Palauttaa kirjautuneen käyttäjän

        Returns:
            Palauttaa kirjautuneen käyttäjän oliona
        """
        return self._user

    def signup(self, username, password, login=True):
        """Rekisteröi uuden käyttäjän ja kirjaa sen sisään

        Args:
            username (str): käyttäjän käyttäjätunnus
            password (str): käyttäjän salasana
            login (bool, optional): käyttäjän kirjautumisen tila

        Raises:
            UserExitsError: TUottaa poikkeksen jos annettu käyttäjätunnus on varattu

        Returns:
            Palauttaa luodun käyttäjän oliona
        """
        user_exist = self._user_repository.find_by_username(username)
        if user_exist:
            raise UserExitsError("Käyttäjätunnus on varattu")
        user = self._user_repository.signup(User(username, password))
        if login:
            self._user = user
        return user

    def login(self, username, password):
        """Kirjaa käyttäjän sisään

        Args:
            username (str): käyttäjän käyttäjätunnus
            password (str): käyttäjän salasana

        Raises:
            LoginError: Tuottaa poikkeuksen jos käyttäjätunnusta ei ole tai
            salasana ei täsmää

        Returns:
            Palauttaa käyttäjän oliona
        """
        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise LoginError("Kirjautuminen epäonnistui")
        self._user = user
        return user

    def logout(self):
        """Kirjaa käyttäjän ulos
        """
        self._user = None

    def add_budget(self, budget, username):
        """Lisää käyttäjälle budjetin

        Args:
            budget (int): käyttäjän antama budjetti
            username (str): käyttäjän käyttäjätunnus

        Raises:
            InvalidInputError: Tuottaa poikkeuksen jos käyttäjä yrittää asettaa
            negatiivisen budjetin

        Returns:
            Palauttaa päivitetyn budjetin
        """
        if budget < 0:
            raise InvalidInputError("Budjetti ei voi olla negatiivinen")
        return self._user_repository.add_budget(budget, username)

    def add_transaction(self, username, category, amount):
        """Lisää käyttäjälle uuden menon

        Args:
            username (str): käyttäjän käyttäjätunnus
            category (str): käyttäjän valitsema kategoria
            amount (int): käyttäjän antama menon summa

        Raises:
            InvalidInputError: Tuottaa poikkeuksen jos käyttäjä yrittää

        Returns:
            Palauttaa annetun menon summan
        """
        transaction = Transaction(username, category,int(amount))
        if transaction.amount < 0:
            raise InvalidInputError("Menon summa ei voi olla negatiivinen")
        return self._transaction_repository.add_transaction(transaction)

    def get_budget(self, username):
        """Palauttaa käyttäjän budjetin

        Args:
            username (str): käyttäjän käyttäjätunnus

        Returns:
            Palauttaa annetun käyttäjän budjetin
        """
        budget = self._user_repository.get_budget(username)
        if not budget:
            return 0
        return budget

    def get_transactions_sum(self, username):
        """Palauttaa käyttäjän menojen yhteissumman

        Args:
            username (str): käyttäjän käyttäjätunnus

        Returns:
            Paluttaa käyttäjän menojen yhteissumman
        """
        transactions = self._transaction_repository.get_transactions(username)
        if not transactions:
            return 0
        return transactions

    def get_balance(self, username):
        """Palauttaa käyttäjän budjetin tasapainon

        Args:
            username(str): käyttäjän käyttätunnus

        Returns:
            Jos käyttäjällä ei ole budjettia eikä menoja palauttaa 0
            JOs käyttäjällä on budjetti muttei menoja palauttaa 0
            Jos käyttäjällä on menoja, muttei budjettia palauttaa menot negatiivisena
            Jos käyttäjällä on budjetti ja menoja palauttaa niiden erotuksen
        """
        budget = self._user_repository.get_budget(username)
        transactions = self._transaction_repository.get_transactions(username)
        if not budget and not transactions:
            return 0
        if budget and not transactions:
            return budget
        if transactions and not budget:
            return -transactions
        return budget-transactions

    def get_transactions(self, user):
        """Palauttaa kaikki menot kategorioittain

        Args:
            username (str): käyttäjän käyttäjätunnus

        Returns:
            palauttaa sanakirjana käyttäjän menot ja niiden kategoriat
        """
        amounts = self._transaction_repository.get_transactions_by_category(
            user)
        return amounts


    def clear_all(self, username):
        """Asettaa käyttäjän budjetin 0 ja poistaa kaikki menot

        Args:
            username(str): käyttäjän käyttäjätunnus

        Returns:
            Palauttaa käyttäjän käyttäjätunnuksen
        """
        self._user_repository.add_budget(0, username)
        self._transaction_repository.clear_transactions(username)
        return username


budget_service = BudgetService()
