"""
Fill-In Challenge #5 — Basic Class

Implement the methods in the BankAccount class below.
"""


class BankAccount:
    """A simple bank account with deposit, withdrawal, and transfer.

    Attributes:
        owner: The account holder's name (string).
        balance: Current balance in dollars (float), starts at 0.
    """

    def __init__(self, owner, balance=0.0):
        """Initialize the account.

        Args:
            owner: Account holder's name.
            balance: Starting balance (default 0.0).
        """
        # YOUR CODE HERE
        pass

    def __str__(self):
        """Return a string like 'BankAccount(Alice, $150.00)'.

        Format the balance to 2 decimal places.
        """
        # YOUR CODE HERE
        pass

    def deposit(self, amount):
        """Add money to the account.

        Args:
            amount: Dollars to deposit (must be positive).

        Returns:
            The new balance.

        Raises:
            ValueError: If amount is not positive.
        """
        # YOUR CODE HERE
        pass

    def withdraw(self, amount):
        """Remove money from the account.

        Args:
            amount: Dollars to withdraw (must be positive).

        Returns:
            The new balance.

        Raises:
            ValueError: If amount is not positive or exceeds balance.
        """
        # YOUR CODE HERE
        pass

    def transfer(self, other, amount):
        """Transfer money from this account to another.

        Args:
            other: Another BankAccount instance.
            amount: Dollars to transfer.

        Returns:
            A tuple of (self.balance, other.balance) after transfer.

        Raises:
            ValueError: If amount is not positive or exceeds self.balance.
        """
        # YOUR CODE HERE
        pass
