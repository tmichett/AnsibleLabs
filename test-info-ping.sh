#!/bin/bash
# Test the custom info_ping module using ad-hoc commands

echo "Testing info_ping module with ad-hoc command..."
echo "=========================================="
echo ""

# Test with ansible command
echo "Running: ansible all -m info_ping"
ansible all -m info_ping

echo ""
echo "=========================================="
echo "Ad-hoc test completed!"
echo ""
echo "To test with a playbook, run:"
echo "  ansible-playbook test-info-ping.yml"
