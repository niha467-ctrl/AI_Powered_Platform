"""
-------------------------------------------------------------
FinRelief AI
Story 2: Financial Engine Module
-------------------------------------------------------------
Description:
This module analyzes a borrower's financial profile and
calculates financial health, debt-to-income ratio,
settlement eligibility, and a recommended settlement amount.
-------------------------------------------------------------
"""

from dataclasses import dataclass


# ==========================================================
# Financial Profile
# ==========================================================

@dataclass
class FinancialProfile:
    monthly_income: float
    monthly_expenses: float
    existing_debts: float
    outstanding_loan: float
    interest_rate: float


# ==========================================================
# Financial Engine
# ==========================================================

class FinancialEngine:

    def __init__(self, profile):
        self.profile = profile

    # ------------------------------------------------------
    # Disposable Income
    # ------------------------------------------------------
    def disposable_income(self):
        return (
            self.profile.monthly_income
            - self.profile.monthly_expenses
        )

    # ------------------------------------------------------
    # Debt-to-Income Ratio
    # ------------------------------------------------------
    def debt_to_income_ratio(self):

        if self.profile.monthly_income == 0:
            return 0

        return round(
            (self.profile.existing_debts /
             self.profile.monthly_income) * 100,
            2
        )

    # ------------------------------------------------------
    # EMI Estimation
    # ------------------------------------------------------
    def estimated_emi(self):

        principal = self.profile.outstanding_loan
        annual_rate = self.profile.interest_rate

        monthly_rate = annual_rate / (12 * 100)

        tenure = 36

        if monthly_rate == 0:
            return round(principal / tenure, 2)

        emi = (
            principal
            * monthly_rate
            * ((1 + monthly_rate) ** tenure)
        ) / (
            ((1 + monthly_rate) ** tenure) - 1
        )

        return round(emi, 2)

    # ------------------------------------------------------
    # Affordability
    # ------------------------------------------------------
    def affordability(self):

        disposable = self.disposable_income()
        emi = self.estimated_emi()

        if disposable >= emi:
            return "Affordable"

        return "Financial Stress"

    # ------------------------------------------------------
    # Financial Health Score
    # ------------------------------------------------------
    def health_score(self):

        score = 100

        dti = self.debt_to_income_ratio()

        if dti > 70:
            score -= 40

        elif dti > 50:
            score -= 30

        elif dti > 30:
            score -= 15

        disposable = self.disposable_income()

        if disposable < 5000:
            score -= 25

        elif disposable < 10000:
            score -= 15

        if self.profile.outstanding_loan > 1000000:
            score -= 20

        return max(score, 0)

    # ------------------------------------------------------
    # Settlement Eligibility
    # ------------------------------------------------------
    def settlement_eligibility(self):

        score = self.health_score()

        if score <= 40:
            return "Highly Eligible"

        elif score <= 60:
            return "Eligible"

        elif score <= 80:
            return "Moderate"

        return "Low"

    # ------------------------------------------------------
    # Settlement Recommendation
    # ------------------------------------------------------
    def recommended_settlement(self):

        score = self.health_score()

        if score <= 40:
            percentage = 0.60

        elif score <= 60:
            percentage = 0.70

        elif score <= 80:
            percentage = 0.80

        else:
            percentage = 0.90

        return round(
            self.profile.outstanding_loan * percentage,
            2
        )

    # ------------------------------------------------------
    # Generate Financial Report
    # ------------------------------------------------------
    def generate_report(self):

        report = {
            "Monthly Income": self.profile.monthly_income,
            "Monthly Expenses": self.profile.monthly_expenses,
            "Existing Debts": self.profile.existing_debts,
            "Outstanding Loan": self.profile.outstanding_loan,
            "Disposable Income": self.disposable_income(),
            "Debt-To-Income Ratio (%)": self.debt_to_income_ratio(),
            "Estimated EMI": self.estimated_emi(),
            "Financial Health Score": self.health_score(),
            "Affordability": self.affordability(),
            "Settlement Eligibility": self.settlement_eligibility(),
            "Recommended Settlement":
                self.recommended_settlement()
        }

        return report


# ==========================================================
# Main Program
# ==========================================================

if __name__ == "__main__":

    borrower = FinancialProfile(

        monthly_income=60000,

        monthly_expenses=35000,

        existing_debts=30000,

        outstanding_loan=500000,

        interest_rate=10.5
    )

    engine = FinancialEngine(borrower)

    report = engine.generate_report()

    print("\n")
    print("=" * 60)
    print("FINRELIEF AI FINANCIAL ENGINE REPORT")
    print("=" * 60)

    for key, value in report.items():
        print(f"{key:30}: {value}")

    print("=" * 60)