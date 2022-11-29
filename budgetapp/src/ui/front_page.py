from tkinter import ttk, constants
from services.budget_service import budget_service


class FrontPage:
    def __init__(self, root, logout, reload):
        self._root = root
        self._frame = None
        self._logout = logout
        self._budget_entry = None
        self._amount_entry = None
        self._reload = reload
        self._user = budget_service.get_logged_user()
        self._budget = budget_service.get_budget(self._user.username)
        self._transactions_sum = budget_service.get_transactions_sum(
            self._user.username)
        self._balance = budget_service.get_balance(self._user.username)

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
        amount_label = ttk.Label(
            master=self._frame,
            text="Summa"
        )
        self._amount_entry = ttk.Entry(master=self._frame)
        amount_label.grid(padx=5, pady=5)
        self._amount_entry.grid(padx=5, pady=5)

        transaction_button = ttk.Button(
            master=self._frame,
            text="Lisää",
            command=self._add_transaction)
        transaction_button.grid(padx=5, pady=5)

        logout_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu ulos",
            command=self._logout_handler
        )
        logout_button.grid(padx=5, pady=5)

    def _logout_handler(self):
        budget_service.logout()
        self._logout()

    def _add_budget(self):
        budget = self._budget_entry.get()
        budget = int(budget)

        budget_service.add_budget(budget, self._user.username)
        self._reload()

    def _add_transaction(self):
        amount = self._amount_entry.get()

        budget_service.add_transaction(self._user.username, amount)
        self._reload()
