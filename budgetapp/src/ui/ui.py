from ui.signup_page import SignupPage
from ui.login_page import LoginPage
from ui.front_page import FrontPage


class UI:
    """Luokka, joka vastaa sovelluksen käyttöliittymästä.
    """

    def __init__(self, root):
        """Luokan konstruktori, joka luo käyttöliittymästä vastaavan luokan.

        Args:
            root: TKinter-ikkuna, johon käyttöliittymä alustettaan
        """

        self._root = root
        self._current_view = None

    def start(self):
        """Käynnistää käyttöliittymän.
        """
        self._show_login_page()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()
        self._current_view = None

    def _show_signup_page(self):
        self._hide_current_view()

        self._current_view = SignupPage(
            self._root,
            self._show_front_page,
            self._show_login_page
        )
        self._current_view.pack()

    def _show_login_page(self):
        self._hide_current_view()

        self._current_view = LoginPage(
            self._root,
            self._show_front_page,
            self._show_signup_page
        )
        self._current_view.pack()

    def _show_front_page(self):
        self._hide_current_view()

        self._current_view = FrontPage(
            self._root,
            self._show_login_page,
            self._handle_update
        )
        self._current_view.pack()

    def _handle_update(self):
        self._show_front_page()
