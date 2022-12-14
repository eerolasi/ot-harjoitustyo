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


class InfiniteInputError(Exception):
    pass


class BudgetService:
    """Luokka, joka vastaa sovelluslogiikasta.
    """

    def __init__(self, user_repository=default_user_repository,
                 transaction_repository=default_transaction_repositiory):
        """Luokan konstruktori, joka luo uuden palvelun.
        Args:
            user_repository (object, optional): UserReposiotryn-olio, jolla on
            UserRepositorio luokan metodit
            transaction_repository (object, optional): TransactionRepositoryn-olio,
            jolla on TransactionRepository luokan metodit
        """
        self._user = None
        self._user_repository = user_repository
        self._transaction_repository = transaction_repository

    def get_logged_user(self):
        """Palauttaa kirjautuneen käyttäjän.
        Returns:
            Kirjautunut käytättäjä User-oliona
        """
        return self._user

    def signup(self, username, password, login=True):
        """Rekisteröi uuden käyttäjän ja kirjaa sen sisään.
        Args:
            username (str): käyttäjän käyttäjätunnus
            password (str): käyttäjän salasana
            login (bool, optional): käyttäjän kirjautumisen tila
        Raises:
            UserExitsError: Tuottaa poikkeuksen jos annettu käyttäjätunnus on varattu
        Returns:
            Luotu käyttäjä oliona
        """
        user_exist = self._user_repository.find_by_username(username)
        if user_exist:
            raise UserExitsError("Käyttäjätunnus on varattu")
        user = self._user_repository.signup(User(username, password))
        if login:
            self._user = user
        return user

    def login(self, username, password):
        """Kirjaa käyttäjän sisään.
        Args:
            username (str): käyttäjän käyttäjätunnus
            password (str): käyttäjän salasana
        Raises:
            LoginError: Tuottaa poikkeuksen jos käyttäjätunnusta ei ole tietokannassa tai
            salasana ei täsmää
        Returns:
            Kirjautunut kyttäjän oliona
        """
        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise LoginError()
        self._user = user
        return user

    def logout(self):
        """Kirjaa käyttäjän ulos.
        """
        self._user = None

    def add_budget(self, budget):
        """Lisää käyttäjälle budjetin.

        Args:
            budget (str): käyttäjän antama budjetti

        Raises:
            InvalidInputError: Tuottaa poikkeuksen jos syöte on nolla tai alle
            InfiniteInputError: Tuottaa poikkeuksen jos syöte on liian suuri

        Returns:
            Päivitetyn budjetin
        """

        try:
            budget = float(budget)
        except ValueError:
            budget = 0
        if budget <= 0:
            raise InvalidInputError()

        if budget == float('inf'):
            raise InfiniteInputError()

        return self._user_repository.add_budget(budget, self._user.username)

    def add_income(self, budget, income):
        """Lisää uuden tulon.
        Args:
            budget (int): käyttämän tämän hetkinen budjetti
            income (str): käyttäjän antama tulo merkkijonona
        Raises:
            InvalidInputError: Tuottaa poikkeuksen jos syöte on nolla tai alle
            InfiniteInputError: Tuottaa poikkeuksen jos syöte on liian suuri
        Returns:
            Päivitetyn budjetin
        """
        try:
            income = float(income)
        except ValueError:
            income = 0
        new_budget = income + budget
        if income <= 0:
            raise InvalidInputError()

        if income == float('inf'):
            raise InfiniteInputError()
        return self._user_repository.add_budget(new_budget, self._user.username)

    def add_transaction(self, category, amount):
        """Lisää käyttäjälle uuden menon.
        Args:
            category (str): käyttäjän valitsema kategoria
            amount (str): käyttäjän antama meno merkkijonona
        Raises:
            InvalidInputError: Tuottaa poikkeuksen jos syöte on nolla tai alle
            InfiniteInputError: Tuottaa poikkeuksen jos syöte on liian suuri
        Returns:
            Annetun menon arvon
        """

        try:
            amount = float(amount)
        except ValueError:
            amount = 0
        if amount <= 0:
            raise InvalidInputError()
        if amount == float('inf'):
            raise InfiniteInputError()
        transaction = Transaction(self._user.username, category, amount)
        return self._transaction_repository.add_transaction(transaction)

    def get_budget(self):
        """Palauttaa käyttäjän budjetin.
        Returns:
           Annetun käyttäjän budjetin
        """
        budget = self._user_repository.get_budget(self._user.username)
        if not budget:
            return 0
        return budget

    def get_transactions_sum(self):
        """Palauttaa käyttäjän menojen yhteissumman.
        Returns:
            Käyttäjän menojen yhteissumman
        """
        transactions = self._transaction_repository.get_transactions(
            self._user.username)
        if not transactions:
            return 0
        return round(transactions, 2)

    def get_balance(self):
        """Palauttaa käyttäjän budjetin tasapainon.
        Returns:
            Jos käyttäjällä ei ole budjettia eikä menoja palauttaa 0
            JOs käyttäjällä on budjetti muttei menoja palauttaa 0
            Jos käyttäjällä on menoja, muttei budjettia palauttaa menot negatiivisena
            Jos käyttäjällä on budjetti ja menoja palauttaa niiden erotuksen
        """
        budget = self._user_repository.get_budget(self._user.username)
        transactions = self._transaction_repository.get_transactions(
            self._user.username)
        if not budget and not transactions:
            return 0
        if budget and not transactions:
            return budget
        if transactions and not budget:
            return -transactions
        return round(budget-transactions, 2)

    def get_transactions_sum_by_category(self):
        """Palauttaa kaikki menot kategorioittain.
        Returns:
            Sanakirjana käyttäjän menot ja niiden kategoriat
        """
        amounts = self._transaction_repository.get_transactions_sum_by_category(
            self._user.username)
        return amounts

    def clear_all(self):
        """Asettaa käyttäjän budjetin nollaksi ja poistaa kaikki menot.
        Returns:
            Käyttäjän käyttäjätunnuksen
        """
        self._user_repository.add_budget(0, self._user.username)
        self._transaction_repository.clear_transactions(self._user.username)
        return self._user.username


budget_service = BudgetService()
