from entities.user import User
from repositories.user_repository import user_repository as default_user_repository


class UserExitsError(Exception):
    pass


class LoginError(Exception):
    pass


class BudgetService:
    def __init__(self, user_repository=default_user_repository):
        self._user = None
        self._user_repository = user_repository

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


budget_service = BudgetService()
