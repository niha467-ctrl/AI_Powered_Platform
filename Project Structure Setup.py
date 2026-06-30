"""
--------------------------------------------------------------
FinRelief AI
Story 4: Project Structure Setup
--------------------------------------------------------------
Description:
Creates the complete project directory structure for the
FinRelief AI full-stack application.
--------------------------------------------------------------
"""

import os

# ===============================
# Project Name
# ===============================
PROJECT_NAME = "FinReliefAI"

# ===============================
# Folder Structure
# ===============================
folders = [

    # Backend
    "backend",
    "backend/app",
    "backend/app/api",
    "backend/app/models",
    "backend/app/services",
    "backend/app/database",
    "backend/app/core",
    "backend/app/schemas",
    "backend/app/utils",
    "backend/tests",

    # Frontend
    "frontend",
    "frontend/public",
    "frontend/src",
    "frontend/src/assets",
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/src/services",
    "frontend/src/styles",

    # Documentation
    "docs",

    # Deployment
    "deployment",

    # GitHub
    ".github",
    ".github/workflows"
]

# ===============================
# Files to Create
# ===============================
files = {

    "README.md":
"# FinRelief AI\n\nAI-Powered Loan Settlement Platform",

    ".gitignore":
"""venv/
node_modules/
__pycache__/
.env
*.pyc
""",

    "requirements.txt":
"""fastapi
uvicorn
sqlalchemy
pydantic
python-dotenv
requests
openai
numpy
pandas
""",

    "backend/app/main.py":
'''from fastapi import FastAPI

app = FastAPI(title="FinRelief AI")

@app.get("/")
def home():
    return {"message":"FinRelief AI Backend Running"}
''',

    "backend/app/__init__.py": "",

    "backend/app/api/__init__.py": "",

    "backend/app/models/__init__.py": "",

    "backend/app/services/__init__.py": "",

    "backend/app/database/__init__.py": "",

    "backend/app/core/__init__.py": "",

    "backend/app/schemas/__init__.py": "",

    "backend/app/utils/__init__.py": "",

    "frontend/src/App.jsx":
'''function App(){

    return(
        <h1>FinRelief AI Frontend</h1>
    );

}

export default App;
''',

    "frontend/src/main.jsx":
'''import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

ReactDOM.createRoot(
document.getElementById("root")
).render(<App />);
''',

    "frontend/src/styles/App.css": "",

    "frontend/src/services/api.js":
'''export const API_URL="http://localhost:8000";
'''
}

# ===============================
# Create Project
# ===============================
print("=" * 60)
print("Creating FinRelief AI Project Structure")
print("=" * 60)

os.makedirs(PROJECT_NAME, exist_ok=True)

os.chdir(PROJECT_NAME)

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Created Folder : {folder}")

# Create files
for file_name, content in files.items():

    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Created File   : {file_name}")

print("\n" + "=" * 60)
print("Project Structure Created Successfully")
print("=" * 60)

print("""

Project Structure

FinReliefAI/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── database/
│   │   ├── schemas/
│   │   ├── core/
│   │   ├── utils/
│   │   ├── main.py
│   │   └── __init__.py
│   └── tests/
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── assets/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── styles/
│       ├── App.jsx
│       └── main.jsx
│
├── docs/
├── deployment/
├── .github/
│   └── workflows/
│
├── requirements.txt
├── README.md
└── .gitignore

""")