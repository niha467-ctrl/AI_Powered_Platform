# FULL STACK: FASTAPI + FRONTEND (SINGLE FILE)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
import time

app = FastAPI(title="Full Stack UI + API System")

# -----------------------------
# CORS (for frontend communication)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# DATABASE (in-memory)
# -----------------------------
DB = []


# -----------------------------
# DATA MODEL
# -----------------------------
class Item(BaseModel):
    name: str


# -----------------------------
# API ROUTES
# -----------------------------

@app.get("/api/items")
def get_items():
    return DB


@app.post("/api/items")
def add_item(item: Item):
    record = {
        "id": str(uuid.uuid4()),
        "name": item.name,
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    DB.append(record)
    return {"message": "Item added", "data": record}


@app.delete("/api/items/{item_id}")
def delete_item(item_id: str):
    global DB
    DB = [x for x in DB if x["id"] != item_id]
    return {"message": "Item deleted"}


# -----------------------------
# FRONTEND (HTML + JS)
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def frontend():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI + Frontend</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input, button { padding: 10px; margin: 5px; }
        .card { padding: 10px; margin: 5px; border: 1px solid #ccc; }
    </style>
</head>

<body>

<h2>Full Stack Frontend ↔ FastAPI</h2>

<input id="name" placeholder="Enter name" />
<button onclick="addItem()">Add</button>
<button onclick="loadItems()">Refresh</button>

<div id="list"></div>

<script>

const API = "/api/items";

// ----------------------
// LOAD ITEMS
// ----------------------
async function loadItems() {
    const res = await fetch(API);
    const data = await res.json();

    const list = document.getElementById("list");
    list.innerHTML = "";

    data.forEach(item => {
        const div = document.createElement("div");
        div.className = "card";
        div.innerHTML = `
            <b>${item.name}</b><br/>
            ${item.time}<br/>
            <button onclick="deleteItem('${item.id}')">Delete</button>
        `;
        list.appendChild(div);
    });
}

// ----------------------
// ADD ITEM
// ----------------------
async function addItem() {
    const name = document.getElementById("name").value;

    await fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    });

    document.getElementById("name").value = "";
    loadItems();
}

// ----------------------
// DELETE ITEM
// ----------------------
async function deleteItem(id) {
    await fetch(`${API}/${id}`, {
        method: "DELETE"
    });

    loadItems();
}

// Initial load
loadItems();

</script>

</body>
</html>
"""


# -----------------------------
# RUN:
# uvicorn filename:app --reload
# -----------------------------