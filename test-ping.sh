#!/bin/bash
# Test Ansible connectivity to all hosts using ping module

echo "Testing Ansible connectivity to all hosts..."
echo "=========================================="
echo ""

ansible all -m ping

echo ""
echo "=========================================="
echo "Ping test completed!"
