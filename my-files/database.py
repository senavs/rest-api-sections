import sqlite3


class Database:

    def __init__(self, database: str):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username text, password text)")
            self.cursor.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name text, price real)")
        except sqlite3.OperationalError:
            pass
        else:
            self.cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (0, 'root', 'toor'))
            self.connection.commit()
        finally:
            self.connection.close()


if __name__ == '__main__':
    Database('data.db')
