# Solutions Directory

This directory contains the complete solution for the hands-on exercise in Chapter 4: Developing Ansible Modules.

## Solution File

### info_ping.py

This is the complete, enhanced version of the `info_ping` module that includes:

- **Original functionality:**
  - FQDN (Fully Qualified Domain Name) detection
  - CPU model information
  - Memory information (total and available)

- **Exercise enhancement:**
  - CPU core count detection
  - Cross-platform support (Linux and macOS)
  - Enhanced error handling

## Key Features

### CPU Core Detection

The solution includes a new `get_cpu_cores()` function that:

- Uses `sysctl -n hw.ncpu` on macOS systems
- Parses `/proc/cpuinfo` on Linux systems to count unique processor entries
- Falls back to `os.cpu_count()` for cross-platform compatibility
- Returns 0 if detection fails (graceful error handling)

### Updated Documentation

The `RETURN` section has been updated to include:

```yaml
cpu_cores:
    description: Number of CPU cores
    returned: always
    type: int
    sample: 4
```

### Integration

The CPU core count is:

1. Gathered in the `main()` function: `cpu_cores = get_cpu_cores()`
2. Added to the result dictionary: `cpu_cores=cpu_cores`
3. Returned to Ansible along with other system information

## Usage

To use this solution:

1. Copy `info_ping.py` to your Ansible project's `library/` directory
2. Ensure the module is executable: `chmod +x library/info_ping.py`
3. Test with: `ansible localhost -m info_ping`

## Testing

The solution has been tested on:

- Linux systems (Fedora, RHEL, Ubuntu)
- macOS systems (Darwin)

## Comparison with Exercise

This solution matches the working implementation from the AnsibleLabs repository, with the addition of CPU core count functionality as specified in the exercise.
