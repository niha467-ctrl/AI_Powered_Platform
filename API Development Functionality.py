# FASTAPI FULL API DEVELOPMENT FUNCTIONALITY (SINGLE FILE)

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import uuid
import time

app = FastAPI(title="API Development Engine", version="1.0")


# -----------------------------
# In-Memory Database
# -----------------------------
DB: Dict[str, Dict] = {}
USERS = {
    "admin_token": {"role": "admin"},
    "user_token": {"role": "user"}
}


# -----------------------------
# Models
# -----------------------------
class Item(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)
    description: Optional[str] = None


class ItemResponse(Item):
    id: str
    created_at: float


# -----------------------------
# Auth Dependency
# -----------------------------
def authenticate(token: str = Header(None)):
    if not token or token not in USERS:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return USERS[token]


# -----------------------------
# Utility Functions
# -----------------------------
def get_item_or_404(item_id: str):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item not found")
    return DB[item_id]


# -----------------------------
# CRUD APIs
# -----------------------------

@app.post("/items", response_model=ItemResponse)
def create_item(item: Item, user=Depends(authenticate)):
    item_id = str(uuid.uuid4())

    DB[item_id] = {
        "id": item_id,
        "name": item.name,
        "price": item.price,
        "description": item.description,
        "created_at": time.time()
    }

    return DB[item_id]


@app.get("/items", response_model=List[ItemResponse])
def list_items(user=Depends(authenticate)):
    return list(DB.values())


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: str, user=Depends(authenticate)):
    return get_item_or_404(item_id)


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: str, item: Item, user=Depends(authenticate)):
    existing = get_item_or_404(item_id)

    existing.update({
        "name": item.name,
        "price": item.price,
        "description": item.description
    })

    return existing


@app.delete("/items/{item_id}")
def delete_item(item_id: str, user=Depends(authenticate)):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item not found")

    del DB[item_id]
    return {"message": "Deleted successfully"}


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "timestamp": time.time(),
        "items_count": len(DB)
    }


# -----------------------------
# Error Handler Example
# -----------------------------
@app.exception_handler(HTTPException)
def custom_http_exception_handler(request, exc):
    return {
        "error": True,
        "status_code": exc.status_code,
        "message": exc.detail,
        "path": str(request.url)
    }


# -----------------------------
# Run:
# uvicorn filename:app --reload
# -----------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)