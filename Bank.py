import sqlite3


# Base class that is inherited by Owner and BankAccount
class Entity:
    """General database object with an id"""

    def __init__(self, id=None):
        """Initializes the id"""
        self.id = id

    def save(self):
        """General method to save to the database (will be specific to each subclass)"""
        raise NotImplementedError("This method must be implemented in the subclass")


# Owner class, inherited from Entity
class Owner(Entity):
    """Owner - inherits from the Entity class"""

    def __init__(self, name, address, phone, id=None):
        super().__init__(id)
        self.name = name
        self.address = address
        self.phone = phone

    def save(self, db):
        """Saves the owner to the database"""
        if self.id is None:
            db.cursor.execute(
                """INSERT INTO owners (name, address, phone)
                                VALUES (?, ?, ?)""",
                (self.name, self.address, self.phone),
            )
            db.conn.commit()
            self.id = db.cursor.lastrowid
        else:
            db.cursor.execute(
                """UPDATE owners SET name = ?, address = ?, phone = ? WHERE id = ?""",
                (self.name, self.address, self.phone, self.id),
            )
            db.conn.commit()

    def __str__(self):
        return f"Owner {self.name} at {self.address} ({self.phone})"


# Bank account class, inherited from Entity
class BankAccount(Entity):
    """Bank account - inherits from the Entity class"""

    def __init__(self, owner, balance=0.0, id=None):
        super().__init__(id)  # Call the superclass constructor to pass the id
        self.owner = owner
        self.balance = balance

    def deposit(self, amount, db):
        """Deposit money into the account"""
        if amount > 0:
            self.balance += amount
            self.save(db)  # Save the changes to the database
            return f"Deposited {amount}. New balance: {self.balance}"
        return "Invalid deposit amount"

    def withdraw(self, amount, db):
        """Withdraw money from the account"""
        if amount <= 0:
            return "Invalid withdraw amount"
        if amount > self.balance:
            return "Invalid withdraw amount or insufficient funds"
        self.balance -= amount
        self.save(db)  # Save the changes to the database
        return f"Withdrew {amount}. New balance: {self.balance}"

    def save(self, db):
        """Saves the bank account to the database"""
        if self.id is None:
            db.cursor.execute(
                """INSERT INTO bank_accounts (owner_id, balance)
                                VALUES (?, ?)""",
                (self.owner.id, self.balance),
            )
            db.conn.commit()
            self.id = db.cursor.lastrowid
        else:
            db.cursor.execute(
                """UPDATE bank_accounts SET owner_id = ?, balance = ? WHERE id = ?""",
                (self.owner.id, self.balance, self.id),
            )
            db.conn.commit()

    def __str__(self):
        return f"Account of {self.owner.name} with balance {self.balance}"


## Database class that manages the connection with SQLite
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
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS owners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                address TEXT,
                phone TEXT
            )
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bank_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER,
                balance REAL,
                FOREIGN KEY (owner_id) REFERENCES owners(id)
            )
        """
        )
        self.conn.commit()

    def get_all_owners(self):
        """Gets all owners from the database"""
        self.cursor.execute("SELECT * FROM owners")
        return self.cursor.fetchall()

    def get_account_balance(self, owner_id):
        """Gets the balance of an owner's bank account"""
        self.cursor.execute(
            "SELECT balance FROM bank_accounts WHERE owner_id = ?", (owner_id,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else 0.0

    def get_total_balance(self):
        """Gets the total balance of all bank accounts"""
        self.cursor.execute("SELECT SUM(balance) FROM bank_accounts")
        result = self.cursor.fetchone()
        return result[0] if result else 0.0

    def close_connection(self):
        """Closes the database connection"""
        self.conn.close()


# Example usage
if __name__ == "__main__":
    # Create the database
    db = Database()

    # Create the owner
    owner = Owner("John Doe", "123 Street", "1234567890")
    owner.save(db)  # Save the owner to the database

    # Create a bank account with the first owner
    account = BankAccount(owner, 1000.0)
    account.save(db)  # Save the account

    # Get the account balance
    print(f"Owner: {owner}, Balance: {account.balance}")

    # Get the list of all owners
    owners = db.get_all_owners()
    for owner_data in owners:
        print(
            f"Owner ID: {owner_data[0]}, Name: {owner_data[1]}, Address: {owner_data[2]}, Phone: {owner_data[3]}"
        )

    # Get the account balance by owner
    owner_balance = db.get_account_balance(owner.id)
    print(f"Account balance for owner {owner.name}: {owner_balance}")

    # Get the total bank balance
    total_balance = db.get_total_balance()
    print(f"Total balance in the bank system: {total_balance}")

    # Close the database connection
    db.close_connection()
