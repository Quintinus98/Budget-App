import pandas as pd
import os
import sys
import numpy as np

categories = ["Food", "Clothing", "Entertainment"]
df = pd.DataFrame({'Category': categories, 'Deposits': [1000, 1000, 1000], 'Withdrawals': [0, 0, 0]})


def generateFilePath():
    file_path = r'.\{}.csv'.format("Budget")
    return file_path


def selectCategory():
    print("\nAvailable Categories include:\n\t0. %s\n\t1. %s\n\t2. %s"
          % (categories[0], categories[1], categories[2]))
    while True:
        category = int(input("Select a budget category(0/1/2): "))
        if category in (0, 1, 2):
            return categories[category]
        else:
            print("Input a number from 0 - 2.\n")


class Budget:
    def __init__(self):
        self.category = None
        self.startBudget()

    def startBudget(self):
        print("""\nBUDGET CLASS
This is a Budget class that can instantiate objects based on
different budget categories like Food, Clothing and Entertainment.
:return: You can deposit and withdraw funds, check and transfer balance.
        """)
        choices = ["Deposit Funds", "Withdraw Funds", "Check Balance", "Transfer Balance", "Quit"]
        print("What would you like to do:")
        for choice in choices:
            print("{}. {}".format(choices.index(choice), choice))  # Print the options along with its index

        while True:
            response = int(input("Enter option (0-4): "))
            if response in (0, 1, 2, 3, 4):
                break

        if response == 3:
            self.transferBalance()
        elif response == 4:
            print("Have a wonderful day!")
            sys.exit()

        self.category = selectCategory()

        if response == 0:
            self.depositFunds()
        elif response == 1:
            self.withdrawFunds()
        elif response == 2:
            self.checkBalance()
        else:
            print("Reaching here should be impossible.")

    def depositFunds(self):
        print("\nWelcome to Deposit!")
        file_path = generateFilePath()
        if os.path.isfile(file_path):
            new_deposit = float(input("How much do you want to deposit: "))
            if new_deposit < 0:
                new_deposit = 0
            position = categories.index(self.category)
            data = pd.read_csv(file_path)
            data.loc[position, 'Deposits'] += new_deposit
            print(data.head())
            data.to_csv(file_path, index=False)
            self.startBudget()
        else:
            print("You have a start fund of 1000.")
            new_deposit = float(input("How much do you want to deposit: "))
            if new_deposit < 0:
                new_deposit = 0
            position = categories.index(self.category)
            df.loc[position, 'Deposits'] += new_deposit
            print(df.head())
            df.to_csv(file_path, index=False)
            self.startBudget()

    def withdrawFunds(self):
        print("\nWelcome to withdraw!")
        file_path = generateFilePath()
        if os.path.isfile(file_path):
            data = pd.read_csv(file_path)
            position = categories.index(self.category)
            max_withdrawal = data.loc[position, 'Deposits']
            for _ in range(3):
                new_withdrawal = float(input("How much do you want to withdraw: "))
                if new_withdrawal < 0:
                    print("No negative withdrawals.")
                elif new_withdrawal > max_withdrawal:
                    print("You cannot withdraw more than {}".format(max_withdrawal))
                else:
                    break
            else:
                print("Setting withdrawal to 0")
                new_withdrawal = 0
            data.loc[position, 'Withdrawals'] = new_withdrawal
            print(data.head())
            data.to_csv(file_path, index=False)
            print("This withdrawal will not be made unless you compute your Balance.")
            response = input("Compute Balance now (y/n)")
            if response in ('y', 'Yes', 'yes', 'Y'):
                self.computeBalance()
            self.startBudget()
        else:
            print("Perform a deposit first.")
            self.startBudget()

    def checkBalance(self):
        print("\nWelcome to Check Balance!")
        balance = self.computeBalance()
        position = categories.index(self.category)
        print("\nYour current balance for {} is {}".format(self.category, balance[position]))

    @staticmethod
    def computeBalance():
        file_path = generateFilePath()
        if os.path.isfile(file_path):
            data = pd.read_csv(file_path)
            for category in categories:
                position = categories.index(category)
                deposit = data.loc[position, 'Deposits']
                withdrawal = data.loc[position, 'Withdrawals']
                balance = deposit - withdrawal
                data.loc[position, 'Deposits'] = balance
                data.loc[position, 'Withdrawals'] = 0
            data.to_csv(file_path, index=False)
            print(data.head())
            return list(data['Deposits'])
        else:
            print(df.head())
            return list(df['Deposits'])

    def transferBalance(self):
        print("\nWelcome to Transfer Balance!")
        # print("\n\"You've left the category {}\"".format(self.category))
        print("See Deposits below. NB: Deposits are your Balances")
        categoriesBalances = self.computeBalance()
        print("\nAvailable Budget Categories are: ")
        print("\t0. %s\n\t1. %s\n\t2. %s" % (categories[0], categories[1], categories[2]))

        while True:
            toTransfer = int(input("Enter index of category you want to transfer TO: "))
            if toTransfer in range(len(categories)):
                print("You've selected {}".format(categories[toTransfer]))
                break
        while True:
            fromTransfer = int(input("Enter index of category you want to transfer FROM: "))
            if fromTransfer in range(len(categories)):
                print("You've selected {}".format(categories[fromTransfer]))
                break
        transferCategory = categories[fromTransfer]
        maxTransfer = categoriesBalances[fromTransfer]
        print("\nMaximum allowable transfer for {} is {}".format(transferCategory, maxTransfer))
        transferValue = 0
        for _ in range(3):
            transferValue = float(input("Enter transfer amount: "))
            if transferValue < 0:
                print("No negative transfers.")
            elif transferValue > maxTransfer:
                print("You cannot withdraw more than {}".format(maxTransfer))
            else:
                break
        file_path = generateFilePath()
        if os.path.isfile(file_path):
            data = pd.read_csv(file_path)
            data.loc[toTransfer, 'Deposits'] += transferValue
            data.loc[fromTransfer, 'Deposits'] -= transferValue
            print("Transfer successful. View details of transfer below.\n")
            print(data.head())
            data.to_csv(file_path, index=False)
            main()
        else:
            df.loc[toTransfer, 'Deposits'] += transferValue
            df.loc[fromTransfer, 'Deposits'] -= transferValue
            print("Transfer successful. View details of transfer below.\n")
            print(df.head())
            df.to_csv(file_path, index=False)
            main()

        pass


def main():
    Budget()


if __name__ == '__main__':
    main()
