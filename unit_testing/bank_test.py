import bank
import pytest

#functions testing init 
def test_init():
    print("testing initialization")
    a = bank.BankAccount(1234, 20)
    assert a.account_number == 1234
    assert a.balance == 20
    a = bank.BankAccount(1, -40)
    assert a.account_number == 1
    assert a.balance == -40
    a = bank.BankAccount(18264912743, 97254917351983724)
    assert a.account_number == 18264912743
    assert a.balance == 97254917351983724



#functions to test deposit
def test_pos_deposit():
    print("testing positive deposits")
    a = bank.BankAccount(1234, 30)
    assert a.deposit(10) == True
    assert a.balance == 40
    assert a.deposit(2000000) == True
    assert a.balance == 2000040
def test_neg_deposit():
    print("testing negative deposits")
    a = bank.BankAccount(1234, 20)
    assert a.deposit(-2) == False
    assert a.balance == 20
    assert a.deposit(-0) == False
    assert a.balance == 20
    assert a.deposit(-92351923875) == False
    assert a.balance == 20

#functions to test withdraw
def test_valid_withdraw():
    print("testing valid withdraw")
    a = bank.BankAccount(1234, 20)
    assert a.withdraw(5) == True
    assert a.balance == 15
    assert a.withdraw(3) == True
    assert a.balance == 12
def test_neg_withdraw():
    print("testing negative withdraw")
    a = bank.BankAccount(1234,20)
    assert a.withdraw(-40) == False
    assert a.balance == 20
    assert a.withdraw(-0) == False
    assert a.withdraw(-923751239) == False
    assert a.balance == 20
def test_over_withdraw():
    print("testing over withdraw")
    a = bank.BankAccount(1234, 20)
    assert a.withdraw(21) == False
    assert a.withdraw(29384723) == False
    assert a.balance == 20
def test_total_withdraw():
    print("testing total withdraw")
    a = bank.BankAccount(1234, 20)
    assert a.withdraw(20) == True
    assert a.balance == 0
def test_zero_withdraw():
    print("testing 0 withdraw")
    a = bank.BankAccount(1234, 20)
    assert a.withdraw(0) == False
    assert a.balance == 20

#functions to test getters
def test_get_balance():
    print("testing get balance")
    a = bank.BankAccount(1234, 20)
    assert a.get_balance() == 20
    a = bank.BankAccount(829347, 9028350918)
    assert a.get_balance() == 9028350918
def test_get_account_number():
    print("testing get account number")
    a = bank.BankAccount(1234, 20)
    assert a.get_account_number() == 1234
    a = bank.BankAccount(829347, 9128421)
    assert a.get_account_number() == 829347
def test_get_neg_balance():
    print("testing get negative balances")
    a = bank.BankAccount(1234, -20)
    assert a.get_balance() == -20
    a = bank.BankAccount(1312, -91284720918)
    assert a.get_balance() == -91284720918

#functions for testing transfer
def test_valid_transfer():
    print("testing valid transfer")
    a = bank.BankAccount(1234, 30)
    b = bank.BankAccount(5678, 0)
    assert a.transfer(10, b) == True
    assert a.balance == 20
    assert b.balance == 10
    assert b.transfer(5, a) == True
    assert a.balance == 25
    assert b.balance == 5
def test_neg_transfer():
    print("testing negative transfer")
    a = bank.BankAccount(1234, 30)
    b = bank.BankAccount(5678, 0)
    assert a.transfer(-4, b) == False
    assert a.balance == 30
    assert b.balance == 0
def test_zero_transfer():
    print("testing zero transfer")
    a = bank.BankAccount(1234, 30)
    b = bank.BankAccount(5678, 40)
    assert a.transfer(0, b) == False
    assert a.balance == 30
    assert b.balance == 40
def test_over_transfer():
    print("testing over transfer")
    a = bank.BankAccount(1234, 30)
    b = bank.BankAccount(5678, 40)
    assert a.transfer(31, b) == False
    assert a.balance == 30
    assert b.balance == 40
def test_self_transfer():
    print("testing self transfer")
    a = bank.BankAccount(1234, 30)
    assert a.transfer(10, a) == True
    assert a.balance == 30

#testing payroll init
def test_payroll_init():
    print("testing payroll init")
    p = bank.Payroll()
    assert p.accounts == {}

