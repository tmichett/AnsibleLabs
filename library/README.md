# Custom Ansible Modules

This directory contains custom Ansible modules for the AnsibleLabs project.

## Available Modules

### info_ping

An extended ping module that returns system information along with connectivity status.

**Returns:**
- `ping` - Ping response message (default: "pong")
- `fqdn` - Fully Qualified Domain Name of the target host
- `cpu_model` - CPU make and model information
- `memory_total_mb` - Total memory in megabytes
- `memory_available_mb` - Available memory in megabytes

**Usage:**

```yaml
- name: Test connectivity and get system info
  info_ping:
```

Or with custom data:

```yaml
- name: Test connectivity with custom message
  info_ping:
    data: "custom message"
```

**Testing:**

```bash
# Ad-hoc test
ansible all -m info_ping

# Using test script
./test-info-ping.sh

# Using playbook
ansible-playbook test-info-ping.yml
```

## Module Development

For detailed information about developing Ansible modules, see the guide in the AnsibleLabsBook project:
`AnsibleLabsBook/Chapters/CH_Modules/Developing_Ansible_Modules.adoc`
