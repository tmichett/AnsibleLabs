#!/bin/bash
# Script to set up and use Ansible in a virtual environment

set -e

cd /Users/travis/Github/AnsibleLabs

echo "Setting up Ansible virtual environment..."
echo "=========================================="

# Create virtual environment if it doesn't exist
if [ ! -d "ansible-env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv ansible-env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source ansible-env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Ansible and dependencies
echo "Installing Ansible and dependencies..."
pip install --upgrade --force-reinstall ansible-core cryptography cffi

# Verify installation
echo ""
echo "Verifying installation..."
echo "Python version: $(python --version)"
echo "Ansible version: $(python -m ansible --version 2>&1 | head -1)"
echo "Ansible location: $(which ansible || echo 'Using: python -m ansible')"

echo ""
echo "=========================================="
echo "Virtual environment is ready!"
echo ""
echo "To use Ansible, activate the environment first:"
echo "  source ansible-env/bin/activate"
echo ""
echo "Then use one of these commands:"
echo "  ansible --version"
echo "  python -m ansible all -m info_ping"
echo "  ANSIBLE_LIBRARY=./library python -m ansible localhost -m info_ping"
echo ""
