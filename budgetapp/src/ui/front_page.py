from tkinter import ttk, constants, StringVar, Listbox
from services.budget_service import budget_service, InfiniteInputError, InvalidInputError
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure


class FrontPage:
    """Sovelluksen etusivusta eli budjetoinnista vastaava näkymä.
    """

    def __init__(self, root, logout, reload):
        """Luokan konstruktori, joka luo budjetointinäkymän.

        Args:
            root: Tkinter-ikkuna, johon näkymä alustetaan
            logout: uloskirjautuminen
            reload: näkymän päivitys
        """
        self._root = root
        self._frame = None
        self._logout = logout
        self._budget_entry = None
        self._amount_entry = None
        self._reload = reload
        self._categories = ["muu", "ruoka", "asuminen",
                            "harrastukset", "vapaa-aika", "viihde", "sijoitukset"]
        self._categories_entry = None
        self._user = budget_service.get_logged_user()
        self._budget = budget_service.get_budget()
        self._transactions_sum = budget_service.get_transactions_sum()
        self._balance = budget_service.get_balance()
        self._transactions = budget_service.get_transactions_sum_by_category()
        self._error_variable = None
        self._error_label = None
        self._front_page()

    def pack(self):
        """Näyttää näkymän.
        """
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Tuhoaa näkymän.
        """
        self._frame.destroy()

    def _front_page(self):
        self._frame = ttk.Frame(master=self._root)
        self._error_variable = StringVar(self._frame)
        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )

        heading_label = ttk.Label(
            master=self._frame, text=f"Olet kirjautunut sisään nimellä {self._user.username}!")
        heading_label.grid()
        show_budget_label = ttk.Label(
            master=self._frame,
            text=f"Budjettisi on {self._budget} euroa"
        )
        show_budget_label.grid(padx=5, pady=5)

        balance_label = ttk.Label(
            master=self._frame,
            text=f"Budjettisi tasapaino on {self._balance} euroa"
        )
        balance_label.grid(padx=5, pady=5)

        transactions_sum_label = ttk.Label(
            master=self._frame,
            text=f"Olet käyttänyt {self._transactions_sum} euroa"
        )
        transactions_sum_label.grid(padx=5, pady=5)

        if not self._budget:
            budget_label = ttk.Label(
                master=self._frame, text="Anna budjettisi:"
            )
            self._budget_entry = ttk.Entry(master=self._frame)
            budget_label.grid(padx=5, pady=5)
            self._budget_entry.grid()

            budget_button = ttk.Button(
                master=self._frame,
                text="Lisää",
                command=self._add_budget_handler)
            budget_button.grid(padx=5, pady=5)

        income_label = ttk.Label(master=self._frame, text="Lisää tuloja:")
        income_label.grid()

        self._income_entry = ttk.Entry(master=self._frame)
        self._income_entry.grid(padx=5, pady=5)
        income_button = ttk.Button(
            master=self._frame,
            text="Lisää",
            command=self._add_income_handler
        )

        income_button.grid()

        transaction_label = ttk.Label(master=self._frame, text="Lisää meno")
        transaction_label.grid(padx=5, pady=5)
        category_label = ttk.Label(
            master=self._frame, text="Valitse kategoria: ")
        category_label.grid(padx=5, pady=5)
        self._category_value = StringVar(master=self._frame)
        self._categories_entry = ttk.OptionMenu(
            self._frame, self._category_value, *self._categories)
        self._categories_entry.grid(padx=5, pady=5)

        amount_label = ttk.Label(
            master=self._frame,
            text="Määrä:"
        )
        amount_label.grid()
        self._amount_entry = ttk.Entry(master=self._frame)
        self._amount_entry.grid(padx=5, pady=5)

        transaction_button = ttk.Button(
            master=self._frame,
            text="Lisää",
            command=self._add_transaction_handler)
        self._error_label.grid(padx=5, pady=5)

        transaction_button.grid(padx=5, pady=5)

        reset_label = ttk.Button(
            master=self._frame,
            text="Nollaa",
            command=self._reset_handler)
        reset_label.grid(padx=5, pady=5)

        logout_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu ulos",
            command=self._logout_handler
        )
        logout_button.grid(padx=5, pady=5)

        if self._transactions_sum:
            labels = list(self._transactions.keys())
            values = list(self._transactions.values())
            fig = Figure()
            ax = fig.add_subplot(111)
            fig.set_size_inches(5, 4)
            fig.set_facecolor('#d9d9d9')
            ax.pie(values, labels=labels, autopct='%0.1f%%')
            chart = FigureCanvasTkAgg(fig, master=self._frame)
            chart.get_tk_widget().grid(row=0, column=1, rowspan=20)

        self._frame.grid_columnconfigure(0, weight=1, minsize=500)
        self._hide_error()

    def _reset_handler(self):
        budget_service.clear_all()
        self._reload()

    def _logout_handler(self):
        budget_service.logout()
        self._logout()

    def _add_budget_handler(self):
        budget = self._budget_entry.get()

        try:
            budget_service.add_budget(budget)
            self._reload()

        except InvalidInputError:
            self._show_error("Anna positiivinen arvo")
        except InfiniteInputError:
            self._show_error("Liian suuri arvo")

    def _add_transaction_handler(self):
        category = self._category_value.get()
        amount = self._amount_entry.get()
        try:
            budget_service.add_transaction(category, amount)
            self._reload()

        except InvalidInputError:
            self._show_error("Anna positiivinen arvo")
        except InfiniteInputError:
            self._show_error("Liian suuri arvo")

    def _add_income_handler(self):
        income = self._income_entry.get()
        try:
            budget_service.add_income(self._budget, income)
            self._reload()
        except InvalidInputError:
            self._show_error("Anna positiivinen arvo")
        except InfiniteInputError:
            self._show_error("Liian suuri arvo")

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()
