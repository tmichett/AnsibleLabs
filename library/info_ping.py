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
import subprocess

from ansible.module_utils.basic import AnsibleModule


def get_fqdn():
    """Get the Fully Qualified Domain Name of the host."""
    try:
        # Try hostname -f first (works on both Linux and macOS)
        if platform.system() in ['Darwin', 'Linux']:
            try:
                result = subprocess.run(['hostname', '-f'], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=5)
                if result.returncode == 0 and result.stdout.strip():
                    fqdn = result.stdout.strip()
                    # Don't return reverse DNS entries
                    if not fqdn.endswith('.in-addr.arpa') and not fqdn.endswith('.ip6.arpa'):
                        return fqdn
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                pass
        
        # Try socket.getfqdn() but filter out reverse DNS
        fqdn = socket.getfqdn()
        if fqdn and not fqdn.endswith('.in-addr.arpa') and not fqdn.endswith('.ip6.arpa'):
            return fqdn
        
        # Fallback to hostname
        hostname = socket.gethostname()
        if hostname:
            return hostname
        
        # Last resort
        return platform.node()
    except Exception:
        return platform.node()


def get_cpu_info():
    """Get CPU make and model information."""
    try:
        system = platform.system()
        
        # macOS - use sysctl
        if system == 'Darwin':
            try:
                result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'],
                                      capture_output=True,
                                      text=True,
                                      timeout=5)
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                pass
        
        # Linux - read from /proc/cpuinfo
        elif system == 'Linux':
            if os.path.exists('/proc/cpuinfo'):
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if 'model name' in line.lower():
                            return line.split(':')[1].strip()
        
        # Fallback: Try platform.processor()
        processor = platform.processor()
        if processor and processor != '' and processor != 'i386':
            return processor
        
        # Last resort: platform.machine() if it's not generic
        machine = platform.machine()
        if machine and machine not in ['i386', 'x86_64', 'AMD64']:
            return machine
        
        return "Unknown CPU"
    except Exception:
        return "Unknown CPU"


def get_memory_info():
    """Get memory information in megabytes."""
    try:
        system = platform.system()
        
        # macOS - use sysctl
        if system == 'Darwin':
            try:
                # Get total memory
                result = subprocess.run(['sysctl', '-n', 'hw.memsize'],
                                      capture_output=True,
                                      text=True,
                                      timeout=5)
                if result.returncode == 0:
                    total_bytes = int(result.stdout.strip())
                    total_mb = total_bytes // (1024 * 1024)
                    
                    # Get available memory using vm_stat (approximate)
                    try:
                        result = subprocess.run(['vm_stat'],
                                              capture_output=True,
                                              text=True,
                                              timeout=5)
                        if result.returncode == 0:
                            # Parse vm_stat output for free pages
                            # This is approximate - macOS doesn't have a simple "available" metric
                            lines = result.stdout.split('\n')
                            free_pages = 0
                            inactive_pages = 0
                            page_size = 4096  # Default page size on macOS
                            
                            for line in lines:
                                if 'Pages free' in line:
                                    try:
                                        free_pages = int(line.split(':')[1].strip().rstrip('.'))
                                    except (ValueError, IndexError):
                                        pass
                                elif 'Pages inactive' in line:
                                    try:
                                        inactive_pages = int(line.split(':')[1].strip().rstrip('.'))
                                    except (ValueError, IndexError):
                                        pass
                            
                            # Calculate available memory (free + inactive)
                            available_bytes = (free_pages + inactive_pages) * page_size
                            available_mb = available_bytes // (1024 * 1024)
                            
                            return total_mb, available_mb
                    except Exception:
                        pass
                    
                    # If vm_stat parsing failed, return total as available (conservative)
                    return total_mb, total_mb
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError, ValueError):
                pass
        
        # Linux - read from /proc/meminfo
        elif system == 'Linux':
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
        
        # Fallback for other systems
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
