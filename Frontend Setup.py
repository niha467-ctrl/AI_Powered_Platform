"""
------------------------------------------------------------
FinRelief AI
Story 3: Frontend Setup (React.js + Vite)
------------------------------------------------------------
Description:
This Python script automates the setup of the React.js
frontend using Vite. It creates the project, installs
required dependencies, and generates a basic folder
structure and starter files.
------------------------------------------------------------
"""

import os
import subprocess
from pathlib import Path


PROJECT_NAME = "frontend"

DEPENDENCIES = [
    "react-router-dom",
    "axios",
    "bootstrap",
    "react-icons",
    "recharts",
    "react-toastify"
]


def run_command(command):
    """Run a shell command."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"Error while executing: {' '.join(command)}")


def create_vite_project():
    print("\nCreating React + Vite Project...\n")

    run_command([
        "npm",
        "create",
        "vite@latest",
        PROJECT_NAME,
        "--",
        "--template",
        "react"
    ])


def install_dependencies():
    print("\nInstalling Dependencies...\n")

    os.chdir(PROJECT_NAME)

    run_command(["npm", "install"])

    for package in DEPENDENCIES:
        print(f"Installing {package}")
        run_command(["npm", "install", package])


def create_folders():

    folders = [
        "src/components",
        "src/pages",
        "src/services",
        "src/styles",
        "src/assets"
    ]

    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)

    print("Project folders created.")


def create_api():

    api = """import axios from 'axios';

const api = axios.create({
    baseURL: "http://localhost:8000"
});

export default api;
"""

    with open("src/services/api.js", "w") as f:
        f.write(api)


def create_home():

    home = """function Home(){

    return(
        <div style={{padding:'30px'}}>
            <h1>FinRelief AI</h1>
            <p>AI Powered Loan Settlement Platform</p>
        </div>
    );

}

export default Home;
"""

    with open("src/pages/Home.jsx", "w") as f:
        f.write(home)


def create_app():

    app = """import Home from "./pages/Home";

function App(){

    return(
        <Home/>
    );

}

export default App;
"""

    with open("src/App.jsx", "w") as f:
        f.write(app)


def create_main():

    main = """import React from 'react';
import ReactDOM from 'react-dom/client';

import App from './App';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-toastify/dist/ReactToastify.css';

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App/>
    </React.StrictMode>
);
"""

    with open("src/main.jsx", "w") as f:
        f.write(main)


def display_summary():

    print("\n")
    print("=" * 60)
    print("Frontend Setup Completed Successfully")
    print("=" * 60)

    print("""
Project Created : frontend/

Installed Packages:
✔ React
✔ Vite
✔ React Router
✔ Axios
✔ Bootstrap
✔ React Icons
✔ Recharts
✔ React Toastify

Run the application using:

cd frontend
npm run dev

Open:
http://localhost:5173
""")


def main():

    print("=" * 60)
    print("FinRelief AI Frontend Setup")
    print("=" * 60)

    create_vite_project()

    install_dependencies()

    create_folders()

    create_api()

    create_home()

    create_app()

    create_main()

    display_summary()


if __name__ == "__main__":
    main()