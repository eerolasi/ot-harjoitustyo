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
    def __init__(self, user_repository=default_user_repository,
                 transaction_repository=default_transaction_repositiory):
        self._user = None
        self._user_repository = user_repository
        self._transaction_repository = transaction_repository

    def get_logged_user(self):
        return self._user

    def signup(self, username, password, login=True):
        user_exist = self._user_repository.find_by_username(username)
        if user_exist:
            raise UserExitsError("Käyttäjätunnus on varattu")
        user = self._user_repository.signup(User(username, password))
        if login:
            self._user = user
        return user

    def login(self, username, password):
        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise LoginError("Kirjautuminen epäonnistui")
        self._user = user
        return user

    def logout(self):
        self._user = None

    def add_budget(self, budget, user):
        if budget < 0:
            raise InvalidInputError("Budjetti ei voi olla negatiivinen")
        return self._user_repository.add_budget(budget, user)

    def add_transaction(self, user, category, amount):
        transaction = Transaction(user, category, int(amount))
        if transaction.amount < 0:
            raise InvalidInputError("Menon summa ei voi olla negatiivinen")
        return self._transaction_repository.add_transaction(transaction)

    def get_budget(self, user):
        budget = self._user_repository.get_budget(user)
        if not budget:
            return 0
        return budget

    def get_transactions_sum(self, user):
        transactions = self._transaction_repository.get_transactions(user)
        if not transactions:
            return 0
        return transactions

    def get_balance(self, user):
        budget = self._user_repository.get_budget(user)
        transactions = self._transaction_repository.get_transactions(user)
        if not budget and not transactions:
            return 0
        if budget and not transactions:
            return budget
        if transactions and not budget:
            return -transactions
        return budget-transactions

    def get_transactions(self, user):
        amounts = self._transaction_repository.get_transactions_by_category(
            user)
        return amounts

    def clear_all(self, user):
        self._user_repository.add_budget(0, user)
        self._transaction_repository.clear_transactions(user)
        return user


budget_service = BudgetService()
