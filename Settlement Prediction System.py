"""
---------------------------------------------------------------
FinRelief AI
Story 3: Settlement Prediction System
---------------------------------------------------------------
Description:
This module predicts a loan settlement amount based on a
borrower's financial condition. It evaluates financial
health, debt burden, repayment capacity, and assigns a
settlement probability, recommended settlement amount,
priority level, and negotiation strategy.
---------------------------------------------------------------
"""

from dataclasses import dataclass


# ==========================================================
# Borrower Financial Information
# ==========================================================

@dataclass
class Borrower:

    user_id: int
    name: str

    monthly_income: float
    monthly_expenses: float
    existing_debts: float

    loan_amount: float
    outstanding_amount: float

    interest_rate: float


# ==========================================================
# Settlement Prediction Engine
# ==========================================================

class SettlementPredictionSystem:

    def __init__(self, borrower):
        self.borrower = borrower

    # ------------------------------------------------------
    # Disposable Income
    # ------------------------------------------------------

    def disposable_income(self):

        return (
            self.borrower.monthly_income -
            self.borrower.monthly_expenses
        )

    # ------------------------------------------------------
    # Debt-To-Income Ratio
    # ------------------------------------------------------

    def debt_to_income_ratio(self):

        if self.borrower.monthly_income == 0:
            return 0

        ratio = (
            self.borrower.existing_debts /
            self.borrower.monthly_income
        ) * 100

        return round(ratio, 2)

    # ------------------------------------------------------
    # Financial Health Score
    # ------------------------------------------------------

    def financial_health_score(self):

        score = 100

        dti = self.debt_to_income_ratio()

        disposable = self.disposable_income()

        if dti > 70:
            score -= 35

        elif dti > 50:
            score -= 25

        elif dti > 30:
            score -= 15

        if disposable < 5000:
            score -= 30

        elif disposable < 10000:
            score -= 20

        elif disposable < 20000:
            score -= 10

        if self.borrower.outstanding_amount > 1000000:
            score -= 20

        return max(score, 0)

    # ------------------------------------------------------
    # Settlement Probability
    # ------------------------------------------------------

    def settlement_probability(self):

        score = self.financial_health_score()

        if score <= 30:
            return 95

        elif score <= 50:
            return 85

        elif score <= 70:
            return 70

        elif score <= 85:
            return 55

        return 35

    # ------------------------------------------------------
    # Recommended Settlement Amount
    # ------------------------------------------------------

    def recommended_amount(self):

        probability = self.settlement_probability()

        if probability >= 90:
            percentage = 0.60

        elif probability >= 80:
            percentage = 0.65

        elif probability >= 70:
            percentage = 0.75

        elif probability >= 50:
            percentage = 0.85

        else:
            percentage = 0.95

        return round(
            self.borrower.outstanding_amount * percentage,
            2
        )

    # ------------------------------------------------------
    # Priority Level
    # ------------------------------------------------------

    def priority_level(self):

        probability = self.settlement_probability()

        if probability >= 90:
            return "Very High"

        elif probability >= 80:
            return "High"

        elif probability >= 70:
            return "Medium"

        return "Low"

    # ------------------------------------------------------
    # Negotiation Strategy
    # ------------------------------------------------------

    def negotiation_strategy(self):

        probability = self.settlement_probability()

        if probability >= 90:
            return (
                "Offer immediate settlement with significant "
                "interest waiver and flexible payment terms."
            )

        elif probability >= 80:
            return (
                "Negotiate reduced outstanding balance and "
                "extend repayment schedule."
            )

        elif probability >= 70:
            return (
                "Offer partial settlement with structured "
                "monthly installments."
            )

        else:
            return (
                "Encourage regular repayment while monitoring "
                "financial stability."
            )

    # ------------------------------------------------------
    # Generate Settlement Report
    # ------------------------------------------------------

    def generate_report(self):

        return {

            "User ID": self.borrower.user_id,

            "Borrower": self.borrower.name,

            "Loan Amount": self.borrower.loan_amount,

            "Outstanding Amount": self.borrower.outstanding_amount,

            "Monthly Income": self.borrower.monthly_income,

            "Disposable Income": self.disposable_income(),

            "Debt-To-Income Ratio (%)":
                self.debt_to_income_ratio(),

            "Financial Health Score":
                self.financial_health_score(),

            "Settlement Probability (%)":
                self.settlement_probability(),

            "Recommended Settlement Amount":
                self.recommended_amount(),

            "Priority Level":
                self.priority_level(),

            "Negotiation Strategy":
                self.negotiation_strategy()

        }


# ==========================================================
# Main Program
# ==========================================================

if __name__ == "__main__":

    borrower = Borrower(

        user_id=101,

        name="John Smith",

        monthly_income=50000,

        monthly_expenses=36000,

        existing_debts=45000,

        loan_amount=800000,

        outstanding_amount=620000,

        interest_rate=10.25

    )

    predictor = SettlementPredictionSystem(borrower)

    report = predictor.generate_report()

    print("\n")
    print("=" * 70)
    print("        FINRELIEF AI SETTLEMENT PREDICTION REPORT")
    print("=" * 70)

    for key, value in report.items():
        print(f"{key:35}: {value}")

    print("=" * 70)