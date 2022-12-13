class User:
    """Luokka, joka kuvaa yksittäistä käyttäjää
    """

    def __init__(self, username, password, budget=None):
        """Luokan konstruktori, joka luo käyttäjän

        Args:
            username (str): käyttäjän käyttäjätunnus
            password (str): käyttäjän salasana
            budget (str, optional): käyttäjän budjetti, joka None jos sitä ei aseteta
        """
        self.username = username
        self.password = password
        self.budget = budget
