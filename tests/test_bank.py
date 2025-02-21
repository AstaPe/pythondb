import unittest
from namu_darbai.DB.Bank import Owner, BankAccount, Database


class TestBankSystem(unittest.TestCase):
    """Unit tests for Bank System"""

    def setUp(self):
        """Setup for the tests"""
        self.db = Database()  # Sukuriame duomenų bazės objektą
        self.owner = Owner("John Doe", "123 Street", "1234567890")
        self.owner.save(self.db)  # Išsaugome savininką į duomenų bazę
        self.account = BankAccount(self.owner, 100.0)
        self.account.save(self.db)  # Išsaugome sąskaitą

    def test_bank_account_deposit(self):
        """Tests deposit function in BankAccount"""
        self.assertEqual(
            self.account.deposit(50, self.db), "Deposited 50. New balance: 150.0"
        )

    def test_bank_account_withdraw(self):
        """Tests withdraw function in BankAccount"""
        self.assertEqual(
            self.account.withdraw(30, self.db), "Withdrew 30. New balance: 70.0"
        )

    def test_bank_account_insufficient_funds(self):
        """Test to ensure withdrawal returns the correct error for insufficient funds."""
        self.account.balance = 0.0  # Set balance to 0
        result = self.account.withdraw(100, self.db)
        self.assertEqual(result, "Invalid withdraw amount or insufficient funds")


if __name__ == "__main__":
    unittest.main()
