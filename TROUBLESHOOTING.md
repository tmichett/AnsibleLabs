# Troubleshooting Guide for AnsibleLabs

## Common Issues and Solutions

### Cryptography/CFFI Module Errors

If you encounter errors like:
```
ModuleNotFoundError: No module named '_cffi_backend'
pyo3_runtime.PanicException: Python API call failed
```

This typically indicates a compatibility issue between Python, cryptography, and Ansible.

#### Solution 1: Reinstall Dependencies

```bash
pip install --upgrade --force-reinstall cryptography cffi
pip install --upgrade --force-reinstall ansible-core
```

#### Solution 2: Use Python 3.11 or 3.12

Python 3.14 is very new and may have compatibility issues. Consider using Python 3.11 or 3.12:

```bash
# Check current Python version
python3 --version

# If using Python 3.14, consider installing Python 3.12
# On macOS with Homebrew:
brew install python@3.12

# Create a virtual environment with Python 3.12
python3.12 -m venv ansible-env
source ansible-env/bin/activate
pip install ansible-core
```

#### Solution 3: Use a Virtual Environment

Isolate your Python environment to avoid conflicts:

```bash
# Create virtual environment
python3 -m venv ~/ansible-env

# Activate it
source ~/ansible-env/bin/activate

# Install Ansible
pip install ansible-core

# Verify installation
ansible --version
```

#### Solution 4: Check Python and Ansible Paths

Ensure you're using compatible versions:

```bash
# Check which Python Ansible is using
ansible --version

# Check Python version
python3 --version

# Check installed packages
pip list | grep -E "(ansible|cryptography|cffi)"
```

### Using System Ansible Instead of Virtual Environment

If you've installed Ansible in a virtual environment but still get errors from the system installation:

**Problem:** The `ansible` command is using the system installation at `/usr/local/bin/ansible` instead of the venv.

**Solution 1: Use `python -m ansible` (Recommended)**

Instead of using the `ansible` command, use Python's module execution:

```bash
# Activate virtual environment
source ansible-env/bin/activate

# Use python -m ansible instead of ansible
ANSIBLE_LIBRARY=./library python -m ansible localhost -m info_ping

# For playbooks
python -m ansible.playbook test-info-ping.yml
```

**Solution 2: Use the helper script**

```bash
./use-ansible-venv.sh "localhost -m info_ping"
./use-ansible-venv.sh "playbook test-info-ping.yml"
```

**Solution 3: Ensure venv is in PATH**

```bash
# Activate virtual environment
source ansible-env/bin/activate

# Verify which ansible is being used
which ansible
# Should show: /Users/travis/Github/AnsibleLabs/ansible-env/bin/ansible

# If it doesn't, the venv's bin directory needs to be first in PATH
export PATH="$VIRTUAL_ENV/bin:$PATH"
```

### Module Not Found Errors

If Ansible can't find your custom module:

1. **Verify library path in ansible.cfg:**
   ```ini
   [defaults]
   library = ./library
   ```

2. **Check module file permissions:**
   ```bash
   chmod +x library/info_ping.py
   ```

3. **Test with explicit library path:**
   ```bash
   # Using python -m (recommended)
   ANSIBLE_LIBRARY=./library python -m ansible localhost -m info_ping
   
   # Or with ansible command (if venv is properly activated)
   ANSIBLE_LIBRARY=./library ansible localhost -m info_ping
   ```

4. **Verify module location:**
   ```bash
   ls -la library/info_ping.py
   ```

### Connection Issues

If you can't connect to lab VMs:

1. **Verify VMs are running:**
   ```bash
   cd ../Fedora_Remix_Lab
   sudo ./lab-status.sh
   ```

2. **Check network connectivity:**
   ```bash
   ping fedoralab1.example.com
   ping fedoralab2.example.com
   ```

3. **Verify /etc/hosts entries:**
   ```bash
   cd ../Fedora_Remix_Lab
   ./manage-hosts.sh status
   ```

### Sudo/Become Password Errors

If you get "Duplicate become password prompt" errors:

**Problem:** Ansible is trying to use sudo when it's not needed (like with `info_ping` module).

**Solution 1: Don't use -K flag for modules that don't need sudo**

```bash
# info_ping doesn't need sudo, so don't use -K
ANSIBLE_LIBRARY=./library ansible localhost -m info_ping

# If you need sudo for other tasks, use it per-task in playbooks
```

**Solution 2: Disable become for specific tasks**

In playbooks, explicitly set `become: no`:

```yaml
- name: Test info_ping (no sudo needed)
  hosts: localhost
  become: no
  tasks:
    - name: Get system info
      info_ping:
```

**Solution 3: Update ansible.cfg**

The default `become = True` in ansible.cfg has been commented out. If you need sudo for specific tasks, enable it per-task or per-playbook.

### Permission Errors

If you get permission denied errors:

1. **Check SSH key permissions:**
   ```bash
   chmod 600 ~/.ssh/id_rsa
   ```

2. **Verify sudo configuration on target hosts:**
   - The `ansibleuser` should have passwordless sudo
   - Check `/etc/sudoers.d/ansibleuser` on target VMs

### Getting Help

For more detailed troubleshooting:

1. **Run with verbose output:**
   ```bash
   ansible all -m info_ping -vvv
   ```

2. **Check Ansible configuration:**
   ```bash
   ansible-config dump
   ```

3. **Test module directly:**
   ```bash
   python3 library/info_ping.py
   ```

4. **Review Ansible documentation:**
   - https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html