#functions for testing payroll add account
def test_payroll_add():
    print("testing payroll add account")
    p = bank.Payroll()
    a = bank.BankAccount(1234, 30)
    assert p.add_account(a) == True
def test_payroll_add_duplicate_account():
    print("testing payroll add duplicate account")
    p = bank.Payroll()
    a = bank.BankAccount(1234, 30)
    assert p.add_account(a) == True
    assert p.add_account(a) == False
def test_payroll_add_duplicate_account_number():
    print("testing payroll add duplicate account number")
    p = bank.Payroll()
    a = bank.BankAccount(1234, 30)
    b = bank.BankAccount(1234, 9823741)
    assert p.add_account(a) == True
    assert p.add_account(b) == False

#functions testing payroll delete account
def test_payroll_delete_account():
    print("testing payroll delete account")
    p = bank.Payroll()
    a = bank.BankAccount(1234, 30)
    assert p.add_account(a) == True
    assert p.delete_account(a.account_number) == True
def test_payroll_delete_invalid_account():
    print("testing payroll delete non existent account")
    p = bank.Payroll()
    assert p.delete_account(5678) == False

#functions to test pay employee
def test_pay_employee():
    print("testing pay employee")
    p = bank.Payroll()
    a = bank.BankAccount(1234, 30)
    assert p.set_budget(3000000000000) == True
    assert p.add_account(a) == True
    assert p.pay_employee(a, 3, 4) == True
    assert a.balance == 42
def test_pay_invalid_employee():
    print("testing pay non existent employee")
    p = bank.Payroll()
    a = bank.BankAccount(1234, 30)
    assert p.set_budget(3000000000000) == True
    assert p.pay_employee(a, 3, 4) == False
def test_pay_invalid_wage():
    print("testing invalid wage")
    p = bank.Payroll()
    a = bank.BankAccount(1234, 30)
    assert p.set_budget(3000000000000) == True
    assert p.add_account(a) == True
    assert p.pay_employee(a, 0, 4) == False
    assert a.balance == 30
    assert p.pay_employee(a, -13, 4) == False
    assert a.balance == 30
def test_pay_invalid_hours():
    print("testing invalid hours")
    p = bank.Payroll()
    a = bank.BankAccount(1234, 30)
    assert p.set_budget(3000000000000) == True
    assert p.add_account(a) == True
    assert p.pay_employee(a, 13, 0) == False
    assert a.balance == 30
    assert p.pay_employee(a, 13, -12312) == False
    assert a.balance == 30
def test_pay_employee_too_much():
    print("testing pay employee more than budget")
    p = bank.Payroll()
    a = bank.BankAccount(1234, 30)
    assert p.add_account(a) == True
    assert p.set_budget(11) == True
    assert p.pay_employee(a, 3, 4) == False

#functions testing set budget
def test_set_neg_budget():
    print("testing set negative budget")
    p = bank.Payroll()
    assert p.set_budget(-1923482) == False
def test_set_zero_budget():
    print("testing set zero budget")
    p = bank.Payroll()
    assert p.set_budget(0) == True
def test_set_invalid_budget():
    print("testing set not int budget")
    p = bank.Payroll()
    assert p.set_budget("918723") == False


'''def main():
    test_init() #1
    test_pos_deposit() #2
    test_neg_deposit() #3
    test_valid_withdraw() #4
    test_neg_withdraw() #5
    test_over_withdraw() #6
    test_total_withdraw() #7
    test_get_balance() #8
    test_get_account_number() #9
    test_get_neg_balance() #10
    test_zero_withdraw() #11
    test_valid_transfer() #12
    test_neg_transfer() #13
    test_zero_transfer() #14
    test_over_transfer() #15
    test_self_transfer() #16
    test_payroll_init() #17
    test_payroll_add() #18
    test_payroll_add_duplicate_account() #19
    test_payroll_add_duplicate_account_number() #20
    test_payroll_delete_account() #21
    test_payroll_delete_invalid_account() #22
    test_pay_employee() #23
    test_pay_invalid_employee() #24
    test_pay_invalid_wage() #25
    test_pay_invalid_hours() #26
    test_pay_employee_too_much() #27
    test_set_neg_budget() #28
    test_set_zero_budget() #29
    test_set_invalid_budget() #30

if __name__ == "__main__":
    main()'''

#pytest -s -v bank_test.py > bank_test_output.txt