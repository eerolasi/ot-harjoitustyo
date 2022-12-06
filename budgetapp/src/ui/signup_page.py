from tkinter import ttk, constants, StringVar
from services.budget_service import budget_service, UserExitsError


class SignupPage:
    def __init__(self, root, signup, show_login_page):
        self._root = root
        self._frame = None
        self._signup = signup
        self._show_login_page = show_login_page
        self._username_entry = None
        self._password_entry = None
        self._error_label = None
        self._error_variable = None

        self._signup_page()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _signup_page(self):
        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)
        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable
        )
        self._error_label.grid(padx=5, pady=5)

        heading_label = ttk.Label(
            master=self._frame, text="Käyttäjätunnuksen luonti")
        heading_label.grid(padx=5, pady=5)

        username_label = ttk.Label(master=self._frame, text="Käyttäjätunnus: ")
        self._username_entry = ttk.Entry(master=self._frame)
        username_label.grid(padx=5, pady=5)
        self._username_entry.grid(padx=5, pady=5)

        password_label = ttk.Label(master=self._frame, text="Salasana: ")
        self._password_entry = ttk.Entry(master=self._frame)
        password_label.grid(padx=5, pady=5)
        self._password_entry.grid(padx=5, pady=5)

        signup_button = ttk.Button(
            master=self._frame,
            text="Luo",
            command=self._signup_handler
        )
        signup_button.grid(padx=5, pady=5)

        login_button = ttk.Button(
            master=self._frame,
            text="Siirry kirjautumissivulle",
            command=self._show_login_page
        )
        login_button.grid(padx=5, pady=5)

        self._frame.grid_columnconfigure(0, weight=3, minsize=600)
        self._hide_error()

    def _signup_handler(self):
        username = self._username_entry.get()
        password = self._password_entry.get()

        if len(username) == 0:
            self._show_error("Käyttäjätunnus puuttuu")
            return
        if len(password) == 0:
            self._show_error("Salasana puuttuu")
            return

        try:
            budget_service.signup(username, password)
            self._signup()
            print("Käyttäjätunnuksen luonti onnistui")
        except UserExitsError:
            self._show_error("Käyttäjätunnus on varattu")

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()
