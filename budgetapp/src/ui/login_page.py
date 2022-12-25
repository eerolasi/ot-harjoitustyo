from tkinter import ttk, constants, StringVar
from services.budget_service import budget_service, LoginError


class LoginPage:
    """Sisäänkirjautumisesta vastaava näkymä.
    """

    def __init__(self, root, login, show_signup_page):
        """Luokan konstruktori, joka luo sisäänkirjautumisesta vastaavan luokn.

        Args:
            root: Tkinter-ikkuna, johon näkymä alustetaan
            login: käyttäjän sisäänkirjautuminen
            show_signup_page: rekisteröitymisnäkymä
        """
        self._root = root
        self._frame = None
        self._login = login
        self._show_signup_page = show_signup_page
        self._username_entry = None
        self._password_entry = None
        self._error_variable = None
        self._error_label = None

        self._login_page()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _login_page(self):
        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)
        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )
        self._error_label.grid(padx=5, pady=5)
        heading_label = ttk.Label(
            master=self._frame, text="Sisäänkirjautuminen")
        heading_label.grid(padx=5, pady=5)

        username_label = ttk.Label(master=self._frame, text="Käyttäjätunnus: ")
        self._username_entry = ttk.Entry(master=self._frame)
        username_label.grid(padx=5, pady=5)
        self._username_entry.grid(padx=5, pady=5)

        password_label = ttk.Label(master=self._frame, text="Salasana: ")
        self._password_entry = ttk.Entry(master=self._frame)
        password_label.grid(padx=5, pady=5)
        self._password_entry.grid(padx=5, pady=5)

        login_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu",
            command=self._login_handler
        )

        signup_button = ttk.Button(
            master=self._frame,
            text="Siirry luomaan käyttäjätunnus",
            command=self._show_signup_page
        )
        login_button.grid(padx=5, pady=5)
        signup_button.grid(padx=5, pady=5)

        self._frame.grid_columnconfigure(0, weight=3, minsize=600)

        self._hide_error()

    def _login_handler(self):
        username = self._username_entry.get()
        password = self._password_entry.get()

        try:
            budget_service.login(username, password)
            self._login()
        except LoginError:
            self._show_error("Kirjautuminen epäonnistui")

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()
