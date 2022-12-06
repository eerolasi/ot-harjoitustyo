from database_connection import get_database_connection


def drop_tables(connection):
    '''Entisten taulujen poisto'''
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users")
    cursor.execute("DROP TABLE IF EXISTS Transactions")
    connection.commit()


def create_tables(connection):
    '''Luodaan uusi taulu tietokantaan'''
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE Users (
            username TEXT PRIMARY KEY,
            password TEXT,
            budget INTEGER)
    ''')
    cursor.execute('''
        CREATE TABLE Transactions (
            username TEXT,
            category TEXT,
            amount INTEGER)
            ''')
    connection.commit()


def initialize_database():
    '''Alustetaan tietokantataulu'''
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()
