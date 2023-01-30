from abc import abstractmethod, ABC
from random import randint


# Dataclass
class Customer:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email


class Account(ABC):
    def __init__(self, pin, customer, balance):
        self.number = randint(1000, 9999)
        self.pin = pin
        self.customer = customer
        self.balance = balance

    @staticmethod
    def get_account(pin, customer, balance, account_type):
        if account_type == "Checking":
            return Checking(pin, customer, balance)
        else:
            return Savings(pin, customer, balance)

    @abstractmethod
    def account_type(self):
        pass


class Checking(Account):
    def account_type(self):
        return "Checking Account"


class Savings(Account):
    def account_type(self):
        return "Savings Account"


class Transaction(ABC):
    def __init__(self, account):
        self.account = account
        self.id = randint(1000, 9999)

    def start(self):
        print("--------------------------------------------------------------------")
        print("Initiating transaction:", self.id)

        self.process()

    def print_new_balance(self):
        print("Your new account balance is: ", self.account.balance)

    @abstractmethod
    def process(self):
        pass

    def end_transaction(self):
        print("You've completed this transaction. "
              "Transaction receipt has been sent to your email:", self.account.customer.email)
        print("Good bye, have a good day!")


class Withdrawal(Transaction):
    def process(self):
        amount = float(input("Enter the amount to be withdrawn: "))

        if amount <= self.account.balance:
            self.account.balance -= amount
            print("Please collect your cash.")
            self.print_new_balance()
        else:
            print("Cannot withdraw, current balance is {}".format(self.account.balance))

        self.end_transaction()


class BalanceInquiry(Transaction):
    def process(self):
        print("Your account balance is: ", self.account.balance)
        self.end_transaction()


class Deposit(Transaction, ABC):
    @staticmethod
    def deposit(account):
        print("Enter A for cash deposit\nEnter B for cheque deposit")
        print("--------------------------------------------------------------------")
        deposit_type = input("Enter your choice: ")

        if deposit_type == "A":
            Cash(account).start()
        elif deposit_type == "B":
            Cheque(account).start()
        else:
            print("You've cancelled this transaction. Good bye, have a good day!")

    @staticmethod
    def print_amount_deposited():
        print("The amount has been deposited.")


class Cheque(Deposit):
    def process(self):
        input("Enter cheque number (any random number): ")
        amount = float(input("Enter amount to be deposited: "))
        self.account.balance += amount
        Deposit.print_amount_deposited()
        self.print_new_balance()
        self.end_transaction()


class Cash(Deposit):
    def process(self):
        amount = int(input("Enter amount to be deposited: "))
        self.account.balance += amount
        Deposit.print_amount_deposited()
        self.print_new_balance()
        self.end_transaction()


class ATM:
    def __init__(self):
        self.accounts = {}

    def authenticate(self, account_number, account_pin):
        return account_number in self.accounts \
               and self.accounts[account_number].pin == account_pin

    def create_account(self, name, phone, email, account_type):
        customer = Customer(name, phone,  email)
        account = Account.get_account(randint(100, 999), customer, randint(1000, 1000000), account_type)
        self.accounts[account.number] = account
        print("Account no: ", account.number, "| Pin:", account.pin)

    def start_transaction(self):
        print("\n\n**************** Welcome to the ATM ****************")
        account_number = int(input("Enter your account number: "))
        account_pin = int(input("Enter your account pin number: "))
        if not self.authenticate(account_number, account_pin):
            print("Invalid account or account pin number, please start over.")
            return

        print("--------------------------------------------------------------------")
        account = self.accounts[account_number]
        print("Hello {}!".format(account.customer.name))
        print("The account you are using is a {}.".format(account.account_type()))

        print("--------------------------------------------------------------------")
        print("Which transaction would you like to initiate today?")
        print("Enter 0 for Withdrawal\nEnter 1 for Balance Inquiry\nEnter 2 for Deposit\nEnter 3 for Exit")

        print("--------------------------------------------------------------------")
        transaction_type = int(input("Enter your choice: "))

        if transaction_type == 0:
            Withdrawal(account).start()
        elif transaction_type == 1:
            BalanceInquiry(account).start()
        elif transaction_type == 2:
            Deposit.deposit(account)
        else:
            print("You've cancelled this transaction. Good bye, have a good day!")


# Start of main program
atm = ATM()
print("Seeding accounts\n(Please use the below accounts)")
atm.create_account("John", 4154567876, "john@gmaill.com", "Checking")
atm.create_account("Summer", 6504567876, "summer@yahoo.com", "Savings")
atm.create_account("Jane", 9204567878, "jane@gmail.com", "Savings")
atm.create_account("April", 2024567878, "april@gmail.com", "Checking")
atm.create_account("June", 2674567878, "june@gmaill.com", "Savings")
print("Starting ATM...")

while True:
    try:
        atm.start_transaction()
    except Exception as _:
        print("Invalid input, restarting.")
