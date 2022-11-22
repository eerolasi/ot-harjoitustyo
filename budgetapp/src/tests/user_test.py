import unittest
from repositories.user_repository import user_repository
from entities.user import User

class TestUser(unittest.TestCase):
    def setUp(self):
        user_repository.clear_table()
        self.user = User("user","123")
        self.user2 = User("user2","1234")

    def test_signup(self):
        user = user_repository.signup(self.user)
        found_user = user_repository.find_by_username(user.username)
        self.assertEqual(found_user.username, user.username)

    def test_find_by_username(self):
        user = user_repository.signup(self.user)
        found_user = user_repository.find_by_username(user.username)
        self.assertEqual(found_user.username, user.username)

    def test_find_all_users(self):
        user1 = user_repository.signup(self.user)
        user2 =user_repository.signup(self.user2)
        users = user_repository.find_all_users()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].username, user1.username)
        self.assertEqual(users[1].username, user2.username)

