# LOAN & SETTLEMENT PROCESSING SYSTEM (SINGLE FILE)

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid
import time
import math


# -----------------------------
# DATA MODELS
# -----------------------------

@dataclass
class Payment:
    amount: float
    timestamp: float


@dataclass
class Loan:
    loan_id: str
    principal: float
    interest_rate: float  # annual %
    tenure_months: int
    emi: float
    outstanding: float
    payments: List[Payment] = field(default_factory=list)
    status: str = "ACTIVE"  # ACTIVE, CLOSED, DEFAULTED
    created_at: float = field(default_factory=time.time)


# -----------------------------
# CORE ENGINE
# -----------------------------

class LoanEngine:
    def __init__(self):
        self.loans: Dict[str, Loan] = {}

    # -------------------------
    # EMI CALCULATION
    # -------------------------
    def calculate_emi(self, principal, rate, months):
        monthly_rate = rate / (12 * 100)

        if monthly_rate == 0:
            return principal / months

        emi = (
            principal * monthly_rate * math.pow(1 + monthly_rate, months)
        ) / (math.pow(1 + monthly_rate, months) - 1)

        return round(emi, 2)

    # -------------------------
    # CREATE LOAN
    # -------------------------
    def create_loan(self, principal: float, interest_rate: float, tenure_months: int):
        loan_id = str(uuid.uuid4())

        emi = self.calculate_emi(principal, interest_rate, tenure_months)

        loan = Loan(
            loan_id=loan_id,
            principal=principal,
            interest_rate=interest_rate,
            tenure_months=tenure_months,
            emi=emi,
            outstanding=principal
        )

        self.loans[loan_id] = loan
        return loan

    # -------------------------
    # MAKE PAYMENT
    # -------------------------
    def make_payment(self, loan_id: str, amount: float):
        if loan_id not in self.loans:
            return {"error": "Loan not found"}

        loan = self.loans[loan_id]

        if loan.status != "ACTIVE":
            return {"error": "Loan not active"}

        loan.outstanding -= amount
        loan.payments.append(Payment(amount=amount, timestamp=time.time()))

        if loan.outstanding <= 0:
            loan.status = "CLOSED"
            loan.outstanding = 0

        return {
            "loan_id": loan_id,
            "paid": amount,
            "remaining": loan.outstanding,
            "status": loan.status
        }

    # -------------------------
    # SETTLEMENT OFFER ENGINE
    # -------------------------
    def settlement_offer(self, loan_id: str):
        loan = self.loans.get(loan_id)

        if not loan:
            return {"error": "Loan not found"}

        if loan.status != "ACTIVE":
            return {"error": "Loan not eligible for settlement"}

        paid_ratio = 1 - (loan.outstanding / loan.principal)

        # Discount logic based on repayment behavior
        if paid_ratio > 0.7:
            discount = 0.4
        elif paid_ratio > 0.4:
            discount = 0.25
        else:
            discount = 0.1

        settlement_amount = loan.outstanding * (1 - discount)

        return {
            "loan_id": loan_id,
            "outstanding": loan.outstanding,
            "discount_percent": discount * 100,
            "settlement_amount": round(settlement_amount, 2)
        }

    # -------------------------
    # CLOSE SETTLEMENT
    # -------------------------
    def close_settlement(self, loan_id: str, amount: float):
        loan = self.loans.get(loan_id)

        if not loan:
            return {"error": "Loan not found"}

        offer = self.settlement_offer(loan_id)

        if "error" in offer:
            return offer

        if amount >= offer["settlement_amount"]:
            loan.status = "CLOSED"
            loan.outstanding = 0
            return {
                "message": "Loan settled successfully",
                "paid": amount
            }

        return {
            "message": "Settlement rejected (insufficient amount)",
            "required": offer["settlement_amount"]
        }

    # -------------------------
    # DEFAULT CHECK
    # -------------------------
    def check_default(self, loan_id: str, missed_emis: int):
        loan = self.loans.get(loan_id)

        if not loan:
            return {"error": "Loan not found"}

        if missed_emis >= 3:
            loan.status = "DEFAULTED"
            return {"loan_id": loan_id, "status": "DEFAULTED"}

        return {"loan_id": loan_id, "status": "ACTIVE"}

    # -------------------------
    # GET LOAN DETAILS
    # -------------------------
    def get_loan(self, loan_id: str):
        return self.loans.get(loan_id, {"error": "Loan not found"})


# -----------------------------
# EXAMPLE USAGE
# -----------------------------

if __name__ == "__main__":
    engine = LoanEngine()

    # Create loan
    loan = engine.create_loan(principal=100000, interest_rate=12, tenure_months=24)
    print("Created Loan:", loan.loan_id)

    # Make payments
    print(engine.make_payment(loan.loan_id, 20000))
    print(engine.make_payment(loan.loan_id, 15000))

    # Settlement offer
    print(engine.settlement_offer(loan.loan_id))

    # Close settlement
    print(engine.close_settlement(loan.loan_id, 70000))

    # Loan status
    print(engine.get_loan(loan.loan_id))