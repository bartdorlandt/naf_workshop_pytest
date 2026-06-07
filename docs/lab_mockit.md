# LAB: Mock'it — Testing Against a Simulated Device

## Objective

Write pytest tests that connect to a real (but simulated) Cisco IOS device running in Docker, send CLI commands, parse the output, and assert the results are correct.

This is the complement to the mocking lab: instead of replacing the device with a Python `Mock`, you run an actual SSH endpoint that returns **deterministic, file-backed responses** — making it fully testable without hardware.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed and running
- The rest of the workshop setup (`uv sync`, virtual env activated)

## Setup

### 1. Start the mock device

```bash
cd labs/lab_mockit
docker compose up -d
```

Verify it's running:

```bash
docker compose ps
# cisco_ios should show "running"
```

### 2. Confirm SSH access

```bash
# SSH to the mock device on localhost:2222
# Ignore host key checking since it's a mock device and has a freshly generated key each time
ssh -p 2222 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null test@localhost
# password: test
# You should land at a Cisco IOS prompt
```

Type `show version` to confirm you get output, then `exit`.

### 3. Copy the lab files to your working directory

```bash
# from the root of this project
cp labs/lab_mockit/device_connector.py .
cp labs/lab_mockit/output_parser.py .
```

The lab provides two stub modules:

- `device_connector.py` — functions to open an SSH session and run commands via Netmiko
- `output_parser.py` — functions that parse raw CLI output into Python data structures

Your job is to **implement the parsers and write tests** that verify them against the live mock device.

## How Mock'it works

The mock device serves static response files over SSH. When you run `show version`, it reads `configs/cisco_ios/templates/show version.txt` and returns that content verbatim. The responses are **fixed**, so your tests will always get the same output — making assertions reliable and repeatable.

The template files are mounted from `labs/lab_mockit/configs/cisco_ios/templates/`. You can read them directly to understand what output to expect before writing your tests.

## Exercise 1: Connectivity and Show Version

Implement `get_connection()` and `send_command()` in `device_connector.py`, then write tests that:

- Open a connection to `127.0.0.1:2222` with username/password `test`
- Assert `connection.is_alive()` returns `True`
- Send `show version` and assert the output is non-empty
- Assert the output contains `"IOS XE"`
- Implement `parse_ios_version()` to extract `version`, `hostname`, and interface count
- Assert the parsed values match the template file

Use a session-scoped fixture in `conftest.py` so the SSH connection is opened once and reused across all tests.

## Exercise 2: Parse Show IP Interface Brief

Send `show ip interface brief` and implement `parse_ip_interface_brief()`.

- Parse each interface into a dict with keys: `interface`, `ip`, `status`, `protocol`
- Assert the correct number of interfaces is returned (check the template file)
- Assert `Loopback0` has the correct IP address
- Assert an administratively down interface shows `"administratively"` as its status
- Assert a subinterface (`Ethernet0/0.11`) has the expected IP

## Exercise 3: Parse Show IP BGP Summary

Send `show ip bgp summary` and implement `parse_bgp_summary()`.

- Return a dict with `router_id`, `local_as`, and `neighbors` (list of dicts)
- Each neighbor dict should have `neighbor`, `remote_as`, `state`
- Assert the local AS number
- Assert the router ID
- Assert the total neighbor count
- Assert a specific neighbor's remote AS
- Assert that the last neighbor (`10.0.0.10`) shows an idle state

## Exercise 4: Parametrize

Use `@pytest.mark.parametrize` to write data-driven tests across multiple commands.

- Parametrize a test that sends each of the four commands and asserts the output is non-empty
- Parametrize a test that checks each command's output for an expected substring
- Combine all four parsers into a single parametrized test using a `(parser, command, assertion)` pattern

## Teardown

Stop the mock device when you're done:

```bash
cd labs/lab_mockit
docker compose down
```

## Checkpoint

!!! success "Solution"

    A complete solution for this lab is provided in the `solutions/lab_mockit/` directory.

    Run it with:
    ```bash
    # Make sure the mock device is running first (see Setup above)
    cd solutions/lab_mockit && uv run pytest -v
    ```
