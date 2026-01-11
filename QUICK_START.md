# Quick Start Guide for Testing info_ping Module

## The Problem

If you're getting errors like:
- `ModuleNotFoundError: No module named '_cffi_backend'`
- `No module named ansible` when using `python -m ansible`
- Cryptography/Pyo3 panic errors

This is due to Python version mismatches and virtual environment configuration.

## Quick Solution

### Option 1: Use the Helper Script (Easiest)

```bash
cd /Users/travis/Github/AnsibleLabs

# Test the module
./use-ansible-venv.sh "localhost -m info_ping"

# Or test all hosts
./use-ansible-venv.sh "all -m info_ping"

# Run a playbook
./use-ansible-venv.sh "playbook test-info-ping.yml"
```

### Option 2: Use Ansible Executable Directly

```bash
cd /Users/travis/Github/AnsibleLabs

# Activate virtual environment
source ansible-env/bin/activate

# Use ansible executable directly (not python -m)
# Note: info_ping doesn't need sudo, so no -K flag needed
ANSIBLE_LIBRARY=./library ansible localhost -m info_ping
```

**Important:** The `info_ping` module doesn't require sudo privileges, so you don't need the `-K` (become password) flag. If you see sudo password prompts, it's because `become` was enabled in ansible.cfg (now fixed).

### Option 3: Use Venv's Python Explicitly

```bash
cd /Users/travis/Github/AnsibleLabs

# Activate virtual environment
source ansible-env/bin/activate

# Use the venv's Python explicitly (not the aliased python)
ANSIBLE_LIBRARY=./library "$VIRTUAL_ENV/bin/python" -m ansible localhost -m info_ping
```

## Why This Happens

1. **Python Aliases**: Your shell may have `python` aliased to `python3.12`, but the venv was created with Python 3.14
2. **PATH Issues**: The system `ansible` at `/usr/local/bin/ansible` may be found before the venv's `ansible`
3. **Module Import**: When using `python -m ansible`, it uses the aliased Python (3.12) which doesn't have ansible installed

## Recommended Approach

**Always use the ansible executable from the venv directly:**

```bash
source ansible-env/bin/activate
ANSIBLE_LIBRARY=./library ansible localhost -m info_ping
```

The `ansible` executable in the venv's `bin/` directory will use the correct Python interpreter automatically.

## Verify Your Setup

```bash
# Activate venv
source ansible-env/bin/activate

# Check which ansible is being used
which ansible
# Should show: /Users/travis/Github/AnsibleLabs/ansible-env/bin/ansible

# Check Python version
"$VIRTUAL_ENV/bin/python" --version

# Test the module
ANSIBLE_LIBRARY=./library ansible localhost -m info_ping
```
