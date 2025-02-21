
# Bank System with SQLite

This project implements a simple bank system that manages bank accounts and owners using SQLite as the database. It includes functionalities like creating owners, adding bank accounts, depositing and withdrawing money, and querying the total balance and account balances.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Classes and Functionality](#classes-and-functionality)
  - [Entity Class](#entity-class)
  - [Owner Class](#owner-class)
  - [BankAccount Class](#bankaccount-class)
  - [Database Class](#database-class)
- [Usage Example](#usage-example)
- [Database Structure](#database-structure)
- [License](#license)

---

## Overview

This application allows you to:

- Create owners with name, address, and phone number.
- Create bank accounts associated with owners.
- Deposit and withdraw money from bank accounts.
- Query the balance of individual accounts and the total balance across all accounts.

The system uses SQLite for data storage, with a simple relational schema to track owners and their associated bank accounts.

---

## Requirements

Before running the project, make sure you have:

- Python 3.x installed.
- SQLite3 (comes pre-installed with Python).
  
No additional libraries or dependencies are required, as SQLite and basic Python libraries are used.

---

## Setup Instructions

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/bank-system.git
   cd bank-system
   ```

2. The project uses SQLite for the database, so there are no additional setup steps for installing a database server. The database file will be automatically created when you run the code.

3. To run the application, simply execute the Python script:
   ```bash
   python bank_system.py
   ```

---

## Classes and Functionality

### Entity Class

The `Entity` class is the base class for both the `Owner` and `BankAccount` classes. It represents a general entity with an `id` field and provides a common structure for all database-related operations.

#### Methods:
- `__init__(self, id=None)`: Initializes the entity with an optional `id`.
- `save(self, db)`: Placeholder method to be implemented in subclasses. This method will save the entity to the database.

### Owner Class

The `Owner` class represents a bank customer who can own one or more bank accounts.

#### Constructor:
- `__init__(self, name, address, phone, id=None)`: Initializes the owner with a name, address, phone number, and optionally an `id` if the owner is already stored in the database.

#### Methods:
- `save(self, db)`: Saves the owner to the `owners` table in the database.
- `__str__(self)`: Returns a string representation of the owner for easy printing.

### BankAccount Class

The `BankAccount` class represents a bank account associated with an owner. It contains functionality for deposit, withdrawal, and saving the account information to the database.

#### Constructor:
- `__init__(self, owner, balance=0.0, id=None)`: Initializes the bank account with an owner, an initial balance, and optionally an `id` for existing accounts.

#### Methods:
- `deposit(self, amount, db)`: Deposits the specified amount into the account.
- `withdraw(self, amount, db)`: Withdraws the specified amount from the account if there are sufficient funds.
- `save(self, db)`: Saves the bank account to the `bank_accounts` table in the database.
- `__str__(self)`: Returns a string representation of the bank account with the owner's name and balance.

### Database Class

The `Database` class manages the connection to the SQLite database, creating the necessary tables and providing methods for querying and updating the data.

#### Constructor:
- `__init__(self, db_name="bank_system.db")`: Initializes the database connection and creates the necessary tables (`owners` and `bank_accounts`) if they do not already exist.

#### Methods:
- `create_tables(self)`: Creates the `owners` and `bank_accounts` tables if they don't exist.
- `get_all_owners(self)`: Returns a list of all owners from the database.
- `get_account_balance(self, owner_id)`: Returns the balance of the bank account associated with the specified owner.
- `get_total_balance(self)`: Returns the total balance of all bank accounts.
- `close_connection(self)`: Closes the connection to the SQLite database.

---

## Usage Example

Here is an example of how to use the classes to create owners, bank accounts, perform deposits and withdrawals, and query account balances.

```python
if __name__ == "__main__":
    # Create the database connection
    db = Database()

    # Create an owner
    owner = Owner("John Doe", "123 Street", "1234567890")
    owner.save(db)  # Save the owner to the database

    # Create a bank account for the owner
    account = BankAccount(owner, 1000.0)
    account.save(db)  # Save the account to the database

    # Print the owner's details and account balance
    print(f"Owner: {owner}, Balance: {account.balance}")

    # Get all owners from the database
    owners = db.get_all_owners()
    for owner_data in owners:
        print(f"Owner ID: {owner_data[0]}, Name: {owner_data[1]}, Address: {owner_data[2]}, Phone: {owner_data[3]}")

    # Get the balance for the specific owner's account
    owner_balance = db.get_account_balance(owner.id)
    print(f"Account balance for owner {owner.name}: {owner_balance}")

    # Get the total balance in the bank system
    total_balance = db.get_total_balance()
    print(f"Total balance in the bank system: {total_balance}")

    # Close the database connection
    db.close_connection()
```

---

## Database Structure

The SQLite database consists of two main tables:

### `owners` Table

| Column | Type       | Description |
|--------|------------|-------------|
| `id`   | INTEGER    | Primary Key (auto-increment) |
| `name` | TEXT       | Owner's name |
| `address` | TEXT    | Owner's address |
| `phone` | TEXT      | Owner's phone number |

### `bank_accounts` Table

| Column     | Type       | Description |
|------------|------------|-------------|
| `id`       | INTEGER    | Primary Key (auto-increment) |
| `owner_id` | INTEGER    | Foreign Key referencing `owners(id)` |
| `balance`  | REAL       | Account balance |

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

This `README.md` provides all the relevant information for setting up, running, and understanding the code. Let me know if you need any adjustments or additional information!
