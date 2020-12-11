"""
This file contains code for the application "Mini ATM App".
Author: DtjiSoftwareDeveloper
"""


# Importing necessary libraries


import sys
import copy
import pickle
import os


# Creating static functions


def load_bank_account_database(file_name):
    # type: (str) -> BankAccountDatabase
    return pickle.load(open(file_name, "rb"))


def save_bank_account_database(bank_account_database, file_name):
    # type: (BankAccountDatabase, str) -> None
    pickle.dump(bank_account_database, open(file_name, "wb"))


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary classes


class BankAccount:
    """
    This class contains attributes of a bank account.
    """

    def __init__(self, username, pin):
        # type: (str, int) -> None
        self.username: str = username
        self.pin: int = pin if len(str(pin)) == 4 else 0000
        self.amount: float = 0

    def change_pin(self, new_pin):
        # type: (int) -> bool
        if len(str(new_pin)) == 4:
            self.pin = new_pin
            return True
        return False

    def withdraw(self, amount):
        # type: (float) -> bool
        if amount <= self.amount:
            self.amount -= amount
            return True
        return False

    def deposit(self, amount):
        # type: (float) -> None
        self.amount += amount

    def clone(self):
        # type: ( )-> BankAccount
        return copy.deepcopy(self)


class BankAccountDatabase:
    """
    This class contains attributes of a bank account database.
    """

    def __init__(self, bank_accounts=None):
        # type: (list) -> None
        if bank_accounts is None:
            bank_accounts = []

        self.__bank_accounts: list = bank_accounts

    def get_bank_account_by_username(self, username):
        # type: (str) -> BankAccount
        for bank_account in self.__bank_accounts:
            if bank_account.username == username:
                return bank_account

        return None

    def get_bank_accounts(self):
        # type: () -> list
        return self.__bank_accounts

    def add_bank_account(self, bank_account):
        # type: (BankAccount) -> bool
        if bank_account.username not in [bank_account.username for bank_account in self.__bank_accounts]:
            self.__bank_accounts.append(bank_account)
            return True
        return False

    def remove_bank_account(self, bank_account):
        # type: (BankAccount) -> bool
        if bank_account in self.__bank_accounts:
            self.__bank_accounts.remove(bank_account)
            return True
        return False

    def clone(self):
        # type: () -> BankAccountDatabase
        return copy.deepcopy(self)


# Creating main function used to run the application.


def main():
    """
    This main function is used to run the application.
    :return: None
    """

    print("Welcome to 'Mini ATM App' by 'DtjiSoftwareDeveloper'.")
    print("This application is a simple ATM app helping you understand how a real ATM works.")

    # Automatically load saved bank account database
    file_name: str = "SAVED BANK ACCOUNT DATABASE"
    new_bank_account_database: BankAccountDatabase
    try:
        new_bank_account_database = load_bank_account_database(file_name)

        # Clearing up the command line window
        clear()

    except FileNotFoundError:
        new_bank_account_database = BankAccountDatabase()

    print("Enter 'Y' for yes.")
    print("Enter anything else for no.")
    continue_using: str = input("Do you want to continue using 'Mini ATM App'? ")
    while continue_using == "Y":
        selected_bank_account: BankAccount = None  # initial value
        if len(new_bank_account_database.get_bank_accounts()) == 0:
            # Clearing the command line window
            clear()
            # Ask the user to create a new bank account
            print("You will need to create a new bank account.")
            username: str = input("Enter your username: ")
            pin: int = int(input("Enter your PIN: "))
            while not len(str(pin)) == 4:
                pin = int(input("Sorry, invalid input! Enter your PIN: "))

            new_bank_account: BankAccount = BankAccount(username, pin)
            new_bank_account_database.add_bank_account(new_bank_account)
            selected_bank_account = new_bank_account
        else:
            # Clearing the command line window
            clear()
            # Ask the user to choose from creating a new bank account or logging into one
            print("Enter 'CREATE NEW' to create a new bank account.")
            print("Enter 'LOGIN' to login.")
            decision: str = input("Do you want to create a new bank account or login into one? ")
            while decision not in ["CREATE NEW", "LOGIN"]:
                decision = input("Sorry, invalid input! Do you want to create a new bank account or login into one? ")

            if decision == "CREATE NEW":
                # Clearing the command line window
                clear()
                # Ask the user to create a new bank account
                print("You will need to create a new bank account.")
                username: str = input("Enter your username: ")
                pin: int = int(input("Enter your PIN: "))
                while not len(str(pin)) == 4:
                    pin = int(input("Sorry, invalid input! Enter your PIN: "))

                new_bank_account: BankAccount = BankAccount(username, pin)
                new_bank_account_database.add_bank_account(new_bank_account)
                selected_bank_account = new_bank_account
            else:
                # Clearing the command line window
                clear()
                username: str = input("Enter your username: ")
                tries: int = 1
                try_success: bool = True
                while username not in [account.username for account in new_bank_account_database.get_bank_accounts()]:
                    if tries < 3:
                        username = input("Invalid username! Try again! ")
                    else:
                        print("You have exceeded the allowed number of tries.")
                        try_success = False
                        break
                    tries += 1

                if try_success:
                    # Clearing the command line window
                    clear()
                    pin: int = int(input("Enter your PIN: "))
                    tries = 1
                    pin_try_success: bool = True
                    selected_bank_account = new_bank_account_database.get_bank_account_by_username(username)
                    while pin != selected_bank_account.pin:
                        if tries < 3:
                            pin = int(input("Wrong PIN! Try again! "))
                        else:
                            print("You have exceeded the allowed number of tries.")
                            pin_try_success = False
                            break
                        tries += 1

                    if pin_try_success:
                        # Clearing the command line window
                        clear()

                        print("You have successfully logged in to your bank account! Continue!")
                        allowed_actions: list = ["VIEW BANK STATEMENT", "DEPOSIT", "WITHDRAW"]
                        print("Enter 'VIEW BANK STATEMENT' to view bank statement.")
                        print("Enter 'DEPOSIT' to deposit cash into your bank account.")
                        print("Enter 'WITHDRAW' to withdraw from your bank account.")
                        chosen_action: str = input("What do you want to do? ")
                        while chosen_action not in allowed_actions:
                            print("Enter 'VIEW BANK STATEMENT' to view bank statement.")
                            print("Enter 'DEPOSIT' to deposit cash into your bank account.")
                            print("Enter 'WITHDRAW' to withdraw from your bank account.")
                            chosen_action = input("Sorry, invalid input! What do you want to do? ")

                        if chosen_action == "VIEW BANK STATEMENT":
                            # Clearing the command line window
                            clear()
                            print("You have " + str(selected_bank_account.amount) + " dollars!")
                            string: str = input("Enter anything to proceed: ")
                        elif chosen_action == "DEPOSIT":
                            # Clearing the command line window
                            clear()
                            deposit_amount: float = float(input("How many dollars do you want to deposit to your "
                                                                "bank account? "))
                            selected_bank_account.deposit(deposit_amount)
                        else:
                            # Clearing the command line window
                            clear()
                            withdraw_amount: float = float(input("How many dollars do you want to withdraw from your "
                                                                 "bank account? "))
                            if selected_bank_account.withdraw(withdraw_amount):
                                print("You have successfully withdrawn " + str(withdraw_amount) + " dollars!")
                            else:
                                print("Sorry, you have insufficient amount of money in your bank account!")

        # Clearing the command line window
        clear()

        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_using = input("Do you want to continue using 'Mini ATM App'? ")
    sys.exit()


if __name__ == '__main__':
    main()
