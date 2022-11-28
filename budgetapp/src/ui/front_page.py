from tkinter import ttk, constants
from services.budget import budget_service


class FrontPage:
    def __init__(self, root):
        self._root = root
        self._frame = None
        self._front_page()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _front_page(self):
        self._frame = ttk.Frame(master=self._root)
        heading_label = ttk.Label(
            master=self._frame, text=f"Olet nyt kirjautunut sisään!")
        heading_label.grid(columnspan=3)
