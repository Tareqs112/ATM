import os
from enum import Enum
from abc import ABC, abstractmethod
import datetime
import uuid


def clear_screen():
  
    os.system("cls")


class TransactionType(Enum):
    WITHDRAW = "withdraw"
    DEPOSIT = "deposit"
    BALANCE_INQUIRY = "balance inquiry"
class Bank:
    def __init__(self, name, swift_code=1789):
        self.name = name
        self.swift_code = swift_code
        self.customers = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def authenticate(self, card_number, pin):
        
            for customer in self.customers:
                for account in customer.accounts:
                    if account.linked_cards and account.linked_cards.number == card_number and account.linked_cards.pin == pin:
                        return account
                
            return None

class Customer:
    def __init__(self, name, address, phone_number, email):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

class Account:
    def __init__(self, account_number):
        self.number = account_number
        self.balance = 0
        self.linked_cards = None
        self.transactions_history = []
        

    def display_transactions_history(self):
        if self.transactions_history:
            print("Transactions history:\n")
            for transaction in self.transactions_history:
                print(f"ID:{transaction.transaction_id}\nType:{transaction.transaction_type.value}\nAmount:{transaction.amount}\nTime:{transaction.timestamp}\n")
                input("\nPress any key to pass: ")
                clear_screen()        
        else:
            print("You don't have any tansactions yet!")
            clear_screen()

    def add_transaction(self, transaction):
        self.transactions_history.append(transaction)

    def link_card(self, card):
        self.linked_cards = card

class Card:
    def __init__(self, number, pin):
        self.number = number
        self.pin = pin
   

class Atm:
    def __init__(self, bank, atm_location):
        self.bank = bank
        self.atm_location = atm_location
        self.Keyad = Keyad()
        self.screen = Screen()

    def insert_card(self, card_number):
        while True:
            pin = self.Keyad.get_input("Enter your PIN: ")
            account = self.bank.authenticate(card_number, pin)
            if account:
                self.screen.show_message("Authentication successful.")
                clear_screen()
                self.display_main_menu(account)
                break
            else:
                self.screen.show_message("Authentication failed. Invalid card number or PIN.")
                clear_screen()

    def display_main_menu(self, account):
        message = '''
            1. Withdraw
            2. Deposit
            3. Balance Inquiry
            4. View Transactions
            5. Exit
            Choose an option: '''
        while True:
            choice = self.Keyad.get_input(message)
            if choice == "5":
                self.screen.show_message("Thank you!")
                break
            self.handling_transactions(choice, account)

    def handling_transactions(self, choice, account):
        try:
            match choice:
                case "1":
                    amount = int(self.Keyad.get_input("Enter the amount to withdraw: "))
                    transaction = WithdrawTransaction(amount)
                case "2":
                    amount = int(self.Keyad.get_input("Enter the amount to deposit: "))
                    transaction = DepositTransaction(amount)
                case "3":
                    transaction = PreviewBalance()
                case "4":
                    account.display_transactions_history()
                    return
                case _:
                    self.screen.show_message("Invalid choice")
                    return
            transaction.execute(account)
            self.Keyad.get_input("\nPress any key to pass: ")
            clear_screen()

            
        except ValueError:
            self.screen.show_message("Invalid choice... Please enter a valid number.")

class Transaction(ABC):
    def __init__(self, transaction_type, amount=None):
        self.transaction_id = uuid.uuid4()
        self.timestamp = datetime.datetime.now()
        self.transaction_type = transaction_type
        self.amount = amount

    @abstractmethod
    def execute(self, account):
        pass

class WithdrawTransaction(Transaction):
    def __init__(self, amount):
        super().__init__(TransactionType.WITHDRAW, amount)

    def execute(self, account):
        if account.balance >= self.amount:
            account.balance -= self.amount
            print(f"Withdrawal successful. Your new balance is {account.balance}")
            account.add_transaction(self)
        else:
            print("Insufficient funds!")

class DepositTransaction(Transaction):
    def __init__(self, amount):
        super().__init__(TransactionType.DEPOSIT, amount)

    def execute(self, account):
        account.balance += self.amount
        print(f"Deposit successful. Your new balance is {account.balance}")
        account.add_transaction(self)

class PreviewBalance(Transaction):
    def __init__(self):
        super().__init__(TransactionType.BALANCE_INQUIRY, amount = 0)

    def execute(self, account):
        self.amount = account.balance
        print(f"Your balance is {account.balance}")
        account.add_transaction(self)
class Keyad:
    def get_input(self, message):
        return (input(message))
class Screen:
    def show_message(self, message):
        print(message)

# Example usage:
bank = Bank("Tareq Bank", "TAREQQS")
customer1 = Customer("Tareq", "Turkey, Bartin", "+905540554590", "altmimytar@gmail.com")
account1 = Account("1122")
card1 = Card("774555888888", "4569")
account1.link_card(card1)
customer1.add_account(account1)
bank.add_customer(customer1)

atm = Atm(bank, "bartin")
atm.insert_card(card1.number)
