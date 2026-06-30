"""
-------------------------------------------------------
FinRelief AI
Story 2 : Backend Dependency Installation
-------------------------------------------------------
Description:
Installs all backend dependencies listed in
requirements.txt.
-------------------------------------------------------
"""

import subprocess
import sys
import os


def check_requirements():

    if not os.path.exists("requirements.txt"):
        print("Error: requirements.txt not found.")
        return False

    print("requirements.txt found.")
    return True


def install_dependencies():

    print("\nInstalling Backend Dependencies...\n")

    try:

        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip"
        ])

        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            "requirements.txt"
        ])

        print("\nAll dependencies installed successfully.")

    except subprocess.CalledProcessError:

        print("\nInstallation failed.")


def display_installed_packages():

    print("\nInstalled Packages\n")

    subprocess.call([
        sys.executable,
        "-m",
        "pip",
        "list"
    ])


def main():

    print("=" * 55)
    print("FinRelief AI Backend Dependency Installer")
    print("=" * 55)

    if check_requirements():
        install_dependencies()
        display_installed_packages()

    print("\nSetup Completed.")


if __name__ == "__main__":
    main()