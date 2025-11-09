from bank_accounts import BankAccount, SavingsAccount, InsufficientFunds

if __name__ == "__main__":
    acc = BankAccount(holder="Anita Sharma", number="BA-1001", balance=1000)
    print("Created:", acc)
    acc.deposit(500)
    print("After deposit:", acc)
    try:
        acc.withdraw(1700)  # should raise
    except InsufficientFunds as e:
        print("Handled:", e)
    acc.withdraw(200)
    print("After withdraw:", acc)

    sav = SavingsAccount(holder="Ravi Khan", number="SA-2001", balance=2000, interest_rate=0.05)
    print("\nCreated:", sav)
    sav.apply_interest()
    print("After interest:", sav)
