# Financial Health Metrics & Settlement Data Visualization (Single File)

import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List
import random

# -----------------------------
# DATA MODEL
# -----------------------------

@dataclass
class Customer:
    customer_id: int
    monthly_income: float
    monthly_expenses: float
    total_debt: float
    outstanding_loan: float
    settlement_amount: float
    credit_score: int


# -----------------------------
# FINANCIAL ANALYTICS ENGINE
# -----------------------------

class FinancialAnalytics:

    def __init__(self):
        self.customers: List[Customer] = []

    # -------------------------
    # Generate Sample Data
    # -------------------------
    def generate_data(self, n=20):
        for i in range(1, n + 1):
            income = random.randint(30000, 120000)
            expenses = random.randint(15000, 70000)
            debt = random.randint(50000, 600000)
            outstanding = random.randint(10000, debt)
            settlement = outstanding * random.uniform(0.55, 0.90)
            credit = random.randint(550, 850)

            self.customers.append(
                Customer(
                    i,
                    income,
                    expenses,
                    debt,
                    outstanding,
                    settlement,
                    credit,
                )
            )

    # -------------------------
    # Financial Health Score
    # -------------------------
    def health_score(self, customer):

        savings = customer.monthly_income - customer.monthly_expenses

        debt_ratio = customer.total_debt / customer.monthly_income

        score = (
            savings * 0.4 +
            customer.credit_score * 2 -
            debt_ratio * 100
        )

        return round(max(0, min(score, 100)), 2)

    # -------------------------
    # Display Metrics
    # -------------------------
    def show_metrics(self):

        print("=" * 70)
        print("Financial Health Report")
        print("=" * 70)

        for c in self.customers:

            score = self.health_score(c)

            print(f"""
Customer ID        : {c.customer_id}
Income             : ₹{c.monthly_income}
Expenses           : ₹{c.monthly_expenses}
Debt               : ₹{c.total_debt}
Outstanding Loan   : ₹{c.outstanding_loan}
Settlement Amount  : ₹{round(c.settlement_amount,2)}
Credit Score       : {c.credit_score}
Health Score       : {score}
""")

    # -------------------------
    # Visualization
    # -------------------------
    def visualize(self):

        ids = [c.customer_id for c in self.customers]

        health = [self.health_score(c) for c in self.customers]

        settlement = [c.settlement_amount for c in self.customers]

        outstanding = [c.outstanding_loan for c in self.customers]

        income = [c.monthly_income for c in self.customers]

        # -------------------------
        # Health Score
        # -------------------------
        plt.figure(figsize=(10,5))
        plt.bar(ids, health)
        plt.title("Customer Financial Health Score")
        plt.xlabel("Customer ID")
        plt.ylabel("Health Score")
        plt.grid(True)
        plt.show()

        # -------------------------
        # Outstanding vs Settlement
        # -------------------------
        plt.figure(figsize=(10,5))
        plt.plot(ids, outstanding, marker='o', label="Outstanding")
        plt.plot(ids, settlement, marker='s', label="Settlement")
        plt.title("Outstanding Loan vs Settlement Amount")
        plt.xlabel("Customer ID")
        plt.ylabel("Amount (₹)")
        plt.legend()
        plt.grid(True)
        plt.show()

        # -------------------------
        # Income Distribution
        # -------------------------
        plt.figure(figsize=(8,8))
        plt.pie(
            income,
            labels=[f"C{i}" for i in ids],
            autopct="%1.1f%%",
            startangle=90
        )
        plt.title("Income Distribution")
        plt.show()

        # -------------------------
        # Scatter Plot
        # -------------------------
        plt.figure(figsize=(8,5))
        plt.scatter(outstanding, settlement)
        plt.title("Outstanding Loan vs Settlement")
        plt.xlabel("Outstanding Loan")
        plt.ylabel("Settlement Amount")
        plt.grid(True)
        plt.show()


# -----------------------------
# MAIN PROGRAM
# -----------------------------

if __name__ == "__main__":

    engine = FinancialAnalytics()

    engine.generate_data(20)

    engine.show_metrics()

    engine.visualize()