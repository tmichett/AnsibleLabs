#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, AnsibleLabs
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: info_ping
short_description: Extended ping module that returns FQDN, CPU, and RAM information
version_added: "1.0.0"
description:
    - This module extends the basic ping functionality by returning system information
    - It provides FQDN, CPU make/model, and RAM information
    - Always returns success (pong) if the host is reachable
author:
    - AnsibleLabs
options:
    data:
        description:
            - Optional data to return with the ping response
        required: false
        type: str
        default: "pong"
notes:
    - This module does not make any changes to the system
    - It is designed for connectivity testing and system information gathering
'''

EXAMPLES = r'''
# Basic ping test
- name: Test connectivity and get system info
  info_ping:

# Ping with custom data
- name: Test connectivity with custom message
  info_ping:
    data: "custom message"
'''

RETURN = r'''
ping:
    description: The ping response message
    returned: always
    type: str
    sample: pong
fqdn:
    description: Fully Qualified Domain Name of the target host
    returned: always
    type: str
    sample: fedoralab1.example.com
cpu_model:
    description: CPU make and model information
    returned: always
    type: str
    sample: Intel(R) Core(TM) i7-8700 CPU @ 3.20GHz
memory_total_mb:
    description: Total memory in megabytes
    returned: always
    type: int
    sample: 1024
memory_available_mb:
    description: Available memory in megabytes
    returned: always
    type: int
    sample: 512
'''

import platform
import socket
import os

from ansible.module_utils.basic import AnsibleModule


def get_fqdn():
    """Get the Fully Qualified Domain Name of the host."""
    try:
        fqdn = socket.getfqdn()
        if fqdn:
            return fqdn
        # Fallback to hostname if FQDN is not available
        return socket.gethostname()
    except Exception:
        return platform.node()


def get_cpu_info():
    """Get CPU make and model information."""
    try:
        # Try to read from /proc/cpuinfo (Linux)
        if os.path.exists('/proc/cpuinfo'):
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if 'model name' in line.lower() or 'processor' in line.lower():
                        if 'model name' in line.lower():
                            return line.split(':')[1].strip()
        # Fallback to platform processor
        return platform.processor() or platform.machine()
    except Exception:
        return "Unknown CPU"


def get_memory_info():
    """Get memory information in megabytes."""
    try:
        # Try to read from /proc/meminfo (Linux)
        if os.path.exists('/proc/meminfo'):
            meminfo = {}
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 2:
                        key = parts[0].rstrip(':')
                        value = int(parts[1])
                        meminfo[key] = value
            
            total_mb = meminfo.get('MemTotal', 0) // 1024
            available_mb = meminfo.get('MemAvailable', 0) // 1024
            # If MemAvailable is not available, calculate from MemFree and buffers/cached
            if available_mb == 0:
                mem_free = meminfo.get('MemFree', 0) // 1024
                buffers = meminfo.get('Buffers', 0) // 1024
                cached = meminfo.get('Cached', 0) // 1024
                available_mb = mem_free + buffers + cached
            
            return total_mb, available_mb
        else:
            # Fallback for non-Linux systems
            # This is a simplified approach - may not work on all systems
            return 0, 0
    except Exception:
        return 0, 0


def main():
    """Main function for info_ping module."""
    module_args = dict(
        data=dict(type='str', required=False, default='pong')
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Get system information
    fqdn = get_fqdn()
    cpu_model = get_cpu_info()
    memory_total_mb, memory_available_mb = get_memory_info()

    result = dict(
        changed=False,
        ping=module.params['data'],
        fqdn=fqdn,
        cpu_model=cpu_model,
        memory_total_mb=memory_total_mb,
        memory_available_mb=memory_available_mb
    )

    module.exit_json(**result)


if __name__ == '__main__':
    main()
