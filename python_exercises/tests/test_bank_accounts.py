from python_exercises.oop.bank_accounts import BankAccount, SavingsAccount, InsufficientFunds

def test_deposit_and_withdraw():
    acc = BankAccount("Test User", "BA-1", 100)
    acc.deposit(50)
    assert acc.balance == 150
    acc.withdraw(25)
    assert acc.balance == 125

def test_insufficient_funds():
    acc = BankAccount("User", "BA-2", 10)
    try:
        acc.withdraw(20)
        assert False, "Expected InsufficientFunds"
    except InsufficientFunds:
        assert True

def test_interest():
    acc = SavingsAccount("User", "SA-1", 1000, interest_rate=0.10)
    acc.apply_interest()
    assert acc.balance == 1100
