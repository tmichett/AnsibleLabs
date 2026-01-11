#!/bin/bash
# Test the custom info_ping module using ad-hoc commands

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Warning: Not in a virtual environment."
    echo "Activate the virtual environment first:"
    echo "  source ansible-env/bin/activate"
    echo ""
    echo "Or use the helper script:"
    echo "  ./use-ansible-venv.sh 'all -m info_ping'"
    echo ""
    
    # Try to use venv if it exists
    if [ -d "ansible-env" ]; then
        echo "Activating virtual environment..."
        source ansible-env/bin/activate
    else
        echo "Virtual environment not found. Please create it first:"
        echo "  ./fix-ansible-env.sh"
        exit 1
    fi
fi

# Get the Python interpreter from the venv (not aliased python)
VENV_PYTHON="$VIRTUAL_ENV/bin/python"

echo "Testing info_ping module with ad-hoc command..."
echo "=========================================="
echo "Using Python: $VENV_PYTHON"
echo ""

# Try using ansible executable first, fallback to python -m
# Note: info_ping doesn't need sudo, so we don't use -K flag
if command -v ansible >/dev/null 2>&1 && [[ "$(which ansible)" == "$VIRTUAL_ENV/bin/ansible" ]]; then
    echo "Running: ansible all -m info_ping"
    ANSIBLE_LIBRARY=./library ansible all -m info_ping
else
    echo "Running: $VENV_PYTHON -m ansible all -m info_ping"
    ANSIBLE_LIBRARY=./library "$VENV_PYTHON" -m ansible all -m info_ping
fi

echo ""
echo "=========================================="
echo "Ad-hoc test completed!"
echo ""
echo "To test with a playbook, run:"
if command -v ansible-playbook >/dev/null 2>&1 && [[ "$(which ansible-playbook)" == "$VIRTUAL_ENV/bin/ansible-playbook" ]]; then
    echo "  ansible-playbook test-info-ping.yml"
else
    echo "  $VENV_PYTHON -m ansible.playbook test-info-ping.yml"
    echo "  Or: ./use-ansible-venv.sh 'playbook test-info-ping.yml'"
fi
