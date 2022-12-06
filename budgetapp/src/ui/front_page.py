from tkinter import ttk, constants, StringVar, Listbox
from services.budget_service import budget_service
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure


class FrontPage:
    def __init__(self, root, logout, reload):
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
        self._budget = budget_service.get_budget(self._user.username)
        self._transactions_sum = budget_service.get_transactions_sum(
            self._user.username)
        self._balance = budget_service.get_balance(self._user.username)
        self._pie = budget_service.get_transactions(self._user.username)
        self._front_page()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _front_page(self):
        self._frame = ttk.Frame(master=self._root)

        heading_label = ttk.Label(
            master=self._frame, text=f"Olet nyt kirjautunut sisään nimellä {self._user.username}!")
        heading_label.grid(padx=5, pady=5)
        show_budget_label = ttk.Label(
            master=self._frame,
            text=f"Budjettisi on: {self._budget} euroa"
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

        if self._transactions_sum:
            labels = list(self._pie.keys())
            values = list(self._pie.values())
            fig = Figure()
            ax = fig.add_subplot(111)
            fig.set_size_inches(5, 5)

            fig.set_facecolor('#DCDCDC')
            ax.pie(values, labels=labels, autopct='%0.1f%%')

            chart = FigureCanvasTkAgg(fig, master=self._frame)

            chart.get_tk_widget().grid()

        if not self._budget:
            budget_label = ttk.Label(
                master=self._frame, text="Anna budjettisi:"
            )
            self._budget_entry = ttk.Entry(master=self._frame)
            budget_label.grid(padx=5, pady=5)
            self._budget_entry.grid(padx=5, pady=5)

            budget_button = ttk.Button(
                master=self._frame,
                text="Lisää",
                command=self._add_budget)
            budget_button.grid(padx=5, pady=5)

        transaction_label = ttk.Label(master=self._frame, text="Lisää meno")
        transaction_label.grid(padx=5, pady=5)
        category_label = ttk.Label(
            master=self._frame, text="Valitse kategoria: ")
        category_label.grid()
        self._category_value = StringVar(master=self._frame)
        self._categories_entry = ttk.OptionMenu(
            self._frame, self._category_value, *self._categories)
        self._categories_entry.grid()

        amount_label = ttk.Label(
            master=self._frame,
            text="Summa"
        )
        amount_label.grid(padx=5, pady=5)
        self._amount_entry = ttk.Entry(master=self._frame)
        self._amount_entry.grid(padx=5, pady=5)

        transaction_button = ttk.Button(
            master=self._frame,
            text="Lisää",
            command=self._add_transaction)
        transaction_button.grid(padx=5, pady=5)

        reset_label = ttk.Button(
            master=self._frame,
            text="Nollaa",
            command=self._reset_handler)
        reset_label.grid()

        logout_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu ulos",
            command=self._logout_handler
        )
        logout_button.grid(padx=5, pady=5)
        self._frame.grid_columnconfigure(0, weight=3, minsize=600)

    def _reset_handler(self):
        budget_service.clear_all(self._user.username)
        self._reload()

    def _logout_handler(self):
        budget_service.logout()
        self._logout()

    def _add_budget(self):
        budget = self._budget_entry.get()
        budget = int(budget)

        budget_service.add_budget(budget, self._user.username)
        self._reload()

    def _add_transaction(self):
        category = self._category_value.get()
        amount = self._amount_entry.get()
        budget_service.add_transaction(self._user.username, category, amount)
        self._reload()
