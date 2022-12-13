class Transaction:
    """Luokka, joka kuvaa yksittäistä menoa.
    """

    def __init__(self, username, category, amount):
        """Luokan konstruktori, joka luo menon

        Args:
            username(str): käyttäjän käyttäjätunnus
            category(str): valittu kategoria
            amount(int): menon summa
        """
        self.username = username
        self.category = category
        self.amount = amount
