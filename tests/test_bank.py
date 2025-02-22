import unittest
from Bank import Database, Owner, BankAccount


class TestBankSystem(unittest.TestCase):
    """Unit tests for Bank System"""

    def setUp(self):
        """Setup for the tests"""
        self.db = Database()  # Create a database object
        self.owner = Owner("John Doe", "123 Street", "1234567890")
        self.owner.save(self.db)  # Save the owner to the database
        self.account = BankAccount(self.owner, 100.0)
        self.account.save(self.db)  # Save the account to the database

    def test_bank_account_deposit(self):
        """Tests deposit function in BankAccount"""
        result = self.account.deposit(50, self.db)
        print(
            f"Updated balance after deposit: {self.account.balance}"
        )  # Print the updated balance
        self.assertEqual(result, "Deposited 50. New balance: 150.0")

    def test_bank_account_withdraw(self):
        """Tests withdraw function in BankAccount"""
        self.assertEqual(
            self.account.withdraw(30, self.db), "Withdrew 30. New balance: 70.0"
        )
        print(f"Updated balance after withdrawal: {self.account.balance}")

    def test_bank_account_insufficient_funds(self):
        """Test to ensure withdrawal returns the correct error for insufficient funds."""
        self.account.balance = 0.0  # Set balance to 0
        result = self.account.withdraw(100, self.db)
        self.assertEqual(result, "Invalid withdraw amount or insufficient funds")
        # Print the result of the withdrawal attempt
        print(f"Withdrawal result: {result}")
        # Print the updated balance after the withdrawal attempt
        print(f"Updated balance after withdrawal attempt: {self.account.balance}")


if __name__ == "__main__":
    unittest.main()
