from __future__ import annotations

class InsufficientFunds(Exception):
    pass

class BankAccount:
    def __init__(self, holder: str, number: str, balance: float = 0.0):
        self.holder = holder
        self.number = number
        self.balance = float(balance)

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Deposit must be > 0")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdrawal must be > 0")
        if amount > self.balance:
            raise InsufficientFunds(f"Need {amount}, have {self.balance}")
        self.balance -= amount
        return self.balance

    def __repr__(self) -> str:
        return f"<BankAccount {self.number} {self.holder} balance={self.balance:.2f}>"

class SavingsAccount(BankAccount):
    def __init__(self, holder: str, number: str, balance: float = 0.0, interest_rate: float = 0.04):
        super().__init__(holder, number, balance)
        self.interest_rate = float(interest_rate)

    def apply_interest(self) -> float:
        interest = self.balance * self.interest_rate
        self.balance += interest
        return self.balance

    def __repr__(self) -> str:
        return f"<SavingsAccount {self.number} {self.holder} balance={self.balance:.2f} rate={self.interest_rate:.2%}>"
