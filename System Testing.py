"""
=========================================================
SYSTEM TESTING FRAMEWORK (Single File)
=========================================================
Features:
✔ Unit Testing
✔ Integration Testing
✔ Functional Testing
✔ Performance Testing
✔ API Testing
✔ Database Testing
✔ Exception Handling Testing
✔ Test Reporting
✔ Summary Statistics

Run:
    python system_testing.py
=========================================================
"""

import unittest
import time
import sqlite3
import json
from dataclasses import dataclass

# =====================================================
# SAMPLE APPLICATION
# =====================================================

class FinancialSystem:

    def __init__(self):
        self.accounts = {}

    def create_account(self, account_id, balance):
        if account_id in self.accounts:
            raise ValueError("Account already exists")

        self.accounts[account_id] = balance
        return True

    def deposit(self, account_id, amount):
        if amount <= 0:
            raise ValueError("Invalid amount")

        self.accounts[account_id] += amount
        return self.accounts[account_id]

    def withdraw(self, account_id, amount):
        if amount > self.accounts[account_id]:
            raise ValueError("Insufficient balance")

        self.accounts[account_id] -= amount
        return self.accounts[account_id]

    def transfer(self, sender, receiver, amount):

        self.withdraw(sender, amount)
        self.deposit(receiver, amount)

        return True

    def settlement(self, outstanding, discount):

        settlement_amount = outstanding - (outstanding * discount / 100)

        return round(settlement_amount,2)


# =====================================================
# DATABASE
# =====================================================

class Database:

    def __init__(self):

        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE customer(
            id INTEGER PRIMARY KEY,
            name TEXT,
            balance REAL
        )
        """)

    def insert(self,name,balance):

        self.cursor.execute(
            "INSERT INTO customer(name,balance) VALUES(?,?)",
            (name,balance)
        )

        self.conn.commit()

    def count(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM customer"
        )

        return self.cursor.fetchone()[0]


# =====================================================
# MOCK API
# =====================================================

def api_health():

    return {
        "status":"success",
        "code":200
    }


# =====================================================
# TEST REPORT
# =====================================================

@dataclass
class TestResultSummary:

    total:int=0
    passed:int=0
    failed:int=0


summary = TestResultSummary()


# =====================================================
# UNIT TESTS
# =====================================================

class TestUnit(unittest.TestCase):

    def setUp(self):

        self.bank = FinancialSystem()

        self.bank.create_account("A",10000)
        self.bank.create_account("B",5000)

    def test_create(self):

        self.assertEqual(
            self.bank.accounts["A"],
            10000
        )

    def test_deposit(self):

        balance = self.bank.deposit("A",2000)

        self.assertEqual(balance,12000)

    def test_withdraw(self):

        balance = self.bank.withdraw("A",3000)

        self.assertEqual(balance,7000)

    def test_settlement(self):

        amount = self.bank.settlement(100000,20)

        self.assertEqual(amount,80000)


# =====================================================
# INTEGRATION TEST
# =====================================================

class TestIntegration(unittest.TestCase):

    def setUp(self):

        self.bank = FinancialSystem()

        self.bank.create_account("A",10000)
        self.bank.create_account("B",5000)

    def test_transfer(self):

        self.bank.transfer("A","B",2000)

        self.assertEqual(
            self.bank.accounts["A"],
            8000
        )

        self.assertEqual(
            self.bank.accounts["B"],
            7000
        )


# =====================================================
# DATABASE TEST
# =====================================================

class TestDatabase(unittest.TestCase):

    def test_database(self):

        db = Database()

        db.insert("John",50000)
        db.insert("Alice",60000)

        self.assertEqual(
            db.count(),
            2
        )


# =====================================================
# API TEST
# =====================================================

class TestAPI(unittest.TestCase):

    def test_api(self):

        response = api_health()

        self.assertEqual(
            response["status"],
            "success"
        )

        self.assertEqual(
            response["code"],
            200
        )


# =====================================================
# PERFORMANCE TEST
# =====================================================

class TestPerformance(unittest.TestCase):

    def test_speed(self):

        start = time.time()

        total = 0

        for i in range(100000):

            total += i

        elapsed = time.time() - start

        self.assertLess(elapsed,1.0)


# =====================================================
# EXCEPTION TEST
# =====================================================

class TestException(unittest.TestCase):

    def setUp(self):

        self.bank = FinancialSystem()

        self.bank.create_account("A",5000)

    def test_exception(self):

        with self.assertRaises(ValueError):

            self.bank.withdraw("A",6000)


# =====================================================
# FUNCTIONAL TEST
# =====================================================

class TestFunctional(unittest.TestCase):

    def test_complete_workflow(self):

        bank = FinancialSystem()

        bank.create_account("C1",100000)
        bank.deposit("C1",5000)

        amount = bank.settlement(
            50000,
            25
        )

        self.assertEqual(
            amount,
            37500
        )


# =====================================================
# CUSTOM TEST RUNNER
# =====================================================

if __name__ == "__main__":

    loader = unittest.TestLoader()

    suite = loader.loadTestsFromModule(__import__(__name__))

    runner = unittest.TextTestRunner(verbosity=2)

    start = time.time()

    result = runner.run(suite)

    end = time.time()

    summary.total = result.testsRun
    summary.failed = len(result.failures) + len(result.errors)
    summary.passed = summary.total - summary.failed

    report = {
        "Total Tests": summary.total,
        "Passed": summary.passed,
        "Failed": summary.failed,
        "Execution Time (sec)": round(end-start,3),
        "Success Rate (%)":
            round(summary.passed/summary.total*100,2)
            if summary.total else 0
    }

    print("\n")
    print("="*60)
    print("SYSTEM TEST REPORT")
    print("="*60)

    print(json.dumps(report,indent=4))

    print("="*60)