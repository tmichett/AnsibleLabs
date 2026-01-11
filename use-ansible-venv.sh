#!/bin/bash
# Helper script to use Ansible from virtual environment

cd /Users/travis/Github/AnsibleLabs

# Check if virtual environment exists
if [ ! -d "ansible-env" ]; then
    echo "Virtual environment not found. Creating it..."
    ./fix-ansible-env.sh
fi

# Activate virtual environment
source ansible-env/bin/activate

# Get the Python interpreter from the venv (not aliased python)
VENV_PYTHON="$VIRTUAL_ENV/bin/python"

# Use the ansible executable directly from venv, or use venv's python
echo "Using Ansible from virtual environment"
echo "Python: $VENV_PYTHON"
echo "Ansible: $($VENV_PYTHON -m ansible --version 2>&1 | head -1 || ansible --version 2>&1 | head -1)"
echo ""

# Run the command passed as arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 <ansible-command>"
    echo "Example: $0 'all -m info_ping'"
    echo "Example: $0 'playbook test-info-ping.yml'"
    exit 1
fi

# Check if it's a playbook command
if [[ "$1" == "playbook" ]]; then
    shift
    ANSIBLE_LIBRARY=./library "$VENV_PYTHON" -m ansible.playbook "$@"
else
    # Try using ansible executable first, fallback to python -m
    if command -v ansible >/dev/null 2>&1 && [[ "$(which ansible)" == "$VIRTUAL_ENV/bin/ansible" ]]; then
        ANSIBLE_LIBRARY=./library ansible "$@"
    else
        ANSIBLE_LIBRARY=./library "$VENV_PYTHON" -m ansible "$@"
    fi
fi
