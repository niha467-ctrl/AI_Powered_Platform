"""
---------------------------------------------------------
FinRelief AI
Story 1: FastAPI Backend & API Endpoints
---------------------------------------------------------
Description:
This FastAPI application provides REST API endpoints for
user management, loan management, financial profiles,
settlement prediction, and AI negotiation.
---------------------------------------------------------
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(
    title="FinRelief AI API",
    version="1.0.0",
    description="AI-Powered Loan Settlement Platform"
)

# -------------------------
# In-Memory Storage
# -------------------------
users = {}
loans = {}
profiles = {}
settlements = []
ai_history = []

# -------------------------
# Models
# -------------------------

class User(BaseModel):
    user_id: int
    name: str
    email: str
    password: str

class Loan(BaseModel):
    loan_id: int
    user_id: int
    loan_type: str
    loan_amount: float
    outstanding_amount: float
    interest_rate: float
    due_date: str

class FinancialProfile(BaseModel):
    profile_id: int
    user_id: int
    monthly_income: float
    monthly_expenses: float
    existing_debts: float

class SettlementRequest(BaseModel):
    loan_id: int
    user_id: int

# -------------------------
# Home Endpoint
# -------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to FinRelief AI Backend",
        "status": "Running"
    }

# -------------------------
# User APIs
# -------------------------

@app.post("/users")
def register_user(user: User):

    if user.user_id in users:
        raise HTTPException(status_code=400, detail="User already exists")

    users[user.user_id] = user

    return {
        "message": "User Registered Successfully",
        "user": user
    }


@app.get("/users")
def get_users():
    return list(users.values())


# -------------------------
# Loan APIs
# -------------------------

@app.post("/loans")
def add_loan(loan: Loan):

    if loan.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    loans[loan.loan_id] = loan

    return {
        "message": "Loan Added Successfully",
        "loan": loan
    }


@app.get("/loans")
def get_loans():
    return list(loans.values())


# -------------------------
# Financial Profile APIs
# -------------------------

@app.post("/financial-profile")
def create_profile(profile: FinancialProfile):

    if profile.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    profiles[profile.user_id] = profile

    return {
        "message": "Financial Profile Saved",
        "profile": profile
    }


@app.get("/financial-profile/{user_id}")
def get_profile(user_id: int):

    if user_id not in profiles:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profiles[user_id]


# -------------------------
# Settlement Prediction API
# -------------------------

@app.post("/predict-settlement")
def settlement_prediction(data: SettlementRequest):

    if data.loan_id not in loans:
        raise HTTPException(status_code=404, detail="Loan not found")

    loan = loans[data.loan_id]

    prediction = round(
        loan.outstanding_amount * 0.75,
        2
    )

    result = {
        "settlement_id": len(settlements) + 1,
        "user_id": data.user_id,
        "loan_id": data.loan_id,
        "recommended_amount": prediction,
        "priority": "High",
        "created_at": str(datetime.now())
    }

    settlements.append(result)

    return result


# -------------------------
# AI Negotiation Endpoint
# -------------------------

@app.post("/ai-negotiation")
def ai_negotiation(data: SettlementRequest):

    strategy = f"""
    Based on loan {data.loan_id},
    offer a settlement of approximately 75%
    of the outstanding amount while requesting
    interest waiver and flexible payment terms.
    """

    history = {
        "history_id": len(ai_history) + 1,
        "user_id": data.user_id,
        "loan_id": data.loan_id,
        "strategy": strategy,
        "generated_at": str(datetime.now())
    }

    ai_history.append(history)

    return history


@app.get("/ai-history")
def get_ai_history():
    return ai_history


# -------------------------
# Health Check
# -------------------------

@app.get("/health")
def health():

    return {
        "Application": "FinRelief AI",
        "Backend": "FastAPI",
        "Status": "Healthy",
        "Timestamp": str(datetime.now())
    }


# -------------------------
# Run Application
# -------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )