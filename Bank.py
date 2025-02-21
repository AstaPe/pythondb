import sqlite3


# Tėvinė klasė, kurią paveldi Owner ir BankAccount
class Entity:
    """Bendras duomenų bazės objektas su id"""

    def __init__(self, id=None):
        """Inicializuoja id"""
        self.id = id

    def save(self):
        """Bendras metodas įrašyti į duomenų bazę (tiks individualiai klasėms)"""
        raise NotImplementedError("Šis metodas turi būti įgyvendintas paveldinčioje klasėje")


# Savininko klasė, paveldinti iš Entity
class Owner(Entity):
    """Savininkas - paveldi iš Entity klasės"""

    def __init__(self, name, address, phone, id=None):
        super().__init__(id)
        self.name = name
        self.address = address
        self.phone = phone

    def save(self, db):
        """Įrašo savininką į duomenų bazę"""
        if self.id is None:
            db.cursor.execute('''INSERT INTO owners (name, address, phone) 
                                VALUES (?, ?, ?)''', (self.name, self.address, self.phone))
            db.conn.commit()
            self.id = db.cursor.lastrowid
        else:
            db.cursor.execute('''UPDATE owners SET name = ?, address = ?, phone = ? WHERE id = ?''',
                              (self.name, self.address, self.phone, self.id))
            db.conn.commit()

    def __str__(self):
        return f"Owner {self.name} at {self.address} ({self.phone})"


# Banko sąskaitos klasė, paveldinti iš Entity
class BankAccount(Entity):
    """Banko sąskaita - paveldi iš Entity klasės"""

    def __init__(self, owner, balance=0.0, id=None):
        super().__init__(id)
        self.owner = owner  # `owner` bus Owner objektas
        self.balance = balance

    def deposit(self, amount, db):
        """Deposituoti pinigus į sąskaitą"""
        if amount > 0:
            self.balance += amount
            self.save(db)  # Išsaugoti pakeitimus į duomenų bazę
            return f"Deposited {amount}. New balance: {self.balance}"
        return "Invalid deposit amount"

    def withdraw(self, amount, db):
        """Išimti pinigus iš sąskaitos"""
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.save(db)  # Išsaugoti pakeitimus į duomenų bazę
            return f"Withdrew {amount}. New balance: {self.balance}"
        return "Invalid withdraw amount or insufficient funds"

    def save(self, db):
        """Įrašo banko sąskaitą į duomenų bazę"""
        if self.id is None:
            db.cursor.execute('''INSERT INTO bank_accounts (owner_id, balance) 
                                VALUES (?, ?)''', (self.owner.id, self.balance))
            db.conn.commit()
            self.id = db.cursor.lastrowid
        else:
            db.cursor.execute('''UPDATE bank_accounts SET owner_id = ?, balance = ? WHERE id = ?''',
                               (self.owner.id, self.balance, self.id))
            db.conn.commit()

    def __str__(self):
        return f"Account of {self.owner.name} with balance {self.balance}"
class BankAccount(Entity):
    """Banko sąskaita - paveldi iš Entity klasės"""

    def __init__(self, owner, balance=0.0, id=None):
        super().__init__(id)  # Super klasės konstruktoriumi perduodame id
        self.owner = owner
        self.balance = balance

    def deposit(self, amount, db):
        """Deposituoti pinigus į sąskaitą"""
        if amount > 0:
            self.balance += amount
            self.save(db)  # Išsaugoti pakeitimus į duomenų bazę
            return f"Deposited {amount}. New balance: {self.balance}"
        return "Invalid deposit amount"

    def withdraw(self, amount, db):
        """Išimti pinigus iš sąskaitos"""
        if amount <= 0:
            return "Invalid withdraw amount"
        if amount > self.balance:
            return "Invalid withdraw amount or insufficient funds"
        self.balance -= amount
        self.save(db)  # Išsaugoti pakeitimus į duomenų bazę
        return f"Withdrew {amount}. New balance: {self.balance}"

    def save(self, db):
        """Įrašo banko sąskaitą į duomenų bazę"""
        if self.id is None:
            db.cursor.execute('''INSERT INTO bank_accounts (owner_id, balance) 
                                VALUES (?, ?)''', (self.owner.id, self.balance))
            db.conn.commit()
            self.id = db.cursor.lastrowid
        else:
            db.cursor.execute('''UPDATE bank_accounts SET owner_id = ?, balance = ? WHERE id = ?''',
                               (self.owner.id, self.balance, self.id))
            db.conn.commit()

    def __str__(self):
        return f"Account of {self.owner.name} with balance {self.balance}"

# Duomenų bazės klasė, kuri valdo ryšį su SQLite
class Database:
    """
    Database connection and setup
    """

    def __init__(self, db_name="bank_system.db"):
        """Initializes the database connection"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates necessary tables if they do not exist"""
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS owners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                address TEXT,
                phone TEXT
            )
        ''')
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS bank_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER,
                balance REAL,
                FOREIGN KEY (owner_id) REFERENCES owners(id)
            )
        ''')
        self.conn.commit()

    def get_all_owners(self):
        """Grabs all owners from the database"""
        self.cursor.execute('SELECT * FROM owners')
        return self.cursor.fetchall()

    def get_account_balance(self, owner_id):
        """Get the balance of an owner's bank account"""
        self.cursor.execute('SELECT balance FROM bank_accounts WHERE owner_id = ?', (owner_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0.0

    def get_total_balance(self):
        """Get the total balance of all bank accounts"""
        self.cursor.execute('SELECT SUM(balance) FROM bank_accounts')
        result = self.cursor.fetchone()
        return result[0] if result else 0.0

    def close_connection(self):
        """Closes the database connection"""
        self.conn.close()


# Pavyzdys, kaip naudoti

if __name__ == "__main__":
    # Sukuriame duomenų bazę
    db = Database()

    # Sukuriame savininką
    owner = Owner("John Doe", "123 Street", "1234567890")
    owner.save(db)  # Išsaugome savininką duomenų bazėje

    # Sukuriame banko sąskaitą su pirmu savininku
    account = BankAccount(owner, 1000.0)
    account.save(db)  # Išsaugome sąskaitą

    # Gauti sąskaitos balansą
    print(f"Owner: {owner}, Balance: {account.balance}")

    # Paimti visų savininkų sąrašą
    owners = db.get_all_owners()
    for owner_data in owners:
        print(f"Owner ID: {owner_data[0]}, Name: {owner_data[1]}, Address: {owner_data[2]}, Phone: {owner_data[3]}")

    # Paimti sąskaitos balansą pagal savininką
    owner_balance = db.get_account_balance(owner.id)
    print(f"Account balance for owner {owner.name}: {owner_balance}")

    # Paimti bendrą banko balansą
    total_balance = db.get_total_balance()
    print(f"Total balance in the bank system: {total_balance}")

    # Baigiame darbą su duomenų baze
    db.close_connection()
