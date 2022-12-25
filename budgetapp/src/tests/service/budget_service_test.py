import unittest
from repositories.user_repository import user_repository
from repositories.transaction_repository import transaction_repository
from entities.user import User
from entities.transaction import Transaction
from services.budget_service import (budget_service, InvalidInputError,
                                     InfiniteInputError, UserExitsError, LoginError)


class TestBudgetService(unittest.TestCase):
    def setUp(self):
        user_repository.clear_table()
        transaction_repository.clear_table()
        self.user = User("user", "123", 100)
        self.transaction = Transaction(self.user.username, "muu", 2)
        self.transaction2 = Transaction(self.user.username, "ruoka", 3)

    def login_user(self):
        budget_service.signup(self.user.username, self.user.password)

    def test_signup(self):
        signed = budget_service.signup(self.user.username, self.user.password)

        budget_service.login(signed.username, signed.password)
        with self.assertRaises(UserExitsError):
            budget_service.signup("user", "1223")

    def test_login_fail(self):
        with self.assertRaises(LoginError):
            budget_service.login(self.user.username, "124")

    def test_get_logged_user(self):
        budget_service.signup(self.user.username, self.user.password)
        logged = budget_service.get_logged_user()
        self.assertEqual(logged.username, self.user.username)

    def test_logout(self):
        login = budget_service.signup("user4", "1224")
        logout = budget_service.logout()
        self.assertNotEqual(login, logout)

    def test_add_budget(self):
        self.login_user()
        with self.assertRaises(InvalidInputError):
            budget_service.add_budget(-1)
        with self.assertRaises(InvalidInputError):
            budget_service.add_budget("hei")
        with self.assertRaises(InfiniteInputError):
            budget_service.add_budget(float('inf'))
        budget = budget_service.add_budget(100)
        self.assertEqual(100, budget)

    def test_add_income(self):
        self.login_user()
        budget_service.add_budget(self.user.budget)

        with self.assertRaises(InvalidInputError):
            budget_service.add_income(self.user.budget, "moi")
        with self.assertRaises(InfiniteInputError):
            budget_service.add_income(self.user.budget, float('inf'))
        budget = budget_service.add_income(self.user.budget, 2)
        self.assertEqual(budget, 102)

    def test_add_transaction(self):
        with self.assertRaises(InvalidInputError):
            budget_service.add_transaction("muu", -1)
        with self.assertRaises(InvalidInputError):
            budget_service.add_transaction("sijoitukset", "lol")
        with self.assertRaises(InfiniteInputError):
            budget_service.add_transaction("vapaa-aika", float('inf'))
        transaction = budget_service.add_transaction(
            self.transaction2.category, self.transaction2.amount)
        self.assertEqual(3, transaction)

    def test_get_budget(self):
        self.login_user()
        budget = budget_service.get_budget()
        self.assertEqual(budget, 0)
        budget_service.add_budget(int(self.user.budget))
        budget2 = budget_service.get_budget()
        self.assertEqual(budget2, 100)

    def test_get_transactions_sum(self):
        transactions = budget_service.get_transactions_sum()
        self.assertEqual(transactions, 0)
        budget_service.add_transaction(
            self.transaction.category, self.transaction2.amount)
        budget_service.add_transaction("muu", 5)
        sum = budget_service.get_transactions_sum()
        self.assertEqual(sum, 8)

    def test_get_transactions_by_category(self):
        budget_service.add_transaction(
            self.transaction.category, self.transaction.amount)
        category = budget_service.get_transactions_sum_by_category()
        self.assertEqual(
            category, {self.transaction.category: self.transaction.amount})

    def test_get_balance(self):
        self.login_user()
        balance = budget_service.get_balance()
        self.assertEqual(balance, 0)

        budget_service.add_transaction(
            self.transaction.category, self.transaction.amount)
        balance = budget_service.get_balance()
        self.assertEqual(balance, -2)

        budget_service.clear_all()
        budget_service.add_budget(self.user.budget)
        balance = budget_service.get_balance()
        self.assertEqual(balance, 100)

        budget_service.add_transaction(
            self.transaction.category, self.transaction.amount)
        budget_service.add_budget(self.user.budget)
        balance = budget_service.get_balance()
        self.assertEqual(balance, 98)

    def test_clear_all(self):
        clear = budget_service.clear_all()
        self.assertEqual(clear, self.user.username)
