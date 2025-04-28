class BankAccount:

    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def get_balance(self):
        return self.balance
    
    def get_account_number(self):
        return self.account_number
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if amount <= 0:
            return False
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def transfer(self, amount, deposit_account):
        if self.withdraw(amount):
            deposit_account.deposit(amount)
            return True
        return False

class Payroll:

    def __init__(self):
        self.accounts = {}
        self.budget = 0
    
    def add_account(self, account):
        if account.account_number not in self.accounts:
            self.accounts[account.account_number] = account
            return True
        else:
            return False
        
    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            return True
        else:
            return False
    
    def pay_employee(self, account, wage, hours):
        if account.account_number in self.accounts:
            if wage > 0 and hours > 0:
                paycheck = wage * hours
                if paycheck <= self.budget:
                    account.deposit(paycheck)
                    return True
                else:
                    return False
            else:
                return False
        return False
    
    def set_budget(self, budget):
        if isinstance(budget, int) and budget >= 0:
            self.budget = budget
            return True
        return False