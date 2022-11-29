from tkinter import ttk, constants
from services.budget import budget_service


class FrontPage:
    def __init__(self, root, logout):
        self._root = root
        self._frame = None
        self._logout = logout
        self._user = budget_service.get_logged_user()
        self._front_page()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _front_page(self):
        self._frame = ttk.Frame(master=self._root)
        heading_label = ttk.Label(
            master=self._frame, text=f"Olet nyt kirjautunut sisään nimellä {self._user.username}!")
        heading_label.grid(row=0, column=0)

        logout_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu ulos",
            command=self._logout_handler
        )
        logout_button.grid()

    def _logout_handler(self):
        budget_service.logout()
        self._logout()
