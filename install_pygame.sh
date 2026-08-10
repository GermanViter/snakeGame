#!/usr/bin/env bash
set -e

if command -v python3 &>/dev/null; then
    echo "Python3 is already installed ($(python3 --version))."
else
    echo "Python3 is not installed. Attempting to install Python3..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y python3 python3-pip
    elif command -v pacman &>/dev/null; then
        sudo pacman -Sy --noconfirm python3 python-pip
    elif command -v brew &>/dev/null; then
        brew install python
    else
        echo "Error: Supported package manager (apt-get, dnf, pacman, brew) not found."
        echo "Please install Python 3 manually."
        exit 1
    fi
fi

HOME_DIR=""
if [[ $(uname) == "Darwin" ]]; then
    "$HOME_DIR"="/Users/$(whoami)"
elif [[ $(uname) == "Linux" ]]; then
    "$HOME_DIR"="/home/$(whoami)"
fi

if [[ ! -f "$HOME_DIR"/venv ]]; then
    echo "Creating virtual environment at ~/venv..."
    python3 -m venv "$HOME_DIR"/venv
fi

echo "Activating virtual environment and installing Pygame..."
source ~/venv/bin/activate
pip install --upgrade pip
pip install pygame-ce
chmod +x ./snake.py

echo "Installation finished successfully!"
